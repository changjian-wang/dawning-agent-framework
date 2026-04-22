<#
.SYNOPSIS
  Renders Mermaid .mmd source files to .svg using local mermaid-cli (mmdc).
.DESCRIPTION
  Walks the docs tree, finds every .mmd file, and renders a sibling .svg.
  SVG是矢量格式，体积小、可缩放、文本可检索，且对 git diff 友好。
.PARAMETER Root
  Root directory to scan. Defaults to the docs folder.
.PARAMETER Force
  Re-render even if .svg is newer than .mmd.
.EXAMPLE
  pwsh docs/scripts/render-mermaid-svg.ps1
  pwsh docs/scripts/render-mermaid-svg.ps1 -Force
#>
param(
    [string]$Root = (Join-Path $PSScriptRoot ".."),
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $Root).Path

# Ensure mmdc is available
$mmdc = Get-Command mmdc -ErrorAction SilentlyContinue
if (-not $mmdc) {
    Write-Error "mmdc not found. Install via: npm install -g @mermaid-js/mermaid-cli"
    exit 1
}

$configPath = Join-Path $PSScriptRoot "mermaid-config.json"
$puppeteerPath = Join-Path $PSScriptRoot "puppeteer-config.json"

$files = Get-ChildItem -Path $Root -Recurse -Filter "*.mmd"
Write-Host "Found $($files.Count) .mmd files under $Root"

$ok = 0; $skip = 0; $fail = 0
foreach ($f in $files) {
    $svg = [IO.Path]::ChangeExtension($f.FullName, ".svg")
    if (-not $Force -and (Test-Path $svg) -and ((Get-Item $svg).LastWriteTime -ge $f.LastWriteTime)) {
        $skip++
        continue
    }

    $args = @("-i", $f.FullName, "-o", $svg, "-b", "transparent")
    if (Test-Path $configPath)    { $args += @("-c", $configPath) }
    if (Test-Path $puppeteerPath) { $args += @("-p", $puppeteerPath) }

    try {
        & mmdc @args 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0 -and (Test-Path $svg)) {
            Write-Host "OK:   $($f.FullName.Substring($Root.Length + 1)) -> .svg"
            $ok++
        } else {
            Write-Warning "FAIL: $($f.FullName) (exit $LASTEXITCODE)"
            $fail++
        }
    }
    catch {
        Write-Warning "FAIL: $($f.FullName) - $_"
        $fail++
    }
}

Write-Host ""
Write-Host "Summary: $ok rendered, $skip up-to-date, $fail failed"
if ($fail -gt 0) { exit 1 }
