#!/usr/bin/env python3
"""
Script to create a complete book from all chapters using pypandoc
"""

import os
import glob
from pathlib import Path

def read_file_content(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def create_complete_book():
    """Create a complete book by combining all chapters"""
    
    # Book header
    book_content = """# 📘 Professional Guide – Building Voice AI Systems for Call Centers

## From IVR to Conversational AI

A comprehensive technical guide for developers, architects, and technical managers building modern voice AI solutions for contact centers.

---

## 🎯 Target Audience

- **Developers & Integrators** who design and deploy call center solutions  
- **Solution Architects** looking to integrate Text-to-Speech (TTS), Speech-to-Text (STT), and AI  
- **Technical Managers** who want to evaluate and modernize their customer service infrastructure  

---

## 📑 Table of Contents

### Part I – Foundations of Voice AI
1. Introduction to Voice Synthesis  
2. Natural Language Processing in Call Centers  

### Part II – Technical Implementation
3. Integration with Telephony Systems  
4. Best Practices in Conversational Design  
5. Modern IVR Scripts – From Static to AI-driven  

### Part III – Operations and Monitoring
6. Monitoring, Logging, and Analytics  
7. Advanced Voice AI Features  
8. Security and Compliance in Voice Applications  

### Part IV – Future and Scalability
9. The Future of Voice AI in Contact Centers  
10. Scalability and Cloud-Native Voice Architectures  

---

"""
    
    # Get all chapter directories sorted by number
    chapters_dir = Path("chapters")
    chapter_dirs = sorted(
        [d for d in chapters_dir.iterdir() if d.is_dir() and d.name.startswith("chapter")],
        key=lambda x: int(x.name.replace("chapter", ""))
    )
    
    print(f"Found {len(chapter_dirs)} chapters")
    
    # Add each chapter content
    for chapter_dir in chapter_dirs:
        chapter_num = chapter_dir.name.replace("chapter", "")
        readme_path = chapter_dir / "README.md"
        
        if readme_path.exists():
            print(f"Processing {chapter_dir.name}...")
            chapter_content = read_file_content(readme_path)
            
            # Add chapter separator
            book_content += f"\n\n---\n\n"
            book_content += chapter_content
            book_content += f"\n\n---\n\n"
        else:
            print(f"Warning: No README.md found in {chapter_dir}")
    
    # Add book footer
    book_content += """
# 📦 Deliverables and Resources  

- **Code Repository**: Ready-to-use integration examples  
- **API Playbooks**: Quick-start guides for Azure, Amazon, Twilio  
- **IVR Templates**: Customizable scripts for different industries  
- **Architecture Diagrams**: Sample deployment models for enterprises  

---

# 🚀 Quick Start  

```bash
# Clone the repository
git clone <repository-url>
cd voice-ai-call-centers

# Install dependencies
pip install -r requirements.txt

# Run examples
python examples/basic_tts_demo.py
```

# 📊 Technology Stack

- **TTS Platforms**: Microsoft Azure, Amazon Polly, Google Cloud TTS, OpenAI
- **STT Platforms**: Azure Speech Services, Amazon Transcribe, Google Speech-to-Text
- **Telephony**: Twilio, Asterisk, Genesys Cloud, Amazon Connect
- **NLP/LLM**: OpenAI GPT, Azure OpenAI, Amazon Bedrock
- **Languages**: Python, Node.js, JavaScript

# 🤝 Contributing

This guide is designed to be a living document. Contributions are welcome!

---

*Generated on: """ + str(Path().cwd()) + """*
"""
    
    # Write the complete book
    output_file = "complete_voice_ai_guide.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(book_content)
    
    print(f"\nComplete book written to: {output_file}")
    
    # Try to convert to PDF using pypandoc if available
    try:
        import pypandoc
        
        print("\nConverting to PDF using pypandoc...")
        # First create HTML
        output = pypandoc.convert_file(
            output_file, 
            'html', 
            outputfile='complete_voice_ai_guide.html',
            extra_args=['--toc', '--number-sections', '--standalone']
        )
        print("HTML created successfully: complete_voice_ai_guide.html")
        
        # Try to create PDF with weasyprint
        try:
            output = pypandoc.convert_file(
                output_file, 
                'pdf', 
                outputfile='complete_voice_ai_guide.pdf',
                extra_args=['--toc', '--number-sections', '--pdf-engine=weasyprint']
            )
            print("PDF created successfully: complete_voice_ai_guide.pdf")
        except Exception as pdf_error:
            print(f"PDF conversion with weasyprint failed: {pdf_error}")
            print("You can open complete_voice_ai_guide.html in a browser and print to PDF")
        
    except ImportError:
        print("\nPypandoc not available. Install with: pip install pypandoc")
        print("Or convert manually using pandoc:")
        print(f"pandoc {output_file} -o complete_voice_ai_guide.pdf --toc --number-sections")
    
    except Exception as e:
        print(f"\nError converting to PDF: {e}")
        print("You can still use the markdown file or convert manually with pandoc")
    
    return output_file

if __name__ == "__main__":
    book_file = create_complete_book()
    print(f"\nBook creation completed! Main file: {book_file}")
