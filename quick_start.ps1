# Script de démarrage rapide - Test OpenCV uniquement
Write-Host "=" -NoNewline; Write-Host ("="*60)
Write-Host "TEST RAPIDE - Solution OpenCV"
Write-Host "=" -NoNewline; Write-Host ("="*60)

$pythonExe = "C:/Users/PAVILION/Documents/FRESH DATA/Comptage colis 2/.venv/Scripts/python.exe"
$scriptPath = "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2\Solution_2_OpenCV\detect_contours.py"

Write-Host "`nLancement de la détection OpenCV..." -ForegroundColor Cyan
& $pythonExe $scriptPath

Write-Host "`n" -NoNewline; Write-Host ("="*60)
Write-Host "Les images annotées sont dans: results/opencv_results/" -ForegroundColor Green
Write-Host ("="*60)
