param(
    [Parameter(Mandatory = $true)]
    [string]$Message,

    [string]$RemoteHost = "ubuntu@124.220.233.126",

    [string]$GroupId = "689863409",

    [string]$Source = "mortis-ai"
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Message)) {
    throw "Message cannot be empty."
}

$messageB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Message))
$sourceB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Source))

$remoteCommand = @"
python3 /home/ubuntu/multica-public-watch/control/send_napcat_group.py --group-id '$GroupId' --message-b64 '$messageB64' --source-b64 '$sourceB64'
"@

Write-Host "Sending whitelisted NapCat group message to group $GroupId via $RemoteHost..."
$result = & ssh $RemoteHost $remoteCommand
if ($LASTEXITCODE -ne 0) {
    throw "Remote NapCat send failed with exit code $LASTEXITCODE."
}

if ($result) {
    $result
}
