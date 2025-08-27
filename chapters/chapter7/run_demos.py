#!/usr/bin/env python3
"""
Chapter 7 Demo Runner
Executes all Chapter 7 demonstration scripts for Advanced Voice AI Features.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def run_demo_script(script_path: str, script_name: str) -> bool:
    """Run a single demo script and return success status"""
    print(f"\n{'='*80}")
    print(f"Running {script_name}")
    print(f"{'='*80}")
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Script completed successfully!")
            print("\nOutput:")
            print(result.stdout)
            return True
        else:
            print("Script failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Script timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error running script: {e}")
        return False

def main():
    """Main function to run all Chapter 7 demos"""
    print("Chapter 7: Advanced Voice AI Features")
    print("="*80)
    print("This will run all Chapter 7 demonstration scripts:")
    print("1. Emotion Detection System - Real-time emotion recognition")
    print("2. Voice Biometric System - Speaker identification and verification")
    print("3. Multilingual Voice AI - Language detection and translation")
    print("4. Advanced Context Manager - Conversational memory and context")
    print("5. Predictive Intent System - Intent prediction and proactive assistance")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/emotion_detection.py", "Emotion Detection System"),
    ]
    
    # Track results
    results = []
    start_time = time.time()
    
    # Run each demo
    for script_path, script_name in demos:
        if os.path.exists(script_path):
            success = run_demo_script(script_path, script_name)
            results.append((script_name, success))
        else:
            print(f"Script not found: {script_path}")
            results.append((script_name, False))
    
    # Print summary
    total_time = time.time() - start_time
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n{'='*80}")
    print("CHAPTER 7 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\nChapter 7 Key Concepts Demonstrated:")
    print("   • Real-time emotion detection from voice")
    print("   • Audio feature extraction and analysis")
    print("   • Emotion-aware response generation")
    print("   • Automatic escalation based on emotional state")
    print("   • Multi-emotion classification with confidence scores")
    print("   • Adaptive IVR responses based on customer emotions")
    
    print(f"\nAdvanced Voice AI Capabilities:")
    print("   • Emotion Detection: Recognize customer emotions from voice")
    print("   • Voice Biometrics: Secure speaker identification and verification")
    print("   • Multilingual Support: Language detection and translation")
    print("   • Context Management: Conversational memory and context retention")
    print("   • Predictive Intent: Proactive assistance and intent prediction")
    print("   • Cultural Adaptation: Region-specific response customization")
    
    print(f"\nProduction Benefits:")
    print("   • Reduced Escalation Rates: Handle emotional situations intelligently")
    print("   • Improved Security: Voice biometrics for fraud prevention")
    print("   • Global Reach: Serve customers in their preferred language")
    print("   • Enhanced Personalization: Context-aware, adaptive responses")
    print("   • Proactive Service: Predict and suggest next actions")
    print("   • Better Customer Experience: Emotionally intelligent interactions")
    
    print(f"\nImplementation Considerations:")
    print("   • Privacy and Consent: Clear user consent for advanced features")
    print("   • Bias Detection: Monitor for bias in emotion detection")
    print("   • Performance Optimization: Parallel processing for real-time analysis")
    print("   • Fallback Mechanisms: Graceful degradation when features fail")
    print("   • Cultural Sensitivity: Respect regional and cultural differences")
    print("   • Security Compliance: Secure handling of voice biometric data")
    
    print(f"\nNext Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Implement advanced features in your voice AI systems")
    print("   • Ensure privacy and security compliance")
    print("   • Test with diverse user populations")
    print("   • Monitor performance and user feedback")
    print("   • Move to Chapter 8 for deployment and scaling strategies")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
