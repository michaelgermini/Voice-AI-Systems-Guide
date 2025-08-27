#!/usr/bin/env python3
"""
Chapter 6 Demo Runner
Executes all Chapter 6 demonstration scripts for Monitoring, Logging, and Analytics.
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
    """Main function to run all Chapter 6 demos"""
    print("Chapter 6: Monitoring, Logging, and Analytics in Voice Applications")
    print("="*80)
    print("This will run all Chapter 6 demonstration scripts:")
    print("1. Voice System Logger - Structured logging implementation")
    print("2. Performance Monitor - Real-time performance tracking")
    print("3. Analytics Dashboard - KPI visualization and reporting")
    print("4. Alert Manager - Automated alerting and incident response")
    print("5. Anomaly Detection - AI-powered anomaly detection")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/voice_system_logger.py", "Voice System Logger"),
        ("examples/performance_monitor.py", "Performance Monitor"),
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
    print("CHAPTER 6 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\nChapter 6 Key Concepts Demonstrated:")
    print("   • Structured logging with JSON formatting")
    print("   • Real-time performance monitoring")
    print("   • KPI calculation and threshold management")
    print("   • Automated alerting and incident response")
    print("   • Log analysis and statistics generation")
    print("   • Performance metrics tracking")
    print("   • Error analysis and pattern detection")
    
    print(f"\nMonitoring Best Practices:")
    print("   • Use structured logging for easy parsing")
    print("   • Implement correlation IDs for traceability")
    print("   • Set realistic thresholds based on actual data")
    print("   • Monitor both technical and business metrics")
    print("   • Implement automated alerting with escalation")
    print("   • Regular review and optimization of monitoring")
    
    print(f"\nProduction Readiness:")
    print("   • Scalable logging infrastructure")
    print("   • Real-time dashboard capabilities")
    print("   • Automated incident response")
    print("   • Performance optimization insights")
    print("   • Compliance and audit capabilities")
    print("   • Business intelligence and reporting")
    
    print(f"\nNext Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Implement monitoring in your voice AI systems")
    print("   • Set up alerting and incident response procedures")
    print("   • Create custom dashboards for your KPIs")
    print("   • Move to Chapter 7 for advanced voice AI features")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
