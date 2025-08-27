#!/usr/bin/env python3
"""
Chapter 2 - Natural Language Processing in Call Centers
Conversation Flow Demo
"""

import time
from enum import Enum
from typing import Dict, Any

class ConversationState(Enum):
    GREETING = "greeting"
    INTENT_COLLECTION = "intent_collection"
    ENTITY_COLLECTION = "entity_collection"
    CONFIRMATION = "confirmation"
    RESOLUTION = "resolution"
    CLOSING = "closing"

class IntentRecognition:
    """Simple intent recognition for demo"""
    def __init__(self):
        self.intents = {
            "check_balance": ["check balance", "account balance", "how much money"],
            "make_payment": ["pay bill", "make payment", "pay invoice"],
            "technical_support": ["technical help", "support", "problem"]
        }
    
    def recognize_intent(self, user_input: str) -> dict:
        user_input = user_input.lower()
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in user_input:
                    return {"intent": intent, "confidence": 0.85, "matched_pattern": pattern}
        return {"intent": "unknown", "confidence": 0.0, "matched_pattern": None}

class ConversationManager:
    """Manage multi-turn conversations"""
    
    def __init__(self):
        self.conversation_context = {}
        self.intent_recognizer = IntentRecognition()
    
    def process_user_input(self, user_input: str, call_id: str) -> dict:
        """Process user input and determine next action"""
        
        # Initialize context if new call
        if call_id not in self.conversation_context:
            self.conversation_context[call_id] = {
                "state": ConversationState.GREETING,
                "entities": {},
                "intent": None,
                "turn_count": 0
            }
        
        context = self.conversation_context[call_id]
        context["turn_count"] += 1
        
        # Recognize intent
        intent_result = self.intent_recognizer.recognize_intent(user_input)
        
        # Update context
        if intent_result["intent"] != "unknown":
            context["intent"] = intent_result["intent"]
        
        # Determine next action
        return self._determine_next_action(context, intent_result)
    
    def _determine_next_action(self, context: dict, intent_result: dict) -> dict:
        """Determine the next action based on current state"""
        
        if context["state"] == ConversationState.GREETING:
            return {
                "action": "ask_intent",
                "message": "Hello! How can I help you today?",
                "next_state": ConversationState.INTENT_COLLECTION
            }
        
        elif context["state"] == ConversationState.INTENT_COLLECTION:
            if intent_result["intent"] != "unknown":
                return {
                    "action": "collect_entities",
                    "message": self._get_entity_prompt(context["intent"]),
                    "next_state": ConversationState.ENTITY_COLLECTION
                }
            else:
                return {
                    "action": "clarify_intent",
                    "message": "I didn't understand. Could you please rephrase?",
                    "next_state": ConversationState.INTENT_COLLECTION
                }
        
        elif context["state"] == ConversationState.ENTITY_COLLECTION:
            if self._has_required_entities(context):
                return {
                    "action": "confirm_action",
                    "message": self._generate_confirmation_message(context),
                    "next_state": ConversationState.CONFIRMATION
                }
            else:
                return {
                    "action": "ask_missing_entity",
                    "message": self._get_missing_entity_prompt(context),
                    "next_state": ConversationState.ENTITY_COLLECTION
                }
        
        return {
            "action": "escalate",
            "message": "Let me connect you to a human agent.",
            "next_state": ConversationState.CLOSING
        }
    
    def _get_entity_prompt(self, intent: str) -> str:
        """Get prompt for collecting required entities"""
        prompts = {
            "check_balance": "Please provide your account number.",
            "make_payment": "What amount would you like to pay?",
            "technical_support": "What specific issue are you experiencing?"
        }
        return prompts.get(intent, "Please provide more details.")
    
    def _has_required_entities(self, context: dict) -> bool:
        """Check if all required entities have been collected"""
        required = self._get_required_entities_for_intent(context["intent"])
        return all(entity in context["entities"] for entity in required)
    
    def _get_required_entities_for_intent(self, intent: str) -> list:
        """Get required entities for a specific intent"""
        requirements = {
            "check_balance": ["account_number"],
            "make_payment": ["amount", "account_number"],
            "technical_support": ["issue_description"]
        }
        return requirements.get(intent, [])
    
    def _get_missing_entity_prompt(self, context: dict) -> str:
        """Get prompt for missing entities"""
        required = self._get_required_entities_for_intent(context["intent"])
        missing = [entity for entity in required if entity not in context["entities"]]
        
        if "account_number" in missing:
            return "I still need your account number. Could you provide it?"
        elif "amount" in missing:
            return "What amount would you like to pay?"
        elif "issue_description" in missing:
            return "Could you describe the issue you're experiencing?"
        
        return "I need a bit more information to help you."
    
    def _generate_confirmation_message(self, context: dict) -> str:
        """Generate confirmation message"""
        intent = context["intent"]
        entities = context["entities"]
        
        if intent == "check_balance":
            return f"I'll check the balance for account {entities.get('account_number', 'your account')}."
        elif intent == "make_payment":
            return f"I'll process a payment of {entities.get('amount', 'the specified amount')} for account {entities.get('account_number', 'your account')}."
        elif intent == "technical_support":
            return "I understand you're having technical issues. Let me connect you with our support team."
        
        return "I'll help you with that."

def demo_conversation_flow():
    """Demonstrate multi-turn conversation flow"""
    
    print("=" * 60)
    print("CONVERSATION FLOW DEMO")
    print("=" * 60)
    
    # Initialize conversation manager
    conversation_manager = ConversationManager()
    call_id = "demo_call_001"
    
    # Simulate conversation turns
    conversation_turns = [
        "Hello",
        "I want to check my balance",
        "My account number is 1234567890",
        "Yes, please check it"
    ]
    
    print("\nSimulating Multi-Turn Conversation:")
    print("-" * 40)
    
    for i, user_input in enumerate(conversation_turns, 1):
        print(f"\nTurn {i}:")
        print(f"User: '{user_input}'")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Process user input
        result = conversation_manager.process_user_input(user_input, call_id)
        
        print(f"System: '{result['message']}'")
        print(f"Action: {result['action']}")
        print(f"Next State: {result['next_state'].value}")
        
        # Update conversation state
        conversation_manager.conversation_context[call_id]["state"] = result["next_state"]
    
    print("\n" + "=" * 60)
    print("CONVERSATION SUMMARY")
    print("=" * 60)
    
    context = conversation_manager.conversation_context[call_id]
    print(f"Total Turns: {context['turn_count']}")
    print(f"Final State: {context['state'].value}")
    print(f"Recognized Intent: {context['intent']}")
    print(f"Collected Entities: {context['entities']}")
    
    print("\nConversation Flow:")
    for i, turn in enumerate(conversation_turns, 1):
        print(f"  Turn {i}: {turn}")
    
    print("\nDemo completed successfully! [SUCCESS]")

if __name__ == "__main__":
    demo_conversation_flow()
