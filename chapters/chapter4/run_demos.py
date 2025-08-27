#!/usr/bin/env python3
"""
Chapter 4 Demo Runner
Executes all Chapter 4 demonstration scripts for Conversational Design Best Practices.
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
    """Main function to run all Chapter 4 demos"""
    print("Chapter 4: Conversational Design Best Practices")
    print("="*80)
    print("This will run all Chapter 4 demonstration scripts:")
    print("1. Conversational Design Patterns Demo")
    print("2. SSML Script Generator")
    print("3. Call Flow Designer")
    print("4. Conversation Analyzer")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/conversational_patterns_demo.py", "Conversational Design Patterns Demo"),
        ("examples/ssml_script_generator.py", "SSML Script Generator"),
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
    print("CHAPTER 4 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\nChapter 4 Key Concepts Demonstrated:")
    print("   • Conversational Design: Good vs bad conversation patterns")
    print("   • SSML Scripting: Natural-sounding TTS with proper pacing")
    print("   • Design Principles: Clarity, context retention, error handling")
    print("   • Best Practices: Human-like turn-taking and natural language")
    
    print(f"\nNext Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Practice writing conversational scripts")
    print("   • Test SSML with actual TTS engines")
    print("   • Move to Chapter 5 for advanced voice AI features")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
