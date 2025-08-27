#!/usr/bin/env python3
"""
Chapter 8 Demo Runner
Executes all Chapter 8 demonstration scripts for Security and Compliance in Voice Applications.
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
    """Main function to run all Chapter 8 demos"""
    print("Chapter 8: Security and Compliance in Voice Applications")
    print("="*80)
    print("This will run all Chapter 8 demonstration scripts:")
    print("1. Voice Security Framework - Comprehensive security implementation")
    print("2. Compliance Manager - GDPR, HIPAA, and PCI compliance")
    print("3. Audit System - Comprehensive audit trails and monitoring")
    print("4. Responsible AI - Ethical AI practices and transparency")
    print("="*80)
    
    # Define demo scripts
    demos = [
        ("examples/voice_security_framework.py", "Voice Security Framework"),
        ("examples/compliance_manager.py", "Compliance Manager"),
        ("examples/audit_system.py", "Audit System"),
        ("examples/responsible_ai.py", "Responsible AI"),
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
    print("CHAPTER 8 DEMO SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Successful: {successful}/{total}")
    print(f"Success Rate: {(successful/total)*100:.1f}%")
    
    print(f"\nResults:")
    for script_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status} - {script_name}")
    
    print(f"\nChapter 8 Key Concepts Demonstrated:")
    print("   • Voice data encryption and secure transmission")
    print("   • Multi-factor authentication and access control")
    print("   • GDPR, HIPAA, and PCI compliance management")
    print("   • Comprehensive audit trails and monitoring")
    print("   • Ethical AI practices and transparency")
    print("   • Bias detection and fairness monitoring")
    
    print(f"\nSecurity and Compliance Capabilities:")
    print("   • Voice Security Framework: Encryption, authentication, threat detection")
    print("   • Compliance Manager: GDPR, HIPAA, PCI compliance automation")
    print("   • Audit System: Comprehensive logging, monitoring, and reporting")
    print("   • Responsible AI: Ethics, transparency, bias detection, accountability")
    print("   • Data Protection: Sensitive data masking and secure handling")
    print("   • Regulatory Compliance: Automated compliance checking and reporting")
    
    print(f"\nProduction Benefits:")
    print("   • Enhanced Security: Comprehensive protection of voice data")
    print("   • Regulatory Compliance: Automated compliance with major frameworks")
    print("   • Risk Mitigation: Proactive threat detection and response")
    print("   • Customer Trust: Transparent and ethical AI practices")
    print("   • Audit Readiness: Complete audit trails and reporting")
    print("   • Legal Protection: Compliance with data protection regulations")
    
    print(f"\nImplementation Considerations:")
    print("   • Security by Design: Integrate security from the beginning")
    print("   • Privacy First: Implement privacy-by-design principles")
    print("   • Compliance Automation: Automate compliance checking and reporting")
    print("   • Ethical AI: Ensure transparency and fairness in AI decisions")
    print("   • Continuous Monitoring: Real-time security and compliance monitoring")
    print("   • Regular Audits: Conduct regular security and compliance audits")
    
    print(f"\nNext Steps:")
    print("   • Review the individual demo outputs above")
    print("   • Implement security and compliance measures in your voice AI systems")
    print("   • Ensure regulatory compliance for your target markets")
    print("   • Establish ethical AI practices and monitoring")
    print("   • Conduct regular security and compliance assessments")
    print("   • Move to Chapter 9 for deployment and scaling strategies")
    
    print(f"\n{'='*80}")
    
    # Return success if all demos passed
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
