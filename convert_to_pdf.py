#!/usr/bin/env python3
"""
Script pour convertir le guide en PDF
"""

import os
import webbrowser
from pathlib import Path

def main():
    """Convertir le guide en PDF"""
    
    print("=" * 60)
    print("CONVERSION DU GUIDE EN PDF")
    print("=" * 60)
    
    # Vérifier les fichiers disponibles
    files = {
        "markdown": "complete_voice_ai_guide.md",
        "html": "complete_voice_ai_guide.html"
    }
    
    print("\nFichiers disponibles:")
    for file_type, filename in files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {file_type.upper()}: {filename} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_type.upper()}: {filename} (manquant)")
    
    print("\n" + "=" * 60)
    print("OPTIONS DE CONVERSION")
    print("=" * 60)
    
    print("\n1. 📄 Ouvrir le fichier HTML dans le navigateur")
    print("   - Le fichier HTML s'ouvrira automatiquement")
    print("   - Utilisez Ctrl+P pour imprimer en PDF")
    print("   - Recommandé pour un meilleur rendu")
    
    print("\n2. 🔧 Conversion automatique (si pandoc disponible)")
    print("   - Tentative de conversion directe en PDF")
    print("   - Nécessite un moteur PDF installé")
    
    print("\n3. 📖 Aperçu du contenu")
    print("   - Afficher les premières lignes du guide")
    
    choice = input("\nChoisissez une option (1-3): ").strip()
    
    if choice == "1":
        print("\nOuverture du fichier HTML...")
        html_file = Path("complete_voice_ai_guide.html").absolute()
        webbrowser.open(f"file://{html_file}")
        print("✅ Fichier HTML ouvert dans le navigateur")
        print("💡 Utilisez Ctrl+P pour imprimer en PDF")
        
    elif choice == "2":
        print("\nTentative de conversion automatique...")
        try:
            import pypandoc
            output = pypandoc.convert_file(
                "complete_voice_ai_guide.md",
                'pdf',
                outputfile='complete_voice_ai_guide.pdf',
                extra_args=['--toc', '--number-sections']
            )
            print("✅ PDF créé avec succès: complete_voice_ai_guide.pdf")
        except Exception as e:
            print(f"❌ Erreur de conversion: {e}")
            print("💡 Essayez l'option 1 (HTML + navigateur)")
            
    elif choice == "3":
        print("\nAperçu du contenu:")
        print("-" * 40)
        try:
            with open("complete_voice_ai_guide.md", 'r', encoding='utf-8') as f:
                lines = f.readlines()[:20]
                for line in lines:
                    print(line.rstrip())
            print("...")
            print(f"📊 Total: {sum(1 for line in open('complete_voice_ai_guide.md', 'r', encoding='utf-8'))} lignes")
        except Exception as e:
            print(f"❌ Erreur de lecture: {e}")
    
    else:
        print("❌ Option invalide")
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS POUR PDF")
    print("=" * 60)
    print("\n📋 Pour créer un PDF parfait:")
    print("1. Ouvrez complete_voice_ai_guide.html dans votre navigateur")
    print("2. Appuyez sur Ctrl+P (ou Cmd+P sur Mac)")
    print("3. Choisissez 'Enregistrer en PDF'")
    print("4. Sélectionnez 'A4' et 'Portrait'")
    print("5. Activez 'En-têtes et pieds de page' si souhaité")
    print("6. Cliquez sur 'Enregistrer'")
    
    print(f"\n📁 Fichiers dans le répertoire: {Path().cwd()}")

if __name__ == "__main__":
    main()
