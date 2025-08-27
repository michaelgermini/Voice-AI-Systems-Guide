#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Demo Runner

This script runs all Chapter 9 demonstration scripts and provides
a consolidated summary of the results.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def run_demo_script(script_path: str, script_name: str) -> bool:
    """Run a demo script and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Check if successful
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully")
            return True
        else:
            print(f"\n❌ {script_name} failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ {script_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"\n💥 {script_name} failed with exception: {str(e)}")
        return False

def main():
    """Main function to run all Chapter 9 demos"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Demo Runner")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all demos to run
    demos = [
        ("examples/microservices_setup.py", "Basic Microservices Setup"),
        ("examples/autoscaling_config.py", "Auto-scaling Configuration"),
        ("examples/load_balancing.py", "Load Balancing"),
        ("examples/storage_management.py", "Storage Management"),
        ("examples/observability.py", "Observability at Scale"),
    ]
    
    results = []
    start_time = time.time()
    
    # Run each demo
    for script_path, script_name in demos:
        if os.path.exists(script_path):
            success = run_demo_script(script_path, script_name)
            results.append((script_name, success))
        else:
            print(f"\n❌ Script not found: {script_path}")
            results.append((script_name, False))
    
    # Calculate summary
    end_time = time.time()
    total_time = end_time - start_time
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    # Print summary
    print(f"\n{'='*60}")
    print("CHAPTER 9 DEMO SUMMARY")
    print(f"{'='*60}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {script_name}")
    
    print(f"\nChapter 9 covers:")
    print("  ✓ Microservices architecture for voice AI")
    print("  ✓ Auto-scaling with Kubernetes HPA")
    print("  ✓ Global load balancing strategies")
    print("  ✓ Multi-tier storage management")
    print("  ✓ Distributed tracing and observability")
    
    print(f"\nKey Benefits Demonstrated:")
    print("  ✓ Horizontal scaling for voice applications")
    print("  ✓ Geographic distribution for low latency")
    print("  ✓ Cost optimization through tiered storage")
    print("  ✓ End-to-end observability across services")
    print("  ✓ Automatic failover and health monitoring")
    
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
