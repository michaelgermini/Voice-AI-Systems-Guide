#!/usr/bin/env python3
"""
Call Flow Simulator - Chapter 3
Demonstrates complete voice AI call flow from telephony to business logic.
"""

import os
import time
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallState(Enum):
    """States for call flow simulation"""
    RINGING = "ringing"
    ANSWERED = "answered"
    GREETING = "greeting"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"
    COLLECTING = "collecting"
    TRANSFERRING = "transferring"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class CallEvent:
    """Represents an event in the call flow"""
    timestamp: datetime
    state: CallState
    event_type: str
    data: Dict
    duration_ms: float

@dataclass
class SimulatedCall:
    """Represents a simulated call session"""
    call_id: str
    phone_number: str
    start_time: datetime
    current_state: CallState
    events: List[CallEvent]
    conversation_history: List[Dict]
    session_data: Dict
    metrics: Dict

class CallFlowSimulator:
    """Simulates complete voice AI call flows"""
    
    def __init__(self):
        # Define call scenarios
        self.call_scenarios = [
            {
                "name": "Balance Check Success",
                "phone_number": "+15551234567",
                "customer_utterances": [
                    "I want to check my account balance",
                    "1234",
                    "No, that's all I need"
                ],
                "expected_flow": ["greeting", "intent_recognition", "authentication", "balance_lookup", "completion"]
            },
            {
                "name": "Password Reset Flow",
                "phone_number": "+15559876543",
                "customer_utterances": [
                    "I forgot my password and can't log in",
                    "john.doe@email.com",
                    "Yes, please send it"
                ],
                "expected_flow": ["greeting", "intent_recognition", "email_collection", "confirmation", "completion"]
            },
            {
                "name": "Agent Escalation",
                "phone_number": "+15551111111",
                "customer_utterances": [
                    "I need to speak with a human agent",
                    "This is urgent"
                ],
                "expected_flow": ["greeting", "intent_recognition", "escalation", "transfer"]
            },
            {
                "name": "Complex Issue",
                "phone_number": "+15552222222",
                "customer_utterances": [
                    "My app keeps crashing when I try to make a payment",
                    "The error message says invalid credentials",
                    "I've tried everything"
                ],
                "expected_flow": ["greeting", "intent_recognition", "issue_collection", "escalation", "transfer"]
            }
        ]
        
        # Performance thresholds
        self.performance_thresholds = {
            "stt_latency_ms": 500,
            "nlp_latency_ms": 200,
            "tts_latency_ms": 800,
            "total_round_trip_ms": 1500
        }

    def simulate_stt(self, audio_input: str) -> Tuple[str, float, float]:
        """Simulate Speech-to-Text processing"""
        start_time = time.time()
        
        # Simulate processing time based on input length
        processing_time = len(audio_input) * 0.01 + 0.1
        time.sleep(processing_time)
        
        # Simulate accuracy based on input clarity
        accuracy = 0.95 if len(audio_input) > 10 else 0.85
        
        # Simulate transcription errors
        transcription = audio_input
        if "balance" in audio_input.lower() and accuracy < 0.9:
            transcription = audio_input.replace("balance", "ballance")
        
        latency = (time.time() - start_time) * 1000
        
        return transcription, accuracy, latency

    def simulate_nlp(self, text: str) -> Tuple[str, Dict, float]:
        """Simulate Natural Language Processing"""
        start_time = time.time()
        
        # Simulate processing time
        processing_time = len(text) * 0.005 + 0.05
        time.sleep(processing_time)
        
        # Intent classification
        text_lower = text.lower()
        if any(word in text_lower for word in ["balance", "account balance", "how much"]):
            intent = "check_balance"
            confidence = 0.92
        elif any(word in text_lower for word in ["password", "reset", "forgot", "can't log in"]):
            intent = "reset_password"
            confidence = 0.89
        elif any(word in text_lower for word in ["agent", "human", "person", "representative"]):
            intent = "escalate_agent"
            confidence = 0.87
        elif any(word in text_lower for word in ["problem", "issue", "not working", "crash", "error"]):
            intent = "report_issue"
            confidence = 0.85
        else:
            intent = "unknown"
            confidence = 0.45
        
        # Entity extraction
        entities = {}
        if "1234" in text or "5678" in text:
            entities["ssn_last4"] = "1234" if "1234" in text else "5678"
        if "@" in text:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                entities["email"] = emails[0]
        
        latency = (time.time() - start_time) * 1000
        
        return intent, {"entities": entities, "confidence": confidence}, latency

    def simulate_tts(self, text: str, voice: str = "Polly.Joanna") -> Tuple[str, float]:
        """Simulate Text-to-Speech generation"""
        start_time = time.time()
        
        # Simulate processing time
        processing_time = len(text) * 0.002 + 0.1
        time.sleep(processing_time)
        
        # Generate audio URL (simulated)
        audio_url = f"https://tts.example.com/audio/{int(time.time())}.wav"
        
        latency = (time.time() - start_time) * 1000
        
        return audio_url, latency

    def simulate_business_logic(self, intent: str, entities: Dict, session_data: Dict) -> Tuple[str, Dict]:
        """Simulate business logic processing"""
        start_time = time.time()
        
        # Simulate processing time
        time.sleep(0.1)
        
        response_text = ""
        business_data = {}
        
        if intent == "check_balance":
            if "ssn_last4" in entities:
                # Simulate balance lookup
                balance = "$2,456.78"
                response_text = f"Thank you. Your account balance is {balance}. Is there anything else I can help you with?"
                business_data = {"balance": balance, "account_verified": True}
            else:
                response_text = "I can help you check your balance. For security, I'll need to verify your identity. What's the last 4 digits of your social security number?"
                business_data = {"requires_authentication": True}
        
        elif intent == "reset_password":
            if "email" in entities:
                # Simulate password reset
                response_text = f"I've sent a password reset link to {entities['email']}. Check your inbox and follow the instructions. Is there anything else I can help you with?"
                business_data = {"password_reset_sent": True, "email": entities["email"]}
            else:
                response_text = "I understand you need to reset your password. What email address is associated with your account?"
                business_data = {"requires_email": True}
        
        elif intent == "escalate_agent":
            response_text = "I'm connecting you with a human agent who can better assist you. Please hold."
            business_data = {"escalation_reason": "customer_request", "agent_available": True}
        
        elif intent == "report_issue":
            response_text = "I understand you're experiencing an issue. Let me connect you with a technical specialist who can help resolve this."
            business_data = {"issue_type": "technical", "escalation_reason": "technical_issue"}
        
        else:
            response_text = "I didn't understand that. Let me connect you with a human agent who can help."
            business_data = {"escalation_reason": "unknown_intent"}
        
        latency = (time.time() - start_time) * 1000
        
        return response_text, business_data

    def simulate_call_flow(self, scenario: Dict) -> SimulatedCall:
        """Simulate a complete call flow"""
        call_id = f"call_{int(time.time())}"
        phone_number = scenario["phone_number"]
        
        # Initialize call
        call = SimulatedCall(
            call_id=call_id,
            phone_number=phone_number,
            start_time=datetime.now(),
            current_state=CallState.RINGING,
            events=[],
            conversation_history=[],
            session_data={},
            metrics={}
        )
        
        logger.info(f"Starting call simulation: {scenario['name']}")
        
        # Call ringing
        self.add_event(call, CallState.RINGING, "call_ringing", {"duration": 2000})
        
        # Call answered
        self.add_event(call, CallState.ANSWERED, "call_answered", {})
        
        # Initial greeting
        greeting_text = "Welcome to our AI-powered customer service. How can I help you today?"
        tts_url, tts_latency = self.simulate_tts(greeting_text)
        self.add_event(call, CallState.GREETING, "tts_generated", {
            "text": greeting_text,
            "audio_url": tts_url,
            "latency_ms": tts_latency
        })
        
        # Process customer utterances
        for i, utterance in enumerate(scenario["customer_utterances"]):
            logger.info(f"Processing utterance {i+1}: '{utterance}'")
            
            # Listening state
            self.add_event(call, CallState.LISTENING, "listening", {"duration": 1000})
            
            # STT processing
            transcription, accuracy, stt_latency = self.simulate_stt(utterance)
            self.add_event(call, CallState.PROCESSING, "stt_completed", {
                "original": utterance,
                "transcription": transcription,
                "accuracy": accuracy,
                "latency_ms": stt_latency
            })
            
            # NLP processing
            intent, nlp_data, nlp_latency = self.simulate_nlp(transcription)
            self.add_event(call, CallState.PROCESSING, "nlp_completed", {
                "intent": intent,
                "entities": nlp_data["entities"],
                "confidence": nlp_data["confidence"],
                "latency_ms": nlp_latency
            })
            
            # Business logic
            response_text, business_data = self.simulate_business_logic(
                intent, nlp_data["entities"], call.session_data
            )
            self.add_event(call, CallState.PROCESSING, "business_logic_completed", {
                "response_text": response_text,
                "business_data": business_data
            })
            
            # Update session data
            call.session_data.update(business_data)
            call.session_data.update(nlp_data["entities"])
            
            # TTS generation
            tts_url, tts_latency = self.simulate_tts(response_text)
            self.add_event(call, CallState.RESPONDING, "tts_generated", {
                "text": response_text,
                "audio_url": tts_url,
                "latency_ms": tts_latency
            })
            
            # Log conversation
            call.conversation_history.append({
                "turn": i + 1,
                "customer": utterance,
                "transcription": transcription,
                "intent": intent,
                "ai_response": response_text,
                "timestamp": datetime.now()
            })
            
            # Check if escalation is needed
            if "escalation_reason" in business_data:
                self.add_event(call, CallState.TRANSFERRING, "escalation_triggered", {
                    "reason": business_data["escalation_reason"]
                })
                break
        
        # Call completion
        if call.current_state != CallState.TRANSFERRING:
            self.add_event(call, CallState.COMPLETED, "call_completed", {})
        
        # Calculate metrics
        call.metrics = self.calculate_call_metrics(call)
        
        logger.info(f"Call simulation completed: {scenario['name']}")
        return call

    def add_event(self, call: SimulatedCall, state: CallState, event_type: str, data: Dict):
        """Add event to call history"""
        if call.events:
            duration = (datetime.now() - call.events[-1].timestamp).total_seconds() * 1000
        else:
            duration = 0
        
        event = CallEvent(
            timestamp=datetime.now(),
            state=state,
            event_type=event_type,
            data=data,
            duration_ms=duration
        )
        
        call.events.append(event)
        call.current_state = state

    def calculate_call_metrics(self, call: SimulatedCall) -> Dict:
        """Calculate performance metrics for the call"""
        total_duration = (call.events[-1].timestamp - call.events[0].timestamp).total_seconds()
        
        # Extract latencies
        stt_latencies = [e.data.get("latency_ms", 0) for e in call.events if e.event_type == "stt_completed"]
        nlp_latencies = [e.data.get("latency_ms", 0) for e in call.events if e.event_type == "nlp_completed"]
        tts_latencies = [e.data.get("latency_ms", 0) for e in call.events if e.event_type == "tts_generated"]
        
        # Calculate averages
        avg_stt_latency = sum(stt_latencies) / len(stt_latencies) if stt_latencies else 0
        avg_nlp_latency = sum(nlp_latencies) / len(nlp_latencies) if nlp_latencies else 0
        avg_tts_latency = sum(tts_latencies) / len(tts_latencies) if tts_latencies else 0
        
        # Check performance thresholds
        performance_issues = []
        if avg_stt_latency > self.performance_thresholds["stt_latency_ms"]:
            performance_issues.append("STT latency too high")
        if avg_nlp_latency > self.performance_thresholds["nlp_latency_ms"]:
            performance_issues.append("NLP latency too high")
        if avg_tts_latency > self.performance_thresholds["tts_latency_ms"]:
            performance_issues.append("TTS latency too high")
        
        return {
            "total_duration_seconds": total_duration,
            "total_events": len(call.events),
            "conversation_turns": len(call.conversation_history),
            "avg_stt_latency_ms": avg_stt_latency,
            "avg_nlp_latency_ms": avg_nlp_latency,
            "avg_tts_latency_ms": avg_tts_latency,
            "performance_issues": performance_issues,
            "final_state": call.current_state.value,
            "success": call.current_state in [CallState.COMPLETED, CallState.TRANSFERRING]
        }

    def print_call_summary(self, call: SimulatedCall, scenario_name: str):
        """Print detailed call summary"""
        print(f"\n{'='*80}")
        print(f"CALL FLOW SIMULATION: {scenario_name}")
        print(f"{'='*80}")
        
        print(f"\nCall Details:")
        print(f"   Call ID: {call.call_id}")
        print(f"   Phone Number: {call.phone_number}")
        print(f"   Duration: {call.metrics['total_duration_seconds']:.1f} seconds")
        print(f"   Final State: {call.metrics['final_state']}")
        print(f"   Success: {'PASS' if call.metrics['success'] else 'FAIL'}")
        
        print(f"\nPerformance Metrics:")
        print(f"   Average STT Latency: {call.metrics['avg_stt_latency_ms']:.1f}ms")
        print(f"   Average NLP Latency: {call.metrics['avg_nlp_latency_ms']:.1f}ms")
        print(f"   Average TTS Latency: {call.metrics['avg_tts_latency_ms']:.1f}ms")
        print(f"   Total Events: {call.metrics['total_events']}")
        print(f"   Conversation Turns: {call.metrics['conversation_turns']}")
        
        if call.metrics['performance_issues']:
            print(f"\nPerformance Issues:")
            for issue in call.metrics['performance_issues']:
                print(f"   • {issue}")
        
        print(f"\nConversation Flow:")
        for i, turn in enumerate(call.conversation_history, 1):
            print(f"   Turn {i}:")
            print(f"     Customer: '{turn['customer']}'")
            print(f"     Transcription: '{turn['transcription']}'")
            print(f"     Intent: {turn['intent']}")
            print(f"     AI Response: '{turn['ai_response']}'")
        
        print(f"\nEvent Timeline:")
        for event in call.events:
            print(f"   {event.timestamp.strftime('%H:%M:%S.%f')[:-3]} - {event.state.value}: {event.event_type}")

    def run_simulation(self):
        """Run complete call flow simulation"""
        print("Call Flow Simulator - Chapter 3")
        print("="*50)
        print("Simulating complete voice AI call flows...")
        
        results = []
        
        for scenario in self.call_scenarios:
            print(f"\nRunning Scenario: {scenario['name']}")
            print("-" * 50)
            
            # Simulate call
            call = self.simulate_call_flow(scenario)
            results.append((scenario, call))
            
            # Print summary
            self.print_call_summary(call, scenario['name'])
        
        # Print overall results
        self.print_overall_results(results)
        
        print(f"\nCall flow simulation completed!")
        print("   This demonstrates the complete voice AI pipeline in action.")

    def print_overall_results(self, results: List[Tuple[Dict, SimulatedCall]]):
        """Print overall simulation results"""
        print(f"\n{'='*80}")
        print("OVERALL SIMULATION RESULTS")
        print(f"{'='*80}")
        
        total_calls = len(results)
        successful_calls = sum(1 for _, call in results if call.metrics['success'])
        avg_duration = sum(call.metrics['total_duration_seconds'] for _, call in results) / total_calls
        
        print(f"\nSummary:")
        print(f"   Total Calls: {total_calls}")
        print(f"   Successful: {successful_calls}/{total_calls} ({successful_calls/total_calls*100:.1f}%)")
        print(f"   Average Duration: {avg_duration:.1f} seconds")
        
        print(f"\nPerformance Analysis:")
        all_stt_latencies = [call.metrics['avg_stt_latency_ms'] for _, call in results]
        all_nlp_latencies = [call.metrics['avg_nlp_latency_ms'] for _, call in results]
        all_tts_latencies = [call.metrics['avg_tts_latency_ms'] for _, call in results]
        
        print(f"   Average STT Latency: {sum(all_stt_latencies)/len(all_stt_latencies):.1f}ms")
        print(f"   Average NLP Latency: {sum(all_nlp_latencies)/len(all_nlp_latencies):.1f}ms")
        print(f"   Average TTS Latency: {sum(all_tts_latencies)/len(all_tts_latencies):.1f}ms")
        
        print(f"\nRecommendations:")
        if any(call.metrics['performance_issues'] for _, call in results):
            print("   • Optimize latency for better user experience")
        else:
            print("   • Performance meets all thresholds")
        
        if successful_calls == total_calls:
            print("   • All calls completed successfully")
        else:
            print("   • Review failed call flows for improvement")

if __name__ == "__main__":
    simulator = CallFlowSimulator()
    simulator.run_simulation()
