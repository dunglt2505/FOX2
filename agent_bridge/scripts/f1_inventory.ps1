# Read-only AppLocker identity extraction. New-AppLockerPolicy constructs XML
# in memory; this script never calls Set-AppLockerPolicy or changes a service.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string[]]$LiteralPath)
$ErrorActionPreference = 'Stop'
Import-Module -Name (Join-Path $PSHOME 'Modules/AppLocker/AppLocker.psd1')
Import-Module -Name (Join-Path $PSHOME 'Modules/Microsoft.PowerShell.Utility/Microsoft.PowerShell.Utility.psd1')
$rows = foreach ($item in $LiteralPath) {
    $file = Get-Item -LiteralPath $item
    if ($file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw 'regular inventoried files required'
    }
    $information = Get-AppLockerFileInformation -Path $file.FullName
    [xml]$policy = New-AppLockerPolicy -FileInformation $information -RuleType Hash -User Everyone -Xml
    if (-not $policy.SelectNodes('//FileHashRule').Count) {
        throw 'Unsupported AppLocker surface: inventory interpreter executables for Python/imported code'
    }
    foreach ($collection in $policy.AppLockerPolicy.RuleCollection) {
        foreach ($rule in $collection.FileHashRule) {
            $hash = $rule.Conditions.FileHashCondition.FileHash
            [pscustomobject]@{ collection=$collection.Type; name=$file.Name;
                length=[long]$hash.SourceFileLength;
                applocker_hash=([string]$hash.Data -replace '^0x','').ToLowerInvariant();
                raw_sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
        }
    }
}
ConvertTo-Json -InputObject @($rows) -Depth 4 -Compress
