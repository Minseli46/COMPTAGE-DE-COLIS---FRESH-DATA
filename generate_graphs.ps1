Write-Host "Génération des graphiques..." -ForegroundColor Cyan

$pythonExe = "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2\.venv\Scripts\python.exe"
$scriptPath = "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2\generate_visualizations.py"

& $pythonExe $scriptPath

Write-Host "`nVérification des fichiers générés..." -ForegroundColor Yellow
Get-ChildItem "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2\results\visualizations\*.png" -ErrorAction SilentlyContinue

Write-Host "`n✅ Terminé! Ouvrez le dossier:" -ForegroundColor Green
Write-Host "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2\results\visualizations" -ForegroundColor Cyan
