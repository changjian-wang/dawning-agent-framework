<#
.SYNOPSIS
  Renders Mermaid markup files to PNG via mermaid.ink API.
.PARAMETER InputDir
  Directory containing .mmd files.
.PARAMETER OutputDir
  Directory for output PNG files.
#>
param(
    [string]$InputDir,
    [string]$OutputDir
)

Get-ChildItem "$InputDir\*.mmd" | ForEach-Object {
    $name = $_.BaseName
    $code = Get-Content $_.FullName -Raw -Encoding UTF8
    $json = @{ code = $code; mermaid = @{ theme = "default" } } | ConvertTo-Json -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)

    # Use pako/deflate compression (required by mermaid.ink)
    $ms = New-Object System.IO.MemoryStream
    $ds = New-Object System.IO.Compression.DeflateStream($ms, [System.IO.Compression.CompressionLevel]::Optimal)
    $ds.Write($bytes, 0, $bytes.Length)
    $ds.Close()
    $compressed = $ms.ToArray()
    $ms.Close()

    # Wrap in zlib format (header + deflate + checksum)
    $zlibHeader = [byte[]](0x78, 0x9C)
    $adler = [uint32]1
    $a = [uint32]1; $b = [uint32]0
    foreach ($byte in $bytes) {
        $a = ($a + $byte) % 65521
        $b = ($b + $a) % 65521
    }
    $checksum = [BitConverter]::GetBytes([uint32](($b -shl 16) -bor $a))
    [Array]::Reverse($checksum)  # big-endian
    $zlibData = $zlibHeader + $compressed + $checksum

    $base64 = [Convert]::ToBase64String($zlibData).Replace('+', '-').Replace('/', '_').TrimEnd('=')
    $url = "https://mermaid.ink/img/pako:$base64"

    $outFile = Join-Path $OutputDir "$name.png"
    try {
        Invoke-WebRequest -Uri $url -OutFile $outFile -UseBasicParsing -UserAgent "Mozilla/5.0"
        Write-Output "OK: $name.png"
    }
    catch {
        Write-Warning "FAIL: $name - $_"
    }
}
