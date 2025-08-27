#!/usr/bin/env python3
"""
Twilio Integration Demo - Chapter 3 (Simplified)
Demonstrates building a complete voice AI application with Twilio Programmable Voice.
This version simulates the functionality without requiring external dependencies.
"""

import os
import time
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CallSession:
    """Represents an active call session"""
    call_sid: str
    phone_number: str
    session_data: Dict
    start_time: datetime
    current_state: str
    conversation_history: List[Dict]

class TwilioVoiceAIDemo:
    """Demonstrates Twilio integration with voice AI capabilities (simulated)"""
    
    def __init__(self):
        self.active_sessions = {}
        
        # Define call flows and responses
        self.call_flows = {
            "greeting": {
                "message": "Welcome to our AI-powered customer service. How can I help you today?",
                "voice": "Polly.Joanna",
                "next_state": "get_intent"
            },
            "get_intent": {
                "message": "Please tell me what you need help with.",
                "voice": "Polly.Joanna",
                "next_state": "process_intent"
            },
            "balance_check": {
                "message": "I can help you check your balance. For security, I'll need to verify your identity. What's the last 4 digits of your social security number?",
                "voice": "Polly.Joanna",
                "next_state": "collect_ssn"
            },
            "password_reset": {
                "message": "I understand you need to reset your password. What email address is associated with your account?",
                "voice": "Polly.Joanna",
                "next_state": "collect_email"
            },
            "escalate_agent": {
                "message": "I'm connecting you with a human agent who can better assist you. Please hold.",
                "voice": "Polly.Joanna",
                "next_state": "transfer_call"
            }
        }
        
        # Simulated TwiML responses
        self.twillml_responses = {
            "voice": """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Welcome to our AI-powered customer service. How can I help you today?</Say>
    <Gather input="speech" action="/process_speech" method="POST" speech_timeout="auto" language="en-US">
        <Say voice="Polly.Joanna">Please tell me what you need help with.</Say>
    </Gather>
    <Say voice="Polly.Joanna">I didn't hear anything. Please try again or say 'agent' to speak with a human.</Say>
</Response>""",
            
            "process_speech": """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I can help you check your balance. For security, I'll need to verify your identity. What's the last 4 digits of your social security number?</Say>
    <Gather input="speech" action="/collect_ssn" method="POST" speech_timeout="auto" language="en-US">
        <Say voice="Polly.Joanna">Please say the last 4 digits of your social security number.</Say>
    </Gather>
</Response>""",
            
            "collect_ssn": """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Thank you. Your account balance is $2,456.78. Is there anything else I can help you with?</Say>
    <Gather input="speech" action="/process_speech" method="POST" speech_timeout="auto" language="en-US">
        <Say voice="Polly.Joanna">Please say yes or no, or ask another question.</Say>
    </Gather>
</Response>"""
        }
    
    def create_session(self, call_sid: str, phone_number: str) -> CallSession:
        """Create a new call session"""
        session = CallSession(
            call_sid=call_sid,
            phone_number=phone_number,
            session_data={},
            start_time=datetime.now(),
            current_state="greeting",
            conversation_history=[]
        )
        self.active_sessions[call_sid] = session
        logger.info(f"Created session for call {call_sid}")
        return session
    
    def get_session(self, call_sid: str) -> Optional[CallSession]:
        """Get existing call session"""
        return self.active_sessions.get(call_sid)
    
    def update_session(self, call_sid: str, **kwargs):
        """Update session data"""
        session = self.get_session(call_sid)
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
                else:
                    session.session_data[key] = value
    
    def log_conversation(self, call_sid: str, speaker: str, message: str, confidence: float = None):
        """Log conversation turn"""
        session = self.get_session(call_sid)
        if session:
            turn = {
                "timestamp": datetime.now(),
                "speaker": speaker,
                "message": message,
                "confidence": confidence
            }
            session.conversation_history.append(turn)
    
    def classify_intent(self, speech_text: str) -> Tuple[str, float]:
        """Classify customer intent from speech"""
        speech_lower = speech_text.lower()
        
        # Simple intent classification
        if any(word in speech_lower for word in ["balance", "account balance", "how much", "money"]):
            return "balance_check", 0.9
        elif any(word in speech_lower for word in ["password", "reset", "forgot", "can't log in"]):
            return "reset_password", 0.9
        elif any(word in speech_lower for word in ["agent", "human", "person", "representative"]):
            return "escalate_agent", 0.8
        else:
            return "unknown", 0.3
    
    def extract_entities(self, speech_text: str) -> Dict[str, str]:
        """Extract entities from speech"""
        entities = {}
        
        # Extract SSN (4 digits)
        ssn_pattern = r'\b\d{4}\b'
        ssn_matches = re.findall(ssn_pattern, speech_text)
        if ssn_matches:
            entities["ssn_last4"] = ssn_matches[0]
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, speech_text)
        if emails:
            entities["email"] = emails[0]
        
        return entities
    
    def simulate_webhook_call(self, endpoint: str, call_sid: str, phone_number: str, speech_result: str = None, confidence: float = None) -> str:
        """Simulate a Twilio webhook call"""
        logger.info(f"Simulating webhook call to {endpoint}")
        
        if endpoint == "/voice":
            # Handle incoming call
            session = self.create_session(call_sid, phone_number)
            return self.twillml_responses["voice"]
        
        elif endpoint == "/process_speech":
            # Handle speech input
            session = self.get_session(call_sid)
            if not session:
                return self.create_error_response("Session not found")
            
            # Log customer input
            self.log_conversation(call_sid, "customer", speech_result, confidence)
            
            # Classify intent
            intent, intent_confidence = self.classify_intent(speech_result)
            
            if intent == "balance_check":
                # Route to balance check flow
                self.update_session(call_sid, current_state="collecting_ssn")
                return self.twillml_responses["process_speech"]
            
            elif intent == "password_reset":
                # Route to password reset flow
                flow = self.call_flows["password_reset"]
                self.update_session(call_sid, current_state="collecting_email")
                return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{flow['voice']}">{flow['message']}</Say>
    <Gather input="speech" action="/collect_email" method="POST" speech_timeout="auto" language="en-US">
        <Say voice="{flow['voice']}">Please say your email address.</Say>
    </Gather>
</Response>"""
            
            elif intent == "escalate_agent":
                # Transfer to human agent
                return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I'm connecting you with a human agent. Please hold.</Say>
    <Dial>+1234567890</Dial>
</Response>"""
            
            else:
                # Unknown intent - escalate to agent
                return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I didn't understand that. Let me connect you with a human agent who can help.</Say>
    <Dial>+1234567890</Dial>
</Response>"""
        
        elif endpoint == "/collect_ssn":
            # Handle SSN collection
            session = self.get_session(call_sid)
            if not session:
                return self.create_error_response("Session not found")
            
            # Log customer input
            self.log_conversation(call_sid, "customer", speech_result, confidence)
            
            # Extract SSN
            entities = self.extract_entities(speech_result)
            ssn = entities.get("ssn_last4")
            
            if ssn and len(ssn) == 4:
                # Simulate balance lookup
                self.update_session(call_sid, current_state="completed", ssn_last4=ssn)
                return self.twillml_responses["collect_ssn"]
            else:
                return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I didn't catch that. Please say the last 4 digits of your social security number.</Say>
    <Gather input="speech" action="/collect_ssn" method="POST" speech_timeout="auto" language="en-US">
        <Say voice="Polly.Joanna">Please repeat the last 4 digits of your social security number.</Say>
    </Gather>
</Response>"""
        
        return self.create_error_response("Unknown endpoint")
    
    def create_error_response(self, message: str) -> str:
        """Create error response"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I'm sorry, there was an error: {message}. Please try again later.</Say>
    <Hangup/>
</Response>"""
    
    def get_session_analytics(self, call_sid: str) -> Dict:
        """Get analytics for a call session"""
        session = self.get_session(call_sid)
        if not session:
            return {}
        
        duration = (datetime.now() - session.start_time).total_seconds()
        turns = len(session.conversation_history)
        
        return {
            "call_sid": call_sid,
            "phone_number": session.phone_number,
            "duration_seconds": duration,
            "conversation_turns": turns,
            "final_state": session.current_state,
            "session_data": session.session_data
        }
    
    def run_demo(self):
        """Run the Twilio voice AI demo simulation"""
        print("Twilio Voice AI Integration Demo (Simulated)")
        print("="*50)
        print("This demo simulates Twilio webhook calls without external dependencies")
        print("="*50)
        
        # Simulate test calls
        test_calls = [
            {
                "call_sid": "CA1234567890abcdef",
                "phone_number": "+15551234567",
                "speech_inputs": [
                    "I want to check my account balance",
                    "1234"
                ]
            },
            {
                "call_sid": "CA0987654321fedcba",
                "phone_number": "+15559876543",
                "speech_inputs": [
                    "I forgot my password and can't log in",
                    "john.doe@email.com"
                ]
            },
            {
                "call_sid": "CA1111111111111111",
                "phone_number": "+15551111111",
                "speech_inputs": [
                    "I need to speak with a human agent"
                ]
            }
        ]
        
        for i, test_call in enumerate(test_calls, 1):
            print(f"\nTest Call {i}: {test_call['phone_number']}")
            print("-" * 40)
            
            # Simulate incoming call
            print("1. Incoming call...")
            response = self.simulate_webhook_call("/voice", test_call["call_sid"], test_call["phone_number"])
            print("   Response: Initial greeting and gather")
            
            # Simulate speech inputs
            for j, speech_input in enumerate(test_call["speech_inputs"], 1):
                print(f"\n2.{j} Customer says: '{speech_input}'")
                
                if j == 1:
                    # First speech input goes to process_speech
                    response = self.simulate_webhook_call("/process_speech", test_call["call_sid"], test_call["phone_number"], speech_input, 0.9)
                else:
                    # Subsequent inputs go to collect_ssn or other endpoints
                    response = self.simulate_webhook_call("/collect_ssn", test_call["call_sid"], test_call["phone_number"], speech_input, 0.9)
                
                print(f"   Response: {len(response)} characters of TwiML")
            
            # Get analytics
            analytics = self.get_session_analytics(test_call["call_sid"])
            print(f"\n3. Call Analytics:")
            print(f"   Duration: {analytics['duration_seconds']:.1f} seconds")
            print(f"   Turns: {analytics['conversation_turns']}")
            print(f"   Final State: {analytics['final_state']}")
        
        print(f"\nTwilio integration demo completed!")
        print("   This demonstrates how to build voice AI applications with Twilio.")
        print("   In a real implementation, you would:")
        print("   - Deploy this as a Flask web application")
        print("   - Configure Twilio webhook URLs")
        print("   - Handle real voice calls and speech input")

if __name__ == "__main__":
    demo = TwilioVoiceAIDemo()
    demo.run_demo()
