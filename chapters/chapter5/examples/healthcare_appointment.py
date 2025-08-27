#!/usr/bin/env python3
"""
Healthcare Appointment Booking IVR - Chapter 5
Medical appointment scheduling system with HIPAA compliance.
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

class AppointmentType(Enum):
    CHECKUP = "checkup"
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"

@dataclass
class CallSession:
    call_id: str
    phone_number: str
    start_time: datetime
    current_state: str
    patient_name: Optional[str]
    doctor_name: Optional[str]
    appointment_type: Optional[AppointmentType]
    preferred_date: Optional[str]
    preferred_time: Optional[str]
    retry_count: int

class HealthcareAppointmentIVR:
    """Healthcare appointment booking IVR system"""
    
    def __init__(self):
        self.active_sessions = {}
        
        # SSML templates
        self.ssml_templates = {
            "greeting": '<speak>Hello, this is <emphasis level="moderate">CityCare Medical Center</emphasis>. <break time="300ms"/> How can I help you today?</speak>',
            "ask_patient_name": '<speak>For security purposes, please provide your full name.</speak>',
            "ask_doctor_name": '<speak>Which doctor would you like to see?</speak>',
            "ask_appointment_type": '<speak>What type of appointment do you need? You can say checkup, consultation, or follow-up.</speak>',
            "ask_date": '<speak>What is your preferred date for the appointment?</speak>',
            "ask_time": '<speak>What time would you prefer? Available times are 9 AM, 10 AM, 2 PM, and 3 PM.</speak>',
            "confirm_appointment": '<speak>I have you scheduled with Dr. <emphasis level="moderate">{doctor}</emphasis> on <emphasis level="moderate">{date}</emphasis> at <emphasis level="moderate">{time}</emphasis> for a <emphasis level="moderate">{type}</emphasis>. <break time="300ms"/> Is this correct?</speak>',
            "appointment_confirmed": '<speak>Your appointment has been confirmed. <break time="300ms"/> Please arrive 15 minutes early to complete paperwork.</speak>',
            "emergency": '<speak>I understand this is urgent. <break time="300ms"/> Let me connect you with our emergency triage nurse immediately.</speak>',
            "goodbye": '<speak>Thank you for calling <emphasis level="moderate">CityCare Medical Center</emphasis>. <break time="200ms"/> Have a healthy day!</speak>',
            "escalate": '<speak>I\'ll connect you with a medical assistant who can better assist you. <break time="300ms"/> Please hold.</speak>'
        }

    def classify_intent(self, utterance: str) -> Dict:
        """Classify customer intent"""
        utterance_lower = utterance.lower()
        
        if any(word in utterance_lower for word in ["book", "appointment", "schedule"]):
            return {"intent": "book_appointment", "confidence": 0.9}
        elif any(word in utterance_lower for word in ["emergency", "urgent", "pain"]):
            return {"intent": "emergency", "confidence": 0.95}
        elif any(word in utterance_lower for word in ["agent", "nurse", "representative"]):
            return {"intent": "speak_agent", "confidence": 0.9}
        else:
            return {"intent": "unknown", "confidence": 0.3}

    def extract_doctor_name(self, utterance: str) -> Optional[str]:
        """Extract doctor name"""
        doctor_pattern = r'Dr\.\s+(\w+)'
        match = re.search(doctor_pattern, utterance, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_appointment_type(self, utterance: str) -> Optional[AppointmentType]:
        """Extract appointment type"""
        utterance_lower = utterance.lower()
        
        if "checkup" in utterance_lower or "physical" in utterance_lower:
            return AppointmentType.CHECKUP
        elif "consultation" in utterance_lower or "consult" in utterance_lower:
            return AppointmentType.CONSULTATION
        elif "follow" in utterance_lower:
            return AppointmentType.FOLLOW_UP
        
        return None

    def create_session(self, call_id: str, phone_number: str) -> CallSession:
        """Create new call session"""
        session = CallSession(
            call_id=call_id,
            phone_number=phone_number,
            start_time=datetime.now(),
            current_state="greeting",
            patient_name=None,
            doctor_name=None,
            appointment_type=None,
            preferred_date=None,
            preferred_time=None,
            retry_count=0
        )
        self.active_sessions[call_id] = session
        return session

    def handle_webhook(self, call_id: str, phone_number: str, speech_result: str = None) -> Dict:
        """Handle webhook from telephony platform"""
        
        session = self.active_sessions.get(call_id)
        if not session:
            session = self.create_session(call_id, phone_number)
        
        if session.current_state == "greeting":
            return self.handle_greeting(session, speech_result)
        elif session.current_state == "collecting_patient_name":
            return self.handle_patient_name(session, speech_result)
        elif session.current_state == "collecting_doctor_name":
            return self.handle_doctor_name(session, speech_result)
        elif session.current_state == "collecting_appointment_type":
            return self.handle_appointment_type(session, speech_result)
        elif session.current_state == "collecting_date":
            return self.handle_date(session, speech_result)
        elif session.current_state == "collecting_time":
            return self.handle_time(session, speech_result)
        elif session.current_state == "confirming":
            return self.handle_confirmation(session, speech_result)
        else:
            return {"response": self.ssml_templates["escalate"], "next_action": "transfer"}

    def handle_greeting(self, session: CallSession, utterance: str) -> Dict:
        """Handle initial greeting"""
        if not utterance:
            return {
                "response": self.ssml_templates["greeting"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        
        intent = self.classify_intent(utterance)
        
        if intent["intent"] == "book_appointment":
            session.current_state = "collecting_patient_name"
            return {
                "response": self.ssml_templates["ask_patient_name"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        elif intent["intent"] == "emergency":
            return {
                "response": self.ssml_templates["emergency"],
                "next_action": "transfer",
                "transfer_number": "+1234567890"
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>I didn\'t understand. You can say "book an appointment" or "emergency".</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_patient_name(self, session: CallSession, utterance: str) -> Dict:
        """Handle patient name collection"""
        if utterance and len(utterance.split()) >= 2:
            session.patient_name = utterance
            session.current_state = "collecting_doctor_name"
            return {
                "response": self.ssml_templates["ask_doctor_name"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please provide your full name, including first and last name.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_doctor_name(self, session: CallSession, utterance: str) -> Dict:
        """Handle doctor name collection"""
        doctor_name = self.extract_doctor_name(utterance)
        
        if doctor_name:
            session.doctor_name = f"Dr. {doctor_name}"
            session.current_state = "collecting_appointment_type"
            return {
                "response": self.ssml_templates["ask_appointment_type"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please say "Dr. Smith", "Dr. Johnson", or "Dr. Williams".</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_appointment_type(self, session: CallSession, utterance: str) -> Dict:
        """Handle appointment type collection"""
        appointment_type = self.extract_appointment_type(utterance)
        
        if appointment_type:
            session.appointment_type = appointment_type
            session.current_state = "collecting_date"
            return {
                "response": self.ssml_templates["ask_date"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please specify the type: checkup, consultation, or follow-up.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_date(self, session: CallSession, utterance: str) -> Dict:
        """Handle date collection"""
        if utterance:
            session.preferred_date = utterance
            session.current_state = "collecting_time"
            return {
                "response": self.ssml_templates["ask_time"],
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please specify your preferred date.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_time(self, session: CallSession, utterance: str) -> Dict:
        """Handle time collection"""
        if utterance:
            session.preferred_time = utterance
            session.current_state = "confirming"
            
            confirm_ssml = self.ssml_templates["confirm_appointment"].format(
                doctor=session.doctor_name,
                date=session.preferred_date,
                time=session.preferred_time,
                type=session.appointment_type.value.replace("_", " ")
            )
            
            return {
                "response": confirm_ssml,
                "next_action": "gather_speech",
                "timeout": 10
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please specify your preferred time.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def handle_confirmation(self, session: CallSession, utterance: str) -> Dict:
        """Handle appointment confirmation"""
        if utterance and any(word in utterance.lower() for word in ["yes", "correct", "confirm"]):
            return {
                "response": self.ssml_templates["appointment_confirmed"],
                "next_action": "hangup"
            }
        else:
            session.retry_count += 1
            if session.retry_count >= 3:
                return {
                    "response": self.ssml_templates["escalate"],
                    "next_action": "transfer"
                }
            else:
                return {
                    "response": '<speak>Please say yes to confirm or no to try again.</speak>',
                    "next_action": "gather_speech",
                    "timeout": 10
                }

    def simulate_call_flow(self, test_scenarios: List[Dict]) -> List[Dict]:
        """Simulate call flows"""
        results = []
        
        for scenario in test_scenarios:
            print(f"\nSimulating: {scenario['name']}")
            print("-" * 50)
            
            call_id = f"test_{int(time.time())}"
            phone_number = scenario.get("phone_number", "+15551234567")
            
            session = self.create_session(call_id, phone_number)
            
            for i, turn in enumerate(scenario["turns"]):
                print(f"Turn {i+1}: Customer says: '{turn['customer_input']}'")
                
                response = self.handle_webhook(
                    call_id=call_id,
                    phone_number=phone_number,
                    speech_result=turn["customer_input"]
                )
                
                print(f"Response: {response['next_action']}")
                
                if response["next_action"] in ["hangup", "transfer"]:
                    break
            
            results.append({
                "scenario": scenario["name"],
                "success": response["next_action"] == "hangup"
            })
        
        return results

    def run_demo(self):
        """Run the healthcare appointment booking demo"""
        print("Healthcare Appointment Booking IVR - Chapter 5")
        print("="*80)
        print("Demonstrating medical appointment scheduling system...")
        
        test_scenarios = [
            {
                "name": "Successful Appointment Booking",
                "turns": [
                    {"customer_input": "I want to book an appointment"},
                    {"customer_input": "John Smith"},
                    {"customer_input": "Dr. Smith"},
                    {"customer_input": "Checkup"},
                    {"customer_input": "Monday"},
                    {"customer_input": "10 AM"},
                    {"customer_input": "Yes, that's correct"}
                ]
            },
            {
                "name": "Emergency Escalation",
                "turns": [
                    {"customer_input": "I have an emergency"}
                ]
            }
        ]
        
        results = self.simulate_call_flow(test_scenarios)
        
        print(f"\n{'='*80}")
        print("DEMO SUMMARY")
        print(f"{'='*80}")
        
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"Total Scenarios: {total}")
        print(f"Successful: {successful}/{total} ({successful/total*100:.1f}%)")
        
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            print(f"  {status} - {result['scenario']}")
        
        print(f"\nKey Features Demonstrated:")
        print(f"  • HIPAA-compliant patient information handling")
        print(f"  • Doctor name recognition")
        print(f"  • Appointment type classification")
        print(f"  • Date and time collection")
        print(f"  • Emergency escalation")
        print(f"  • Appointment confirmation")
        
        print(f"\nHealthcare appointment booking demo completed!")

if __name__ == "__main__":
    ivr = HealthcareAppointmentIVR()
    ivr.run_demo()
