using Dawning.AgentOS.Domain.Core;

namespace Dawning.AgentOS.Application.Inbox;

/// <summary>
/// Factory helpers for inbox-side <see cref="DomainError"/> codes used by
/// the application layer. Per ADR-030 §决策 F1 the inbox-summarize path
/// adds exactly one new error: <c>inbox.notFound</c>, surfaced by the
/// API layer as HTTP 404 (manual mapping, see <c>InboxEndpoints</c>).
/// </summary>
/// <remarks>
/// Capture-time validation errors (<c>inbox.content.required</c>, etc.)
/// are emitted inline by <c>InboxAppService</c> rather than threaded
/// through this class — those are field-level errors that the existing
/// <c>ResultHttpExtensions.ToHttpResult</c> already maps correctly to
/// HTTP 400. This class collects the non-field errors that need bespoke
/// HTTP mapping.
/// </remarks>
public static class InboxErrors
{
    /// <summary>The error code returned when an inbox item lookup misses.</summary>
    public const string ItemNotFoundCode = "inbox.notFound";

    /// <summary>
    /// Builds an <see cref="DomainError"/> indicating that no inbox item
    /// matches the supplied id. Per ADR-030 §决策 F1 the API layer maps
    /// this to HTTP 404 in <c>InboxEndpoints</c>'s manual error switch.
    /// </summary>
    /// <param name="itemId">The id that produced the miss; included in the message for diagnostics.</param>
    /// <returns>A non-field-level error tagged with <see cref="ItemNotFoundCode"/>.</returns>
    public static DomainError ItemNotFound(Guid itemId) =>
        new(
            Code: ItemNotFoundCode,
            Message: $"Inbox item '{itemId}' not found.",
            Field: null
        );
}
