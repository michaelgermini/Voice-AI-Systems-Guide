#!/usr/bin/env python3
"""
Chapter 2 - Natural Language Processing in Call Centers
Demo Runner
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def run_demo_script(script_name: str, description: str) -> bool:
    """Run a demo script and return success status"""
    
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    
    script_path = os.path.join("examples", script_name)
    
    if not os.path.exists(script_path):
        print(f"[ERROR] Script not found: {script_path}")
        return False
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed successfully")
            return True
        else:
            print(f"[FAILED] {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error running {description}: {str(e)}")
        return False

def main():
    """Run all Chapter 2 demos"""
    
    print("=" * 80)
    print("CHAPTER 2 - NATURAL LANGUAGE PROCESSING IN CALL CENTERS")
    print("DEMO RUNNER")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of demos to run
    demos = [
        ("intent_recognition_demo.py", "Intent Recognition Demo"),
        ("entity_extraction_demo.py", "Entity Extraction Demo"),
        ("conversation_flow_demo.py", "Conversation Flow Demo"),
        ("llm_integration_demo.py", "LLM Integration Demo")
    ]
    
    successful_demos = 0
    total_demos = len(demos)
    
    print(f"\nRunning {total_demos} demos...")
    
    for script_name, description in demos:
        success = run_demo_script(script_name, description)
        if success:
            successful_demos += 1
        
        # Brief pause between demos
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 80)
    print("CHAPTER 2 DEMO SUMMARY")
    print("=" * 80)
    print(f"Total Demos: {total_demos}")
    print(f"Successful: {successful_demos}")
    print(f"Failed: {total_demos - successful_demos}")
    print(f"Success Rate: {(successful_demos/total_demos)*100:.1f}%")
    
    if successful_demos == total_demos:
        print("\n[SUCCESS] All Chapter 2 demos completed successfully!")
    else:
        print(f"\n[WARNING] {total_demos - successful_demos} demo(s) failed. Check the output above for details.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
