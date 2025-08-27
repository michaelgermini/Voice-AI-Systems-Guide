#!/usr/bin/env python3
"""
Chapter 2 - Natural Language Processing in Call Centers
Intent Recognition Demo
"""

import time
from typing import Dict, List

class IntentRecognition:
    """Intent recognition for voice AI systems"""
    
    def __init__(self):
        self.intents = {
            "check_balance": ["check balance", "account balance", "how much money", "balance inquiry"],
            "make_payment": ["pay bill", "make payment", "pay invoice", "payment"],
            "technical_support": ["technical help", "support", "problem with service", "issue"],
            "schedule_appointment": ["book appointment", "schedule meeting", "make reservation", "appointment"],
            "order_status": ["track order", "order status", "where is my order", "shipping"],
            "billing_inquiry": ["billing question", "invoice", "bill", "charges"]
        }
    
    def recognize_intent(self, user_input: str) -> dict:
        """Recognize user intent from input text"""
        user_input = user_input.lower()
        
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in user_input:
                    return {
                        "intent": intent,
                        "confidence": 0.85,
                        "matched_pattern": pattern
                    }
        
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "matched_pattern": None
        }

def demo_intent_recognition():
    """Demonstrate intent recognition capabilities"""
    
    print("=" * 60)
    print("INTENT RECOGNITION DEMO")
    print("=" * 60)
    
    # Initialize intent recognition
    intent_recognizer = IntentRecognition()
    
    # Test cases
    test_cases = [
        "I want to check my account balance",
        "Can you help me pay my bill?",
        "I'm having technical problems with my service",
        "I need to schedule an appointment",
        "Where is my order?",
        "I have a question about my bill",
        "What's the weather like today?",  # Unknown intent
        "How much money do I have in my account?"
    ]
    
    print("\nTesting Intent Recognition:")
    print("-" * 40)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Recognize intent
        result = intent_recognizer.recognize_intent(test_input)
        
        print(f"  Intent: {result['intent']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        if result['matched_pattern']:
            print(f"  Matched Pattern: '{result['matched_pattern']}'")
        
        # Color coding for results
        if result['intent'] != "unknown":
            print("  Status: [SUCCESS] Recognized")
        else:
            print("  Status: [FAILED] Unknown Intent")
    
    print("\n" + "=" * 60)
    print("DEMO SUMMARY")
    print("=" * 60)
    
    # Calculate statistics
    total_tests = len(test_cases)
    recognized = sum(1 for test in test_cases 
                    if intent_recognizer.recognize_intent(test)['intent'] != "unknown")
    
    print(f"Total Test Cases: {total_tests}")
    print(f"Successfully Recognized: {recognized}")
    print(f"Recognition Rate: {(recognized/total_tests)*100:.1f}%")
    
    print("\nSupported Intents:")
    for intent in intent_recognizer.intents.keys():
        print(f"  - {intent}")
    
    print("\nDemo completed successfully! [SUCCESS]")

if __name__ == "__main__":
    demo_intent_recognition()
