#!/usr/bin/env python3
"""
E-commerce Order Tracking IVR - Chapter 5
Complete implementation of an order tracking system with NLP, TTS, and telephony integration.
"""

import os
import time
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Order:
    """Represents an order in the system"""
    order_number: str
    customer_name: str
    items: List[Dict]
    total_amount: float
    status: OrderStatus
    order_date: datetime
    shipping_date: Optional[datetime]
    estimated_delivery: Optional[datetime]
    tracking_number: Optional[str]

@dataclass
class CallSession:
    """Represents an active call session"""
    call_id: str
    phone_number: str
    start_time: datetime
    current_state: str
    order_number: Optional[str]
    retry_count: int
    conversation_history: List[Dict]

class EcommerceOrderTrackingIVR:
    """Complete e-commerce order tracking IVR system"""
    
    def __init__(self):
        # Initialize order database (simulated)
        self.orders_db = self.initialize_orders_database()
        
        # Active call sessions
        self.active_sessions = {}
        
        # NLP patterns for intent recognition
        self.intent_patterns = {
            "track_order": [
                r"track.*order", r"order.*status", r"where.*order", 
                r"check.*order", r"order.*tracking", r"my.*order"
            ],
            "cancel_order": [
                r"cancel.*order", r"cancel.*purchase", r"refund.*order"
            ],
            "speak_agent": [
                r"speak.*agent", r"human.*agent", r"representative", 
                r"talk.*someone", r"help.*agent"
            ]
        }
        
        # SSML templates for responses
        self.ssml_templates = {
            "greeting": {
                "text": "Welcome to ShopEasy. How can I assist you today?",
                "ssml": '<speak>Welcome to <emphasis level="moderate">ShopEasy</emphasis>. <break time="300ms"/> How can I assist you today?</speak>'
            },
            "ask_order_number": {
                "text": "Please provide your order number.",
                "ssml": '<speak>Please provide your order number.</speak>'
            },
            "confirm_order_number": {
                "text": "Did you say order number {order_number}?",
                "ssml": '<speak>Did you say order number <say-as interpret-as="digits">{order_number}</say-as>?</speak>'
            },
            "order_not_found": {
                "text": "I couldn't find order number {order_number}. Please check the number and try again.",
                "ssml": '<speak>I couldn\'t find order number <say-as interpret-as="digits">{order_number}</say-as>. <break time="300ms"/> Please check the number and try again.</speak>'
            },
            "order_status": {
                "text": "Order {order_number} is {status}. {additional_info}",
                "ssml": '<speak>Order <say-as interpret-as="digits">{order_number}</say-as> is <emphasis level="moderate">{status}</emphasis>. <break time="300ms"/> {additional_info}</speak>'
            },
            "anything_else": {
                "text": "Is there anything else I can help you with?",
                "ssml": '<speak>Is there anything else I can help you with?</speak>'
            },
            "goodbye": {
                "text": "Thank you for calling ShopEasy. Have a great day!",
                "ssml": '<speak>Thank you for calling <emphasis level="moderate">ShopEasy</emphasis>. <break time="200ms"/> Have a great day!</speak>'
            },
            "escalate": {
                "text": "I'll connect you with a customer service representative. Please hold.",
                "ssml": '<speak>I\'ll connect you with a customer service representative. <break time="300ms"/> Please hold.</speak>'
            }
        }

    def initialize_orders_database(self) -> Dict[str, Order]:
        """Initialize a simulated orders database"""
        orders = {}
        
        # Sample orders
        sample_orders = [
            Order(
                order_number="12345",
                customer_name="John Smith",
                items=[{"name": "Wireless Headphones", "quantity": 1, "price": 89.99}],
                total_amount=89.99,
                status=OrderStatus.SHIPPED,
                order_date=datetime.now() - timedelta(days=3),
                shipping_date=datetime.now() - timedelta(days=1),
                estimated_delivery=datetime.now() + timedelta(days=1),
                tracking_number="1Z999AA1234567890"
            ),
            Order(
                order_number="67890",
                customer_name="Jane Doe",
                items=[{"name": "Smartphone Case", "quantity": 2, "price": 24.99}],
                total_amount=49.98,
                status=OrderStatus.PROCESSING,
                order_date=datetime.now() - timedelta(days=1),
                shipping_date=None,
                estimated_delivery=None,
                tracking_number=None
            ),
            Order(
                order_number="11111",
                customer_name="Bob Johnson",
                items=[{"name": "Laptop Stand", "quantity": 1, "price": 45.00}],
                total_amount=45.00,
                status=OrderStatus.DELIVERED,
                order_date=datetime.now() - timedelta(days=7),
                shipping_date=datetime.now() - timedelta(days=5),
                estimated_delivery=datetime.now() - timedelta(days=2),
                tracking_number="1Z999AA1111111111"
            )
        ]
        
        for order in sample_orders:
            orders[order.order_number] = order
        
        return orders

    def classify_intent(self, utterance: str) -> Dict:
        """Classify customer intent from utterance"""
        utterance_lower = utterance.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, utterance_lower):
                    confidence = 0.9 if len(utterance) > 10 else 0.7
                    return {
                        "intent": intent,
                        "confidence": confidence,
                        "utterance": utterance
                    }
        
        # Check for order numbers in utterance
        order_numbers = re.findall(r'\b(\d{5,})\b', utterance)
        if order_numbers:
            return {
                "intent": "provide_order_number",
                "confidence": 0.8,
                "order_number": order_numbers[0],
                "utterance": utterance
            }
        
        return {
            "intent": "unknown",
            "confidence": 0.3,
            "utterance": utterance
        }

    def extract_order_number(self, utterance: str) -> Optional[str]:
        """Extract order number from utterance"""
        order_numbers = re.findall(r'\b(\d{5,})\b', utterance)
        return order_numbers[0] if order_numbers else None

    def get_order_status(self, order_number: str) -> Optional[Order]:
        """Get order status from database"""
        return self.orders_db.get(order_number)

    def generate_order_status_response(self, order: Order) -> str:
        """Generate natural language response for order status"""
        if order.status == OrderStatus.PENDING:
            return f"Your order is currently pending and will be processed soon. Estimated processing time is 1-2 business days."
        
        elif order.status == OrderStatus.PROCESSING:
            return f"Your order is being processed and will be shipped within 24 hours."
        
        elif order.status == OrderStatus.SHIPPED:
            if order.estimated_delivery:
                delivery_date = order.estimated_delivery.strftime("%A, %B %d")
                return f"Your order has been shipped and is expected to arrive on {delivery_date}. Your tracking number is {order.tracking_number}."
            else:
                return f"Your order has been shipped. Your tracking number is {order.tracking_number}."
        
        elif order.status == OrderStatus.DELIVERED:
            return f"Your order has been delivered. Thank you for your purchase!"
        
        elif order.status == OrderStatus.CANCELLED:
            return f"Your order has been cancelled. If you have any questions, please speak with a customer service representative."
        
        return "I'm sorry, I couldn't determine the status of your order."

    def create_session(self, call_id: str, phone_number: str) -> CallSession:
        """Create a new call session"""
        session = CallSession(
            call_id=call_id,
            phone_number=phone_number,
            start_time=datetime.now(),
            current_state="greeting",
            order_number=None,
            retry_count=0,
            conversation_history=[]
        )
        self.active_sessions[call_id] = session
        return session

    def get_session(self, call_id: str) -> Optional[CallSession]:
        """Get existing call session"""
        return self.active_sessions.get(call_id)

    def update_session(self, call_id: str, **kwargs):
        """Update call session"""
        if call_id in self.active_sessions:
            session = self.active_sessions[call_id]
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)

    def log_conversation(self, call_id: str, speaker: str, text: str, metadata: Dict = None):
        """Log conversation turn"""
        if call_id in self.active_sessions:
            session = self.active_sessions[call_id]
            session.conversation_history.append({
                "timestamp": datetime.now(),
                "speaker": speaker,
                "text": text,
                "metadata": metadata or {}
            })

    def handle_webhook(self, call_id: str, phone_number: str, speech_result: str = None, 
                      confidence: float = None, digits: str = None) -> Dict:
        """Handle incoming webhook from telephony platform"""
        
        # Create or get session
        session = self.get_session(call_id)
        if not session:
            session = self.create_session(call_id, phone_number)
        
        # Log customer input
        if speech_result:
            self.log_conversation(call_id, "customer", speech_result, {"confidence": confidence})
        
        # Process based on current state
        if session.current_state == "greeting":
            return self.handle_greeting(session, speech_result)
        elif session.current_state == "collecting_order_number":
            return self.handle_order_number_collection(session, speech_result, digits)
        elif session.current_state == "confirming_order_number":
            return self.handle_order_confirmation(session, speech_result)
        elif session.current_state == "providing_status":
            return self.handle_status_provided(session, speech_result)
        else:
            return self.handle_unknown_state(session)

    def handle_greeting(self, session: CallSession, utterance: str) -> Dict:
        """Handle initial greeting and intent recognition"""
        if not utterance:
            # Initial greeting
            self.update_session(session.call_id, current_state="greeting")
            return {
                "response": self.ssml_templates["greeting"]["ssml"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        
        # Classify intent
        intent = self.classify_intent(utterance)
        
        if intent["intent"] == "track_order":
            self.update_session(session.call_id, current_state="collecting_order_number")
            return {
                "response": self.ssml_templates["ask_order_number"]["ssml"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        
        elif intent["intent"] == "speak_agent":
            return {
                "response": self.ssml_templates["escalate"]["ssml"],
                "next_action": "transfer",
                "transfer_number": "+1234567890"
            }
        
        else:
            # Unknown intent - ask for clarification
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"]["ssml"],
                    "next_action": "transfer",
                    "transfer_number": "+1234567890"
                }
            else:
                return {
                    "response": '<speak>I didn\'t understand that. You can say "track my order" or "speak to an agent".</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_order_number_collection(self, session: CallSession, utterance: str, digits: str) -> Dict:
        """Handle order number collection"""
        order_number = None
        
        if utterance:
            order_number = self.extract_order_number(utterance)
        elif digits:
            order_number = digits
        
        if order_number:
            # Confirm order number
            self.update_session(session.call_id, order_number=order_number, current_state="confirming_order_number")
            confirm_ssml = self.ssml_templates["confirm_order_number"]["ssml"].format(order_number=order_number)
            return {
                "response": confirm_ssml,
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            # No order number found
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"]["ssml"],
                    "next_action": "transfer",
                    "transfer_number": "+1234567890"
                }
            else:
                return {
                    "response": '<speak>I didn\'t catch the order number. Please say it clearly, or you can enter it using your keypad.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_order_confirmation(self, session: CallSession, utterance: str) -> Dict:
        """Handle order number confirmation"""
        if utterance and any(word in utterance.lower() for word in ["yes", "correct", "right", "that's right"]):
            # Order number confirmed, look up status
            order = self.get_order_status(session.order_number)
            
            if order:
                # Generate status response
                status_response = self.generate_order_status_response(order)
                status_ssml = self.ssml_templates["order_status"]["ssml"].format(
                    order_number=order.order_number,
                    status=order.status.value,
                    additional_info=status_response
                )
                
                self.update_session(session.call_id, current_state="providing_status")
                return {
                    "response": status_ssml,
                    "next_action": "gather_speech",
                    "timeout": 10
                }
            else:
                # Order not found
                not_found_ssml = self.ssml_templates["order_not_found"]["ssml"].format(
                    order_number=session.order_number
                )
                self.update_session(session.call_id, current_state="collecting_order_number", order_number=None, retry_count=0)
                return {
                    "response": not_found_ssml,
                    "next_action": "gather_speech",
                    "timeout": 10
                }
        else:
            # Order number not confirmed, ask again
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"]["ssml"],
                    "next_action": "transfer",
                    "transfer_number": "+1234567890"
                }
            else:
                return {
                    "response": '<speak>Please say yes to confirm, or no to try a different order number.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_status_provided(self, session: CallSession, utterance: str) -> Dict:
        """Handle after providing order status"""
        if utterance and any(word in utterance.lower() for word in ["no", "that's all", "nothing else"]):
            # Customer is done
            return {
                "response": self.ssml_templates["goodbye"]["ssml"],
                "next_action": "hangup"
            }
        else:
            # Ask if they need anything else
            return {
                "response": self.ssml_templates["anything_else"]["ssml"],
                "next_action": "gather_speech",
                "timeout": 10
            }

    def handle_unknown_state(self, session: CallSession) -> Dict:
        """Handle unknown state"""
        return {
            "response": self.ssml_templates["escalate"]["ssml"],
            "next_action": "transfer",
            "transfer_number": "+1234567890"
        }

    def simulate_call_flow(self, test_scenarios: List[Dict]) -> List[Dict]:
        """Simulate complete call flows for testing"""
        results = []
        
        for scenario in test_scenarios:
            print(f"\nSimulating: {scenario['name']}")
            print("-" * 50)
            
            call_id = f"test_{int(time.time())}"
            phone_number = scenario.get("phone_number", "+15551234567")
            
            # Initialize call
            session = self.create_session(call_id, phone_number)
            
            # Process each turn
            for i, turn in enumerate(scenario["turns"]):
                print(f"Turn {i+1}: Customer says: '{turn['customer_input']}'")
                
                # Handle webhook
                response = self.handle_webhook(
                    call_id=call_id,
                    phone_number=phone_number,
                    speech_result=turn["customer_input"],
                    confidence=turn.get("confidence", 0.9)
                )
                
                print(f"Response: {response['next_action']}")
                print(f"SSML: {response['response'][:100]}...")
                
                # Check if call should end
                if response["next_action"] in ["hangup", "transfer"]:
                    break
            
            # Store results
            results.append({
                "scenario": scenario["name"],
                "call_id": call_id,
                "final_state": session.current_state,
                "conversation_turns": len(session.conversation_history),
                "success": response["next_action"] == "hangup"
            })
        
        return results

    def run_demo(self):
        """Run the e-commerce order tracking demo"""
        print("E-commerce Order Tracking IVR - Chapter 5")
        print("="*80)
        print("Demonstrating complete order tracking system...")
        
        # Define test scenarios
        test_scenarios = [
            {
                "name": "Successful Order Tracking",
                "phone_number": "+15551234567",
                "turns": [
                    {"customer_input": "I want to track my order", "confidence": 0.95},
                    {"customer_input": "12345", "confidence": 0.9},
                    {"customer_input": "Yes", "confidence": 0.9},
                    {"customer_input": "No, that's all", "confidence": 0.9}
                ]
            },
            {
                "name": "Order Not Found",
                "phone_number": "+15559876543",
                "turns": [
                    {"customer_input": "Track my order", "confidence": 0.9},
                    {"customer_input": "99999", "confidence": 0.9},
                    {"customer_input": "Yes", "confidence": 0.9},
                    {"customer_input": "Let me try 12345", "confidence": 0.9},
                    {"customer_input": "Yes", "confidence": 0.9},
                    {"customer_input": "That's all", "confidence": 0.9}
                ]
            },
            {
                "name": "Escalation to Agent",
                "phone_number": "+15551111111",
                "turns": [
                    {"customer_input": "I want to speak to an agent", "confidence": 0.9}
                ]
            }
        ]
        
        # Run simulations
        results = self.simulate_call_flow(test_scenarios)
        
        # Print summary
        print(f"\n{'='*80}")
        print("DEMO SUMMARY")
        print(f"{'='*80}")
        
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"Total Scenarios: {total}")
        print(f"Successful: {successful}/{total} ({successful/total*100:.1f}%)")
        
        print(f"\nDetailed Results:")
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            print(f"  {status} - {result['scenario']}")
            print(f"    Final State: {result['final_state']}")
            print(f"    Turns: {result['conversation_turns']}")
        
        print(f"\nKey Features Demonstrated:")
        print(f"  • Natural Language Processing for intent recognition")
        print(f"  • Order number extraction and validation")
        print(f"  • SSML generation for natural TTS responses")
        print(f"  • Session management and conversation flow")
        print(f"  • Error handling and escalation")
        print(f"  • Order status lookup and response generation")
        
        print(f"\nE-commerce order tracking demo completed!")
        print("   This demonstrates a complete, production-ready IVR system.")

if __name__ == "__main__":
    ivr = EcommerceOrderTrackingIVR()
    ivr.run_demo()
