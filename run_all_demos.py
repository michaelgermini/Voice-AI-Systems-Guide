#!/usr/bin/env python3
"""
Run All Demos - Voice AI Systems Guide

This script runs all demo scripts from all chapters to verify
the complete functionality of the voice AI systems guide.

Usage:
    python run_all_demos.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")

def run_demo(chapter_path, chapter_name):
    """Run the demo script for a specific chapter."""
    demo_script = chapter_path / "run_demos.py"
    
    if not demo_script.exists():
        print(f"[WARNING] No demo script found for {chapter_name}")
        return False
    
    print_section(f"Running {chapter_name} Demos")
    print(f"Path: {demo_script}")
    
    try:
        # Change to chapter directory and run demo
        original_dir = os.getcwd()
        os.chdir(chapter_path)
        
        # Run the demo script
        result = subprocess.run([sys.executable, "run_demos.py"], 
                              capture_output=True, text=True, timeout=60)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
        
        # Return to original directory
        os.chdir(original_dir)
        
        success = result.returncode == 0
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{status} {chapter_name} demos completed")
        
        return success
        
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {chapter_name} demos took too long")
        os.chdir(original_dir)
        return False
    except Exception as e:
        print(f"[ERROR] Failed to run {chapter_name} demos: {e}")
        os.chdir(original_dir)
        return False

def main():
    """Main function to run all chapter demos."""
    print_header("Voice AI Systems Guide - Complete Demo Suite")
    
    # Get the project root directory
    project_root = Path(__file__).parent
    chapters_dir = project_root / "chapters"
    
    if not chapters_dir.exists():
        print("[ERROR] Chapters directory not found!")
        print(f"Expected: {chapters_dir}")
        return 1
    
    # Define chapter information
    chapters = [
        ("chapter1", "Chapter 1: Introduction to Voice Synthesis"),
        ("chapter2", "Chapter 2: Natural Language Processing in Call Centers"),
        ("chapter3", "Chapter 3: Integration with Telephony Systems"),
        ("chapter4", "Chapter 4: Best Practices in Conversational Design"),
        ("chapter5", "Chapter 5: Modern IVR Script Examples"),
        ("chapter6", "Chapter 6: Monitoring, Logging, and Analytics"),
        ("chapter7", "Chapter 7: Advanced Voice AI Features"),
        ("chapter8", "Chapter 8: Security and Compliance in Voice Applications"),
        ("chapter9", "Chapter 9: The Future of Voice AI in Contact Centers"),
        ("chapter10", "Chapter 10: Scalability and Cloud-Native Voice Architectures")
    ]
    
    print(f"Found {len(chapters)} chapters to test")
    print(f"Project root: {project_root}")
    print(f"Chapters directory: {chapters_dir}")
    
    # Track results
    results = []
    start_time = time.time()
    
    # Run each chapter's demos
    for chapter_dir, chapter_name in chapters:
        chapter_path = chapters_dir / chapter_dir
        
        if not chapter_path.exists():
            print(f"[WARNING] Chapter directory not found: {chapter_path}")
            results.append((chapter_name, False))
            continue
        
        success = run_demo(chapter_path, chapter_name)
        results.append((chapter_name, success))
        
        # Small delay between chapters
        time.sleep(1)
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print_header("Demo Suite Summary")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Total chapters tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    print(f"Total time: {duration:.2f} seconds")
    
    print("\nDetailed Results:")
    for chapter_name, success in results:
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"  {status} {chapter_name}")
    
    # Return appropriate exit code
    if successful == total:
        print("\n🎉 All demos completed successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - successful} chapter(s) had issues. Check the output above.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Demo suite stopped by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
