using Dawning.AgentOS.Application.Abstractions;
using Dawning.AgentOS.Domain.Core;
using MediatR;

namespace Dawning.AgentOS.Application.Runtime;

/// <summary>
/// Handles <see cref="GetRuntimeStatusQuery"/> by composing the start-time
/// provider with the clock and reporting an always-healthy snapshot in V0.
/// </summary>
/// <remarks>
/// V0 always reports <c>Healthy = true</c>; later slices may probe the
/// SQLite store, the bus, or downstream LLM endpoints before flipping the
/// flag. The handler is the canonical reference for the Application layout
/// in ADR-021: ports under <c>Abstractions/</c>, marker under
/// <c>Messaging/</c>, slice files (<see cref="GetRuntimeStatusQuery"/>,
/// <see cref="RuntimeStatus"/>, this handler) under <c>Runtime/</c>.
/// </remarks>
public sealed class GetRuntimeStatusQueryHandler(
    IClock clock,
    IRuntimeStartTimeProvider startTimeProvider
) : IRequestHandler<GetRuntimeStatusQuery, Result<RuntimeStatus>>
{
    private readonly IClock _clock = clock ?? throw new ArgumentNullException(nameof(clock));
    private readonly IRuntimeStartTimeProvider _startTimeProvider =
        startTimeProvider ?? throw new ArgumentNullException(nameof(startTimeProvider));

    /// <inheritdoc />
    public Task<Result<RuntimeStatus>> Handle(
        GetRuntimeStatusQuery request,
        CancellationToken cancellationToken
    )
    {
        ArgumentNullException.ThrowIfNull(request);

        var startedAt = _startTimeProvider.StartedAtUtc;
        var now = _clock.UtcNow;
        var uptime = now >= startedAt ? now - startedAt : TimeSpan.Zero;

        var snapshot = new RuntimeStatus(
            StartedAtUtc: startedAt,
            NowUtc: now,
            Uptime: uptime,
            Healthy: true
        );

        return Task.FromResult(Result<RuntimeStatus>.Success(snapshot));
    }
}
