#!/usr/bin/env python3
"""
SSML Script Generator - Chapter 4
Demonstrates how to create natural-sounding TTS scripts with SSML markup.
"""

import os
import time
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SSMLScript:
    """Represents an SSML script with metadata"""
    name: str
    text: str
    ssml: str
    voice: str
    duration_estimate: float
    complexity_score: int

class SSMLScriptGenerator:
    """Generates natural-sounding SSML scripts for TTS"""
    
    def __init__(self):
        # Define voice options
        self.voices = {
            "en-US": {
                "female": ["Polly.Joanna", "Polly.Salli", "Polly.Kendra"],
                "male": ["Polly.Matthew", "Polly.Justin", "Polly.Kevin"]
            },
            "en-GB": {
                "female": ["Polly.Amy", "Polly.Emma"],
                "male": ["Polly.Brian", "Polly.Arthur"]
            }
        }
        
        # Define SSML templates
        self.templates = {
            "greeting": {
                "name": "Friendly Greeting",
                "text": "Welcome to ACME Bank. How can I help you today?",
                "ssml": '<speak>Welcome to <emphasis level="moderate">ACME Bank</emphasis>. <break time="300ms"/> How can I help you today?</speak>'
            },
            "balance_check": {
                "name": "Balance Check Response",
                "text": "Your account balance is $2,456.78.",
                "ssml": '<speak>Your account balance is <break time="400ms"/> <say-as interpret-as="currency">2456.78</say-as>.</speak>'
            },
            "confirmation": {
                "name": "Information Confirmation",
                "text": "Did you say order number 1-2-3-4-5?",
                "ssml": '<speak>Did you say order number <break time="200ms"/> <say-as interpret-as="digits">12345</say-as>?</speak>'
            },
            "error_recovery": {
                "name": "Error Recovery",
                "text": "I didn't quite get that. You can say things like 'track my order', 'technical support', or 'billing questions'.",
                "ssml": '<speak>I didn\'t quite get that. <break time="300ms"/> You can say things like <emphasis level="moderate">track my order</emphasis>, <emphasis level="moderate">technical support</emphasis>, or <emphasis level="moderate">billing questions</emphasis>.</speak>'
            },
            "escalation": {
                "name": "Graceful Escalation",
                "text": "I understand this is important. Let me connect you with a specialist who can better assist you.",
                "ssml": '<speak>I understand this is <emphasis level="strong">important</emphasis>. <break time="400ms"/> Let me connect you with a specialist who can better assist you.</speak>'
            },
            "closing": {
                "name": "Natural Closing",
                "text": "Great! Thank you for calling ACME Bank. Have a wonderful day.",
                "ssml": '<speak><emphasis level="moderate">Great!</emphasis> <break time="300ms"/> Thank you for calling <emphasis level="moderate">ACME Bank</emphasis>. <break time="200ms"/> Have a wonderful day.</speak>'
            }
        }
        
        # Define SSML elements and their usage
        self.ssml_elements = {
            "break": {
                "description": "Add pauses for natural pacing",
                "examples": [
                    '<break time="200ms"/>',
                    '<break time="500ms"/>',
                    '<break strength="weak"/>',
                    '<break strength="medium"/>',
                    '<break strength="strong"/>'
                ]
            },
            "emphasis": {
                "description": "Add emphasis to important words",
                "examples": [
                    '<emphasis level="reduced">whisper</emphasis>',
                    '<emphasis level="moderate">normal emphasis</emphasis>',
                    '<emphasis level="strong">strong emphasis</emphasis>'
                ]
            },
            "say-as": {
                "description": "Control pronunciation of numbers, dates, etc.",
                "examples": [
                    '<say-as interpret-as="digits">12345</say-as>',
                    '<say-as interpret-as="currency">2456.78</say-as>',
                    '<say-as interpret-as="date">2024-01-15</say-as>',
                    '<say-as interpret-as="time">14:30</say-as>'
                ]
            },
            "prosody": {
                "description": "Control speech rate, pitch, and volume",
                "examples": [
                    '<prosody rate="slow">speak slowly</prosody>',
                    '<prosody pitch="high">speak in high pitch</prosody>',
                    '<prosody volume="loud">speak loudly</prosody>'
                ]
            },
            "phoneme": {
                "description": "Control exact pronunciation",
                "examples": [
                    '<phoneme alphabet="ipa" ph="tomeito">tomato</phoneme>',
                    '<phoneme alphabet="ipa" ph="karamel">caramel</phoneme>'
                ]
            }
        }

    def generate_ssml_from_text(self, text: str, voice: str = "Polly.Joanna", 
                               add_pauses: bool = True, add_emphasis: bool = True) -> str:
        """Generate SSML from plain text"""
        ssml = text
        
        # Add pauses for natural pacing
        if add_pauses:
            ssml = self.add_natural_pauses(ssml)
        
        # Add emphasis to important words
        if add_emphasis:
            ssml = self.add_emphasis(ssml)
        
        # Convert numbers and special formats
        ssml = self.convert_special_formats(ssml)
        
        # Wrap in speak tags
        ssml = f'<speak>{ssml}</speak>'
        
        return ssml

    def add_natural_pauses(self, text: str) -> str:
        """Add natural pauses to text"""
        # Add pauses after punctuation
        text = re.sub(r'([.!?])\s+', r'\1 <break time="300ms"/> ', text)
        
        # Add pauses before important information
        text = re.sub(r'(\$[\d,]+\.?\d*)', r'<break time="400ms"/> \1', text)
        
        # Add pauses before lists
        text = re.sub(r'(\w+), (\w+), or (\w+)', r'\1, <break time="200ms"/> \2, or <break time="200ms"/> \3', text)
        
        # Add pauses for emphasis
        text = re.sub(r'(Thank you|Great|Perfect)', r'\1 <break time="300ms"/>', text)
        
        return text

    def add_emphasis(self, text: str) -> str:
        """Add emphasis to important words"""
        # Emphasize company names
        text = re.sub(r'\b(ACME|Bank|Corporation)\b', r'<emphasis level="moderate">\1</emphasis>', text, flags=re.IGNORECASE)
        
        # Emphasize important words
        important_words = ['important', 'urgent', 'critical', 'balance', 'account', 'order']
        for word in important_words:
            text = re.sub(rf'\b{word}\b', r'<emphasis level="moderate">' + word + r'</emphasis>', text, flags=re.IGNORECASE)
        
        # Emphasize numbers
        text = re.sub(r'(\$[\d,]+\.?\d*)', r'<emphasis level="moderate">\1</emphasis>', text)
        
        return text

    def convert_special_formats(self, text: str) -> str:
        """Convert special formats to SSML say-as tags"""
        # Convert currency
        text = re.sub(r'\$([\d,]+\.?\d*)', r'<say-as interpret-as="currency">\1</say-as>', text)
        
        # Convert phone numbers
        text = re.sub(r'(\d{3})-(\d{3})-(\d{4})', r'<say-as interpret-as="telephone">\1\2\3</say-as>', text)
        
        # Convert account numbers (4+ digits)
        text = re.sub(r'\b(\d{4,})\b', r'<say-as interpret-as="digits">\1</say-as>', text)
        
        # Convert dates
        text = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'<say-as interpret-as="date">\1-\2-\3</say-as>', text)
        
        return text

    def create_conversation_script(self, conversation_turns: List[Dict], 
                                 voice: str = "Polly.Joanna") -> List[SSMLScript]:
        """Create SSML scripts for a complete conversation"""
        scripts = []
        
        for i, turn in enumerate(conversation_turns):
            if turn["speaker"] == "AI":
                # Generate SSML for AI responses
                ssml = self.generate_ssml_from_text(turn["text"], voice)
                
                script = SSMLScript(
                    name=f"Turn {i+1} - AI Response",
                    text=turn["text"],
                    ssml=ssml,
                    voice=voice,
                    duration_estimate=len(turn["text"]) * 0.06,  # Rough estimate: 60ms per character
                    complexity_score=self.calculate_complexity(ssml)
                )
                scripts.append(script)
        
        return scripts

    def calculate_complexity(self, ssml: str) -> int:
        """Calculate complexity score of SSML (1-10)"""
        complexity = 1
        
        # Add complexity for each SSML element
        if "<break" in ssml:
            complexity += 1
        if "<emphasis" in ssml:
            complexity += 2
        if "<say-as" in ssml:
            complexity += 2
        if "<prosody" in ssml:
            complexity += 3
        if "<phoneme" in ssml:
            complexity += 4
        
        # Add complexity for length
        if len(ssml) > 500:
            complexity += 2
        elif len(ssml) > 200:
            complexity += 1
        
        return min(10, complexity)

    def generate_template_script(self, template_name: str, 
                               voice: str = "Polly.Joanna") -> SSMLScript:
        """Generate SSML script from a template"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        
        return SSMLScript(
            name=template["name"],
            text=template["text"],
            ssml=template["ssml"],
            voice=voice,
            duration_estimate=len(template["text"]) * 0.06,
            complexity_score=self.calculate_complexity(template["ssml"])
        )

    def print_ssml_guide(self):
        """Print SSML usage guide"""
        print(f"\n{'='*80}")
        print("SSML ELEMENTS GUIDE")
        print(f"{'='*80}")
        
        for element, info in self.ssml_elements.items():
            print(f"\n{element.upper()}:")
            print(f"   Description: {info['description']}")
            print(f"   Examples:")
            for example in info['examples']:
                print(f"     {example}")

    def print_script_analysis(self, script: SSMLScript):
        """Print detailed analysis of an SSML script"""
        print(f"\n{'='*80}")
        print(f"SSML SCRIPT: {script.name}")
        print(f"{'='*80}")
        
        print(f"\nVoice: {script.voice}")
        print(f"Duration Estimate: {script.duration_estimate:.1f} seconds")
        print(f"Complexity Score: {script.complexity_score}/10")
        
        print(f"\nPlain Text:")
        print(f"   '{script.text}'")
        
        print(f"\nSSML Markup:")
        print(f"   {script.ssml}")
        
        # Analyze SSML elements used
        elements_used = []
        if "<break" in script.ssml:
            elements_used.append("break")
        if "<emphasis" in script.ssml:
            elements_used.append("emphasis")
        if "<say-as" in script.ssml:
            elements_used.append("say-as")
        if "<prosody" in script.ssml:
            elements_used.append("prosody")
        if "<phoneme" in script.ssml:
            elements_used.append("phoneme")
        
        print(f"\nSSML Elements Used: {', '.join(elements_used) if elements_used else 'None'}")

    def run_demo(self):
        """Run the SSML script generator demo"""
        print("SSML Script Generator - Chapter 4")
        print("="*80)
        print("Demonstrating natural-sounding TTS script generation...")
        
        # Print SSML guide
        self.print_ssml_guide()
        
        # Generate scripts from templates
        print(f"\n{'='*80}")
        print("GENERATING SCRIPTS FROM TEMPLATES")
        print(f"{'='*80}")
        
        for template_name in self.templates.keys():
            script = self.generate_template_script(template_name)
            self.print_script_analysis(script)
        
        # Generate custom conversation script
        print(f"\n{'='*80}")
        print("GENERATING CUSTOM CONVERSATION SCRIPT")
        print(f"{'='*80}")
        
        conversation = [
            {"speaker": "Customer", "text": "I want to check my account balance"},
            {"speaker": "AI", "text": "I can help you check your balance. For security, I'll need to verify your identity. What's the last 4 digits of your social security number?"},
            {"speaker": "Customer", "text": "1234"},
            {"speaker": "AI", "text": "Did you say 1-2-3-4?"},
            {"speaker": "Customer", "text": "Yes"},
            {"speaker": "AI", "text": "Thank you. Your account balance is $2,456.78. Is there anything else I can help you with today?"}
        ]
        
        scripts = self.create_conversation_script(conversation)
        
        for script in scripts:
            self.print_script_analysis(script)
        
        # Summary
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        
        print(f"\nKey SSML Techniques:")
        print(f"   • Use <break> for natural pacing and pauses")
        print(f"   • Use <emphasis> to highlight important information")
        print(f"   • Use <say-as> for proper pronunciation of numbers and dates")
        print(f"   • Use <prosody> to control speech rate and pitch")
        print(f"   • Keep complexity manageable for better TTS quality")
        
        print(f"\nBest Practices:")
        print(f"   • Add pauses before important information")
        print(f"   • Emphasize company names and key terms")
        print(f"   • Use proper number formatting for currency and account numbers")
        print(f"   • Test scripts with actual TTS engines")
        print(f"   • Keep SSML complexity under control")
        
        print(f"\nSSML script generator demo completed!")
        print("   Remember: Natural pacing and emphasis make TTS sound more human.")

if __name__ == "__main__":
    generator = SSMLScriptGenerator()
    generator.run_demo()
