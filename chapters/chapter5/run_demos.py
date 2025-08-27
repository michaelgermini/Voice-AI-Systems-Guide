#!/usr/bin/env python3
"""
Chapter 5 Demo Runner
Executes all Chapter 5 demonstration scripts for Modern IVR Script Examples.
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
    """Main function to run all Chapter 5 demos"""
    print("Chapter 5: Modern IVR Script Examples")
    print("="*80)
    print("This will run all Chapter 5 demonstration scripts:")
    print("1. E-commerce Order Tracking")
    print("2. Healthcare Appointment Booking")
    print("3. Payment Collection System")
    print("4. Technical Support Flow")
    print("5. Banking Balance Inquiry")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/ecommerce_order_tracking.py", "E-commerce Order Tracking"),
        ("examples/healthcare_appointment.py", "Healthcare Appointment Booking"),
        ("examples/payment_collection.py", "Payment Collection System"),
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
    print("CHAPTER 5 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\nChapter 5 Key Concepts Demonstrated:")
    print("   • Real-world IVR implementations across industries")
    print("   • E-commerce order tracking with NLP and TTS")
    print("   • Healthcare appointment booking with HIPAA compliance")
    print("   • Payment collection with PCI compliance")
    print("   • Session management and conversation flow")
    print("   • Error handling and escalation patterns")
    print("   • SSML generation for natural TTS responses")
    
    print(f"\nIndustry Applications:")
    print("   • E-commerce: Order tracking, customer service")
    print("   • Healthcare: Appointment scheduling, patient care")
    print("   • Banking: Payment processing, account management")
    print("   • Technical Support: Issue resolution, troubleshooting")
    print("   • Customer Service: General inquiries, escalations")
    
    print(f"\nNext Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Adapt these patterns to your specific industry")
    print("   • Integrate with your existing backend systems")
    print("   • Test with real users and iterate")
    print("   • Move to Chapter 6 for advanced voice AI features")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
