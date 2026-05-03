using Microsoft.Extensions.Options;

namespace Dawning.AgentOS.Infrastructure.Options;

/// <summary>
/// Strongly-typed bind target for the <c>Llm</c> configuration section.
/// Per ADR-028 §决策 E1 / F1 / G2 V0 holds:
/// <list type="bullet">
///   <item>
///     <description>
///       a single <see cref="ActiveProvider"/> string that selects which
///       <c>ILlmProvider</c> implementation gets registered;
///     </description>
///   </item>
///   <item>
///     <description>
///       a per-provider sub-section with <c>ApiKey</c> / <c>BaseUrl</c> /
///       <c>Model</c>; ApiKey defaults to empty string and is supplied
///       at runtime through environment variables, dotnet user-secrets,
///       or <c>appsettings.{Environment}.json</c>.
///     </description>
///   </item>
/// </list>
/// </summary>
/// <remarks>
/// Per ADR-028 §决策 G2 the validation deliberately fail-fasts on a
/// structurally-invalid <see cref="ActiveProvider"/> (otherwise the DI
/// composition cannot pick a provider) but does <em>not</em> reject an
/// empty <c>ApiKey</c>: that becomes a per-call
/// <c>LlmErrors.AuthenticationFailed</c> at runtime so the host stays
/// up and the rest of the surface (inbox, runtime status) remains
/// usable while the user configures their key.
/// </remarks>
public sealed class LlmOptions
{
    /// <summary>Configuration section name expected by <c>builder.Configuration.GetSection</c>.</summary>
    public const string SectionName = "Llm";

    /// <summary>Canonical name for the OpenAI provider.</summary>
    public const string OpenAiProviderName = "OpenAI";

    /// <summary>Canonical name for the DeepSeek provider.</summary>
    public const string DeepSeekProviderName = "DeepSeek";

    /// <summary>
    /// The provider whose <see cref="ILlmProvider"/> implementation gets
    /// registered. Must be one of <see cref="OpenAiProviderName"/> or
    /// <see cref="DeepSeekProviderName"/>; case-sensitive.
    /// </summary>
    public string ActiveProvider { get; set; } = OpenAiProviderName;

    /// <summary>Per-provider configuration map keyed by provider name.</summary>
    public LlmProvidersOptions Providers { get; set; } = new();
}

/// <summary>Container for the per-provider sub-sections under <c>Llm:Providers</c>.</summary>
public sealed class LlmProvidersOptions
{
    /// <summary>OpenAI provider settings.</summary>
    public LlmProviderOptions OpenAI { get; set; } = new()
    {
        BaseUrl = "https://api.openai.com/v1",
        Model = "gpt-4o-mini",
    };

    /// <summary>DeepSeek provider settings.</summary>
    public LlmProviderOptions DeepSeek { get; set; } = new()
    {
        BaseUrl = "https://api.deepseek.com",
        Model = "deepseek-chat",
    };
}

/// <summary>Settings shared by every provider implementation.</summary>
public sealed class LlmProviderOptions
{
    /// <summary>
    /// API key supplied at runtime. Empty string is allowed and surfaces
    /// at call time as <c>LlmErrors.AuthenticationFailed</c>; this is
    /// the explicit V0 contract per ADR-028 §决策 G2.
    /// </summary>
    public string ApiKey { get; set; } = string.Empty;

    /// <summary>HTTP base URL the named <see cref="System.Net.Http.HttpClient"/> uses; must include scheme.</summary>
    public string BaseUrl { get; set; } = string.Empty;

    /// <summary>Default model identifier sent when the request omits <see cref="Application.Abstractions.Llm.LlmRequest.Model"/>.</summary>
    public string Model { get; set; } = string.Empty;
}

/// <summary>
/// IOptions validator enforcing the structural constraint of ADR-028
/// §决策 G2: <see cref="LlmOptions.ActiveProvider"/> must name a known
/// provider. ApiKey is intentionally <em>not</em> validated here — see
/// the type-level remarks.
/// </summary>
public sealed class LlmOptionsValidator : IValidateOptions<LlmOptions>
{
    /// <inheritdoc />
    public ValidateOptionsResult Validate(string? name, LlmOptions options)
    {
        ArgumentNullException.ThrowIfNull(options);

        var active = options.ActiveProvider;
        if (string.IsNullOrWhiteSpace(active))
        {
            return ValidateOptionsResult.Fail(
                $"Configuration '{LlmOptions.SectionName}:ActiveProvider' is required."
            );
        }

        if (
            !string.Equals(active, LlmOptions.OpenAiProviderName, StringComparison.Ordinal)
            && !string.Equals(active, LlmOptions.DeepSeekProviderName, StringComparison.Ordinal)
        )
        {
            return ValidateOptionsResult.Fail(
                $"Configuration '{LlmOptions.SectionName}:ActiveProvider' must be "
                    + $"'{LlmOptions.OpenAiProviderName}' or '{LlmOptions.DeepSeekProviderName}'; "
                    + $"got '{active}'."
            );
        }

        return ValidateOptionsResult.Success;
    }
}
