# Script pour exécuter tous les tests
Write-Host "=" -NoNewline; Write-Host ("="*80)
Write-Host "TESTS DE COMPTAGE DE COLIS SUR PALETTES"
Write-Host "=" -NoNewline; Write-Host ("="*80)

$pythonExe = "C:/Users/PAVILION/Documents/FRESH DATA/Comptage colis 2/.venv/Scripts/python.exe"
$projectRoot = "C:\Users\PAVILION\Documents\FRESH DATA\Comptage colis 2"

# Test Solution 2 - OpenCV (le plus rapide)
Write-Host "`n[1/4] Test Solution OpenCV (Vision classique)..." -ForegroundColor Cyan
& $pythonExe "$projectRoot\Solution_2_OpenCV\detect_contours.py"

# Test Solution 3 - DETR
Write-Host "`n[2/4] Test Solution DETR (Modèle pré-entraîné)..." -ForegroundColor Cyan
Write-Host "Installation des dépendances DETR..." -ForegroundColor Yellow
pip install transformers torch pillow timm
& $pythonExe "$projectRoot\Solution_3_Pretrained\detr_detection.py"

# Test LLM - uniquement si les clés API sont configurées
Write-Host "`n[3/4] Tests LLM Vision..." -ForegroundColor Cyan

if ($env:OPENAI_API_KEY) {
    Write-Host "Test ChatGPT..." -ForegroundColor Green
    pip install openai
    & $pythonExe "$projectRoot\Tests_LLM_Vision\test_chatgpt.py"
} else {
    Write-Host "Clé OPENAI_API_KEY non configurée - Test ChatGPT ignoré" -ForegroundColor Yellow
}

if ($env:GOOGLE_API_KEY) {
    Write-Host "Test Gemini..." -ForegroundColor Green
    pip install google-generativeai
    & $pythonExe "$projectRoot\Tests_LLM_Vision\test_gemini.py"
} else {
    Write-Host "Clé GOOGLE_API_KEY non configurée - Test Gemini ignoré" -ForegroundColor Yellow
}

if ($env:MISTRAL_API_KEY) {
    Write-Host "Test Mistral..." -ForegroundColor Green
    pip install mistralai
    & $pythonExe "$projectRoot\Tests_LLM_Vision\test_mistral.py"
} else {
    Write-Host "Clé MISTRAL_API_KEY non configurée - Test Mistral ignoré" -ForegroundColor Yellow
}

# Comparaison finale
Write-Host "`n[4/4] Comparaison des résultats..." -ForegroundColor Cyan
pip install pandas
& $pythonExe "$projectRoot\Tests_LLM_Vision\compare_results.py"

Write-Host "`n" -NoNewline; Write-Host ("="*80)
Write-Host "TESTS TERMINÉS!" -ForegroundColor Green
Write-Host "Consultez les résultats dans le dossier 'results/'" -ForegroundColor Green
Write-Host ("="*80)
