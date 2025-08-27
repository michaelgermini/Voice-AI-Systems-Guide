#!/usr/bin/env python3
"""
Script to convert the HTML guide to PDF using weasyprint
"""

import os
from pathlib import Path

def create_pdf_from_html():
    """Convert the HTML guide to PDF using weasyprint"""
    
    html_file = "complete_voice_ai_guide.html"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML file not found: {html_file}")
        print("Please run create_book.py first to generate the HTML file")
        return False
    
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        print("🔄 Converting HTML to PDF using weasyprint...")
        
        # Configure fonts
        font_config = FontConfiguration()
        
        # Create PDF from HTML
        HTML(filename=html_file).write_pdf(
            'complete_voice_ai_guide.pdf',
            font_config=font_config
        )
        
        print("✅ PDF created successfully: complete_voice_ai_guide.pdf")
        return True
        
    except ImportError:
        print("❌ Weasyprint not installed. Install with: pip install weasyprint")
        return False
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print(" PDF GENERATION - VOICE AI SYSTEMS GUIDE")
    print("=" * 60)
    
    success = create_pdf_from_html()
    
    if success:
        print("\n🎉 PDF generation completed!")
        print("📄 File: complete_voice_ai_guide.pdf")
    else:
        print("\n💡 Alternative: Open complete_voice_ai_guide.html in your browser")
        print("   and use Ctrl+P to print to PDF")

if __name__ == "__main__":
    main()
