#!/usr/bin/env python3
"""
Chapter 2 - Natural Language Processing in Call Centers
LLM Integration Demo
"""

import json
import time
from typing import Dict, Any

class LLMIntentClassifier:
    """Use LLMs for advanced intent classification"""
    
    def __init__(self):
        self.system_prompt = """
        You are a customer service AI assistant. Classify the customer's intent from their message.
        Available intents: check_balance, make_payment, technical_support, schedule_appointment, general_inquiry
        
        Return a JSON response with:
        - intent: the classified intent
        - confidence: confidence score (0-1)
        - reasoning: brief explanation
        - entities: any relevant information extracted
        """
    
    def classify_intent(self, user_input: str) -> Dict[str, Any]:
        """Classify intent using LLM"""
        
        # Simulate LLM response (in real implementation, call actual LLM API)
        response = self._simulate_llm_response(user_input)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "reasoning": "Failed to parse LLM response",
                "entities": {}
            }
    
    def _simulate_llm_response(self, user_input: str) -> str:
        """Simulate LLM response for demonstration"""
        user_input = user_input.lower()
        
        if any(word in user_input for word in ["balance", "account", "money", "how much"]):
            return json.dumps({
                "intent": "check_balance",
                "confidence": 0.92,
                "reasoning": "Customer is asking about account balance or money",
                "entities": {"account_type": "general"}
            })
        elif any(word in user_input for word in ["pay", "payment", "bill", "invoice"]):
            return json.dumps({
                "intent": "make_payment",
                "confidence": 0.88,
                "reasoning": "Customer wants to make a payment or pay a bill",
                "entities": {"payment_type": "bill"}
            })
        elif any(word in user_input for word in ["help", "support", "problem", "issue", "broken"]):
            return json.dumps({
                "intent": "technical_support",
                "confidence": 0.85,
                "reasoning": "Customer needs technical assistance or support",
                "entities": {"support_type": "technical"}
            })
        elif any(word in user_input for word in ["appointment", "schedule", "book", "meeting"]):
            return json.dumps({
                "intent": "schedule_appointment",
                "confidence": 0.87,
                "reasoning": "Customer wants to schedule or book an appointment",
                "entities": {"appointment_type": "general"}
            })
        else:
            return json.dumps({
                "intent": "general_inquiry",
                "confidence": 0.75,
                "reasoning": "General customer inquiry or question",
                "entities": {}
            })

class LLMResponseGenerator:
    """Generate contextual responses using LLMs"""
    
    def __init__(self):
        self.context_template = """
        Previous conversation context:
        - Intent: {intent}
        - Collected entities: {entities}
        - Conversation turn: {turn_count}
        
        Generate a natural, helpful response for the customer.
        Keep it concise and conversational.
        """
    
    def generate_response(self, context: dict, user_input: str) -> str:
        """Generate contextual response"""
        
        # Simulate LLM response generation
        return self._simulate_response_generation(context, user_input)
    
    def _simulate_response_generation(self, context: dict, user_input: str) -> str:
        """Simulate LLM response generation"""
        
        intent = context.get("intent", "unknown")
        entities = context.get("entities", {})
        
        if intent == "check_balance":
            if "account_number" in entities:
                return f"Let me check the balance for account {entities['account_number']}. Your current balance is $1,234.56."
            else:
                return "I'd be happy to check your balance. Could you please provide your account number?"
        
        elif intent == "make_payment":
            if "amount" in entities and "account_number" in entities:
                return f"I'll help you make a payment of {entities['amount']} for account {entities['account_number']}. Is this correct?"
            elif "amount" in entities:
                return f"I can help you make a payment of {entities['amount']}. What account should I apply this to?"
            else:
                return "I'd be happy to help you make a payment. What amount would you like to pay?"
        
        elif intent == "technical_support":
            return "I'm sorry to hear you're experiencing issues. Let me connect you with our technical support team who can better assist you."
        
        elif intent == "schedule_appointment":
            return "I can help you schedule an appointment. What date and time would work best for you?"
        
        else:
            return "I understand you need help. Let me connect you with a customer service representative who can assist you further."

def demo_llm_integration():
    """Demonstrate LLM integration capabilities"""
    
    print("=" * 60)
    print("LLM INTEGRATION DEMO")
    print("=" * 60)
    
    # Initialize LLM components
    llm_classifier = LLMIntentClassifier()
    llm_generator = LLMResponseGenerator()
    
    # Test cases for intent classification
    test_cases = [
        "I need to check my account balance",
        "Can you help me pay my electricity bill?",
        "My internet is not working properly",
        "I want to schedule a meeting with customer service",
        "What's the weather like today?",  # General inquiry
        "How much money do I have left in my savings account?"
    ]
    
    print("\nTesting LLM Intent Classification:")
    print("-" * 40)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Classify intent using LLM
        result = llm_classifier.classify_intent(test_input)
        
        print(f"  Intent: {result['intent']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Entities: {result['entities']}")
        
        # Generate response using LLM
        context = {
            "intent": result["intent"],
            "entities": result["entities"],
            "turn_count": 1
        }
        
        response = llm_generator.generate_response(context, test_input)
        print(f"  Generated Response: '{response}'")
        
        if result['intent'] != "unknown":
            print("  Status: [SUCCESS] LLM Classification Successful")
        else:
            print("  Status: [FAILED] LLM Classification Failed")
    
    print("\n" + "=" * 60)
    print("LLM INTEGRATION SUMMARY")
    print("=" * 60)
    
    # Calculate statistics
    total_tests = len(test_cases)
    successful = sum(1 for test in test_cases 
                    if llm_classifier.classify_intent(test)['intent'] != "unknown")
    
    print(f"Total Test Cases: {total_tests}")
    print(f"Successful Classifications: {successful}")
    print(f"Success Rate: {(successful/total_tests)*100:.1f}%")
    
    print("\nLLM Capabilities Demonstrated:")
    print("  - Advanced intent classification")
    print("  - Contextual reasoning")
    print("  - Entity extraction")
    print("  - Natural response generation")
    
    print("\nBenefits of LLM Integration:")
    print("  - Better understanding of complex queries")
    print("  - More natural conversation flow")
    print("  - Improved accuracy in intent recognition")
    print("  - Context-aware responses")
    
    print("\nDemo completed successfully! [SUCCESS]")

if __name__ == "__main__":
    demo_llm_integration()
