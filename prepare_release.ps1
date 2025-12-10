# Prepare a release zip excluding secrets and unneeded files
$releaseName = "automacao_de_listas_release_$(Get-Date -Format yyyyMMdd_HHmmss).zip"
$excludes = @('.git','.venv','pessoas_geradas','Relatorios','client_secrets.json','credentials.json','logs')
$items = Get-ChildItem -Path . -Force | Where-Object { $excludes -notcontains $_.Name }

$tempDir = Join-Path $env:TEMP "release_pack_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $tempDir | Out-Null

foreach ($item in $items) {
    $dest = Join-Path $tempDir $item.Name
    if ($item.PSIsContainer) { Copy-Item $item.FullName -Destination $dest -Recurse -Force }
    else { Copy-Item $item.FullName -Destination $dest -Force }
}

Compress-Archive -Path (Join-Path $tempDir '*') -DestinationPath $releaseName
Write-Host "Release prepared: $releaseName"
