using Dawning.AgentOS.Application.Messaging;

namespace Dawning.AgentOS.Application.Runtime;

/// <summary>
/// Read-side query that returns the current <see cref="RuntimeStatus"/>
/// snapshot. Carries no parameters; uptime is computed against an injected
/// clock and start-time provider in the handler.
/// </summary>
public sealed record GetRuntimeStatusQuery : IQuery<RuntimeStatus>;
