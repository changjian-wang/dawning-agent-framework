using Dawning.AgentOS.Domain.Core;
using MediatR;

namespace Dawning.AgentOS.Application.Messaging;

/// <summary>
/// Marker for read-side use cases that return a value and have no observable
/// side effects on aggregates.
/// </summary>
/// <typeparam name="TResponse">Type of the projection / DTO returned to the caller.</typeparam>
/// <remarks>
/// Per ADR-018 read-side use cases are still wrapped in <see cref="Result{T}"/>
/// so that caller-visible failures (e.g. NotFound, Forbidden) are uniform with
/// the command path. Per ADR-021 this marker lives under
/// <c>Application/Messaging/</c>.
/// </remarks>
public interface IQuery<TResponse> : IRequest<Result<TResponse>> { }
