using Dawning.AgentOS.Application.Abstractions;
using Dawning.AgentOS.Application.Runtime;
using Moq;
using NUnit.Framework;

namespace Dawning.AgentOS.Application.Tests.Runtime;

/// <summary>
/// Verifies that the runtime status handler composes the clock and start-time
/// provider correctly, including non-negative uptime under clock skew.
/// </summary>
[TestFixture]
public sealed class GetRuntimeStatusQueryHandlerTests
{
    [Test]
    public async Task Handle_ReturnsSuccessWithComputedUptime()
    {
        var startedAt = new DateTimeOffset(2026, 4, 30, 12, 0, 0, TimeSpan.Zero);
        var now = startedAt + TimeSpan.FromMinutes(7);

        var clock = new Mock<IClock>(MockBehavior.Strict);
        clock.SetupGet(c => c.UtcNow).Returns(now);
        var provider = new Mock<IRuntimeStartTimeProvider>(MockBehavior.Strict);
        provider.SetupGet(p => p.StartedAtUtc).Returns(startedAt);

        var handler = new GetRuntimeStatusQueryHandler(clock.Object, provider.Object);

        var result = await handler.Handle(new GetRuntimeStatusQuery(), CancellationToken.None);

        Assert.Multiple(() =>
        {
            Assert.That(result.IsSuccess, Is.True);
            Assert.That(result.Value.StartedAtUtc, Is.EqualTo(startedAt));
            Assert.That(result.Value.NowUtc, Is.EqualTo(now));
            Assert.That(result.Value.Uptime, Is.EqualTo(TimeSpan.FromMinutes(7)));
            Assert.That(result.Value.Healthy, Is.True);
        });
    }

    [Test]
    public async Task Handle_ClampsUptimeToZero_WhenNowPrecedesStart()
    {
        // Defensive: if a backwards clock skew makes Now < StartedAt, the
        // handler must still return a non-negative TimeSpan rather than
        // surfacing a negative uptime to callers.
        var startedAt = new DateTimeOffset(2026, 4, 30, 12, 0, 0, TimeSpan.Zero);
        var now = startedAt - TimeSpan.FromSeconds(5);

        var clock = new Mock<IClock>(MockBehavior.Strict);
        clock.SetupGet(c => c.UtcNow).Returns(now);
        var provider = new Mock<IRuntimeStartTimeProvider>(MockBehavior.Strict);
        provider.SetupGet(p => p.StartedAtUtc).Returns(startedAt);

        var handler = new GetRuntimeStatusQueryHandler(clock.Object, provider.Object);

        var result = await handler.Handle(new GetRuntimeStatusQuery(), CancellationToken.None);

        Assert.Multiple(() =>
        {
            Assert.That(result.IsSuccess, Is.True);
            Assert.That(result.Value.Uptime, Is.EqualTo(TimeSpan.Zero));
        });
    }

    [Test]
    public void Constructor_ThrowsOnNullClock()
    {
        var provider = new Mock<IRuntimeStartTimeProvider>().Object;

        Assert.Throws<ArgumentNullException>(() =>
            new GetRuntimeStatusQueryHandler(null!, provider)
        );
    }

    [Test]
    public void Constructor_ThrowsOnNullStartTimeProvider()
    {
        var clock = new Mock<IClock>().Object;

        Assert.Throws<ArgumentNullException>(() => new GetRuntimeStatusQueryHandler(clock, null!));
    }

    [Test]
    public void Handle_ThrowsOnNullRequest()
    {
        var handler = new GetRuntimeStatusQueryHandler(
            new Mock<IClock>().Object,
            new Mock<IRuntimeStartTimeProvider>().Object
        );

        Assert.ThrowsAsync<ArgumentNullException>(() =>
            handler.Handle(null!, CancellationToken.None)
        );
    }
}
