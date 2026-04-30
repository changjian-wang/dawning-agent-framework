using Dawning.AgentOS.Application.Messaging;
using Dawning.AgentOS.Domain.Core;
using MediatR;
using NUnit.Framework;

namespace Dawning.AgentOS.Application.Tests.Messaging;

/// <summary>
/// Pins the inheritance chains of the CQRS marker interfaces. ADR-018 defines
/// the contract; ADR-021 places these markers under <c>Application/Messaging/</c>.
/// </summary>
[TestFixture]
public sealed class MarkerInterfaceTests
{
    [Test]
    public void ICommand_NoResponse_InheritsIRequestOfResult()
    {
        Assert.That(
            typeof(IRequest<Result>).IsAssignableFrom(typeof(ICommand)),
            Is.True,
            "ICommand must be IRequest<Result> so MediatR can dispatch it to a handler that returns Result."
        );
    }

    [Test]
    public void ICommand_OfT_InheritsIRequestOfResultOfT()
    {
        Assert.That(
            typeof(IRequest<Result<int>>).IsAssignableFrom(typeof(ICommand<int>)),
            Is.True,
            "ICommand<T> must be IRequest<Result<T>>."
        );
    }

    [Test]
    public void IQuery_OfT_InheritsIRequestOfResultOfT()
    {
        Assert.That(
            typeof(IRequest<Result<int>>).IsAssignableFrom(typeof(IQuery<int>)),
            Is.True,
            "IQuery<T> must be IRequest<Result<T>> so read-side failures stay uniform with the command path."
        );
    }
}
