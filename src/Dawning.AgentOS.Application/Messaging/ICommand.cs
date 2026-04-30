using Dawning.AgentOS.Domain.Core;
using MediatR;

namespace Dawning.AgentOS.Application.Messaging;

/// <summary>
/// Marker for write-side use cases that mutate state and return no value on
/// success. Implementations are dispatched through MediatR; the handler
/// must implement <see cref="IRequestHandler{TRequest, TResponse}"/> with
/// <typeparamref name="TRequest"/> = the concrete command and
/// <typeparamref name="TResponse"/> = <see cref="Result"/>.
/// </summary>
/// <remarks>
/// Per ADR-018 business failures are conveyed via <see cref="Result"/>, not
/// thrown exceptions. Per ADR-021 this marker lives under
/// <c>Application/Messaging/</c> rather than <c>Common/Messaging/</c>.
/// </remarks>
public interface ICommand : IRequest<Result> { }

/// <summary>
/// Marker for write-side use cases that mutate state and return a value on
/// success.
/// </summary>
/// <typeparam name="TResponse">Type of the success value.</typeparam>
public interface ICommand<TResponse> : IRequest<Result<TResponse>> { }
