#!/usr/bin/env python3
"""
Chapter 3 Demo Runner
Executes all Chapter 3 demonstration scripts for Telephony Integration.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def run_demo_script(script_path: str, script_name: str) -> bool:
    """Run a single demo script and return success status"""
    print(f"\n{'='*80}")
    print(f"🚀 Running {script_name}")
    print(f"{'='*80}")
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Script completed successfully!")
            print("\n📋 Output:")
            print(result.stdout)
            return True
        else:
            print("❌ Script failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Script timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def main():
    """Main function to run all Chapter 3 demos"""
    print("📞 Chapter 3: Integration with Telephony Systems")
    print("="*80)
    print("This will run all Chapter 3 demonstration scripts:")
    print("1. Twilio Integration Demo")
    print("2. Call Flow Simulator")
    print("3. Telephony Platform Comparison")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/twilio_integration_demo.py", "Twilio Integration Demo"),
        ("examples/call_flow_simulator.py", "Call Flow Simulator"),
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
            print(f"❌ Script not found: {script_path}")
            results.append((script_name, False))
    
    # Print summary
    total_time = time.time() - start_time
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n{'='*80}")
    print("📊 CHAPTER 3 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\n📋 Results:")
    for script_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\n🎯 Chapter 3 Key Concepts Demonstrated:")
    print("   • Telephony Integration: Connecting voice AI with phone systems")
    print("   • Twilio Integration: Building cloud-based voice applications")
    print("   • Call Flow Management: Complete voice AI pipeline simulation")
    print("   • Performance Monitoring: Real-time call metrics and analytics")
    
    print(f"\n📚 Next Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Configure your own Twilio account for testing")
    print("   • Experiment with different call flows and scenarios")
    print("   • Move to Chapter 4 for advanced voice AI features")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
