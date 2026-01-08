import json
from pathlib import Path
import pandas as pd

def compare_all_methods():
    """Comparer les résultats de toutes les méthodes"""
    # Obtenir le chemin absolu
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    results_folder = project_root / 'results'
    
    # Charger tous les résultats
    methods = {
        'YOLOv8': 'yolov8_results/results.json',
        'OpenCV': 'opencv_results/results.json',
        'DETR': 'pretrained_results/detr_results.json',
        'Mistral': 'llm_results/mistral_results.json',
        'ChatGPT': 'llm_results/chatgpt_results.json',
        'Gemini': 'llm_results/gemini_results.json'
    }
    
    data = []
    available_methods = []
    
    for method_name, result_file in methods.items():
        file_path = results_folder / result_file
        if file_path.exists():
            available_methods.append(method_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                    
                for img_name, result in results.items():
                    detected = result.get('detected')
                    expected = result.get('expected')
                    
                    if detected is not None and expected is not None:
                        data.append({
                            'Image': img_name,
                            'Méthode': method_name,
                            'Détecté': detected,
                            'Attendu': expected,
                            'Erreur': abs(detected - expected)
                        })
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de {method_name}: {e}")
        else:
            print(f"⚠️ Résultats non disponibles pour {method_name}")
    
    if not data:
        print("❌ Aucun résultat disponible à comparer")
        print("\nExécutez d'abord les scripts de test:")
        print("  - python Solution_2_OpenCV/detect_contours.py")
        print("  - python Tests_LLM_Vision/test_chatgpt.py")
        print("  - python Tests_LLM_Vision/test_mistral.py")
        print("  - python Tests_LLM_Vision/test_gemini.py")
        return None
    
    # Créer un DataFrame
    df = pd.DataFrame(data)
    
    # Tableau pivot
    pivot = df.pivot_table(
        values='Détecté',
        index='Image',
        columns='Méthode',
        aggfunc='first'
    )
    pivot['Attendu'] = df.groupby('Image')['Attendu'].first()
    
    print("\n" + "="*100)
    print("COMPARAISON DE TOUTES LES MÉTHODES")
    print("="*100)
    print(pivot.to_string())
    
    # Statistiques par méthode
    print("\n" + "="*100)
    print("PRÉCISION PAR MÉTHODE")
    print("="*100)
    
    for method in available_methods:
        method_data = df[df['Méthode'] == method]
        if not method_data.empty:
            erreur_moyenne = method_data['Erreur'].mean()
            erreur_max = method_data['Erreur'].max()
            precision_parfaite = (method_data['Erreur'] == 0).sum() / len(method_data) * 100
            
            print(f"\n{method}:")
            print(f"  - Erreur moyenne: {erreur_moyenne:.2f}")
            print(f"  - Erreur maximale: {erreur_max}")
            print(f"  - Précision parfaite: {precision_parfaite:.1f}%")
    
    # Sauvegarder le rapport
    report_path = results_folder / 'comparison_report.csv'
    pivot.to_csv(report_path)
    print(f"\n✅ Rapport sauvegardé dans: {report_path}")
    
    # Créer un résumé JSON
    summary = {
        'methods_tested': available_methods,
        'total_images': len(pivot),
        'method_stats': {}
    }
    
    for method in available_methods:
        method_data = df[df['Méthode'] == method]
        if not method_data.empty:
            summary['method_stats'][method] = {
                'erreur_moyenne': float(method_data['Erreur'].mean()),
                'erreur_max': int(method_data['Erreur'].max()),
                'precision_parfaite': float((method_data['Erreur'] == 0).sum() / len(method_data) * 100)
            }
    
    summary_path = results_folder / 'summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Résumé JSON sauvegardé dans: {summary_path}")
    
    return pivot

if __name__ == "__main__":
    print("="*100)
    print("COMPARAISON DES MÉTHODES DE COMPTAGE")
    print("="*100)
    
    comparison = compare_all_methods()
