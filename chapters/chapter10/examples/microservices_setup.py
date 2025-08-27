#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Example: Basic Microservices Setup

This example demonstrates how to decompose a voice AI system into
independent microservices that can scale independently.
"""

import time
import json
import uuid
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import random

@dataclass
class CallRequest:
    call_id: str
    audio_data: bytes
    user_id: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class CallResponse:
    call_id: str
    text_response: str
    audio_response: bytes
    processing_time_ms: float
    services_used: List[str]
    timestamp: datetime

class STTService:
    """Speech-to-Text Microservice"""
    
    def __init__(self, service_id: str = None):
        self.service_id = service_id or f"stt-{uuid.uuid4().hex[:8]}"
        self.request_count = 0
        self.avg_latency_ms = 150
    
    async def transcribe(self, audio_data: bytes) -> Dict[str, Any]:
        """Simulate STT processing"""
        start_time = time.time()
        self.request_count += 1
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # Simulate transcription result
        transcriptions = [
            "I need help with my order",
            "What's my account balance?",
            "I want to speak to a representative",
            "Can you help me reset my password?",
            "I have a billing question"
        ]
        
        result = {
            "text": random.choice(transcriptions),
            "confidence": random.uniform(0.85, 0.98),
            "language": "en-US",
            "service_id": self.service_id
        }
        
        processing_time = (time.time() - start_time) * 1000
        self.avg_latency_ms = (self.avg_latency_ms + processing_time) / 2
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_type": "STT",
            "request_count": self.request_count,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "status": "healthy"
        }

class NLPService:
    """Natural Language Processing Microservice"""
    
    def __init__(self, service_id: str = None):
        self.service_id = service_id or f"nlp-{uuid.uuid4().hex[:8]}"
        self.request_count = 0
        self.avg_latency_ms = 50
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Simulate NLP processing"""
        start_time = time.time()
        self.request_count += 1
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.05, 0.15))
        
        # Simulate intent recognition
        intents = {
            "I need help with my order": {
                "intent": "order_support",
                "confidence": 0.92,
                "entities": [{"type": "request_type", "value": "help"}]
            },
            "What's my account balance?": {
                "intent": "check_balance",
                "confidence": 0.95,
                "entities": [{"type": "account_type", "value": "balance"}]
            },
            "I want to speak to a representative": {
                "intent": "human_escalation",
                "confidence": 0.88,
                "entities": [{"type": "escalation_type", "value": "human"}]
            },
            "Can you help me reset my password?": {
                "intent": "password_reset",
                "confidence": 0.90,
                "entities": [{"type": "action", "value": "reset"}]
            },
            "I have a billing question": {
                "intent": "billing_support",
                "confidence": 0.87,
                "entities": [{"type": "topic", "value": "billing"}]
            }
        }
        
        result = intents.get(text, {
            "intent": "unknown",
            "confidence": 0.5,
            "entities": []
        })
        result["service_id"] = self.service_id
        
        processing_time = (time.time() - start_time) * 1000
        self.avg_latency_ms = (self.avg_latency_ms + processing_time) / 2
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_type": "NLP",
            "request_count": self.request_count,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "status": "healthy"
        }

class TTSService:
    """Text-to-Speech Microservice"""
    
    def __init__(self, service_id: str = None):
        self.service_id = service_id or f"tts-{uuid.uuid4().hex[:8]}"
        self.request_count = 0
        self.avg_latency_ms = 200
    
    async def synthesize(self, text: str, voice: str = "en-US-JennyNeural") -> Dict[str, Any]:
        """Simulate TTS processing"""
        start_time = time.time()
        self.request_count += 1
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.2, 0.4))
        
        # Generate response based on intent
        responses = {
            "order_support": "I'd be happy to help you with your order. Can you provide your order number?",
            "check_balance": "I can help you check your account balance. Please provide your account number.",
            "human_escalation": "I understand you'd like to speak with a representative. Let me connect you now.",
            "password_reset": "I can help you reset your password. I'll need to verify your identity first.",
            "billing_support": "I can assist with your billing question. What specific issue are you experiencing?",
            "unknown": "I'm sorry, I didn't understand that. Could you please rephrase your request?"
        }
        
        # Extract intent from text (simplified)
        intent = "unknown"
        if "order" in text.lower():
            intent = "order_support"
        elif "balance" in text.lower():
            intent = "check_balance"
        elif "representative" in text.lower() or "human" in text.lower():
            intent = "human_escalation"
        elif "password" in text.lower():
            intent = "password_reset"
        elif "billing" in text.lower():
            intent = "billing_support"
        
        response_text = responses.get(intent, responses["unknown"])
        
        result = {
            "audio_data": f"simulated_audio_{uuid.uuid4().hex[:8]}.mp3",
            "text": response_text,
            "voice": voice,
            "duration_ms": len(response_text) * 50,  # Rough estimate
            "service_id": self.service_id
        }
        
        processing_time = (time.time() - start_time) * 1000
        self.avg_latency_ms = (self.avg_latency_ms + processing_time) / 2
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_type": "TTS",
            "request_count": self.request_count,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "status": "healthy"
        }

class SessionService:
    """Session Management Microservice"""
    
    def __init__(self, service_id: str = None):
        self.service_id = service_id or f"session-{uuid.uuid4().hex[:8]}"
        self.sessions = {}
        self.request_count = 0
    
    async def create_session(self, call_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new session"""
        self.request_count += 1
        
        session = {
            "session_id": f"session-{uuid.uuid4().hex[:8]}",
            "call_id": call_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "context": {},
            "conversation_history": []
        }
        
        self.sessions[call_id] = session
        return session
    
    async def update_session(self, call_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update session data"""
        self.request_count += 1
        
        if call_id in self.sessions:
            self.sessions[call_id].update(updates)
            self.sessions[call_id]["last_activity"] = datetime.utcnow().isoformat()
            return self.sessions[call_id]
        return None
    
    async def get_session(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        self.request_count += 1
        return self.sessions.get(call_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_type": "Session",
            "request_count": self.request_count,
            "active_sessions": len(self.sessions),
            "status": "healthy"
        }

class VoiceAIService:
    """Main Voice AI Service that orchestrates microservices"""
    
    def __init__(self):
        # Initialize microservices
        self.stt_service = STTService()
        self.nlp_service = NLPService()
        self.tts_service = TTSService()
        self.session_service = SessionService()
        
        self.services = [
            self.stt_service,
            self.nlp_service,
            self.tts_service,
            self.session_service
        ]
    
    async def process_call(self, call_request: CallRequest) -> CallResponse:
        """Process a complete voice call through all microservices"""
        start_time = time.time()
        services_used = []
        
        try:
            # Step 1: Create session
            session = await self.session_service.create_session(
                call_request.call_id, 
                call_request.user_id
            )
            services_used.append("session")
            
            # Step 2: Speech-to-Text
            stt_result = await self.stt_service.transcribe(call_request.audio_data)
            services_used.append("stt")
            
            # Step 3: Natural Language Processing
            nlp_result = await self.nlp_service.analyze(stt_result["text"])
            services_used.append("nlp")
            
            # Step 4: Text-to-Speech
            tts_result = await self.tts_service.synthesize(nlp_result.get("response", "I'm sorry, I didn't understand that."))
            services_used.append("tts")
            
            # Step 5: Update session with conversation history
            await self.session_service.update_session(call_request.call_id, {
                "conversation_history": [
                    {"role": "user", "text": stt_result["text"], "timestamp": datetime.utcnow().isoformat()},
                    {"role": "assistant", "text": tts_result["text"], "timestamp": datetime.utcnow().isoformat()}
                ]
            })
            
            processing_time = (time.time() - start_time) * 1000
            
            return CallResponse(
                call_id=call_request.call_id,
                text_response=tts_result["text"],
                audio_response=tts_result["audio_data"].encode(),
                processing_time_ms=processing_time,
                services_used=services_used,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            # Handle errors gracefully
            error_response = f"I'm sorry, I encountered an error: {str(e)}"
            return CallResponse(
                call_id=call_request.call_id,
                text_response=error_response,
                audio_response=b"error_audio",
                processing_time_ms=(time.time() - start_time) * 1000,
                services_used=services_used,
                timestamp=datetime.utcnow()
            )
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics from all microservices"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "services": [service.get_metrics() for service in self.services],
            "total_requests": sum(service.request_count for service in self.services)
        }

async def simulate_microservices_demo():
    """Demonstrate microservices architecture"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Example: Basic Microservices Setup")
    print("=" * 60)
    
    # Initialize Voice AI Service
    voice_ai = VoiceAIService()
    
    print("\n1. Initializing Microservices:")
    for service in voice_ai.services:
        metrics = service.get_metrics()
        print(f"   - {metrics['service_type']} Service: {metrics['service_id']}")
    
    print("\n2. Processing Sample Calls:")
    
    # Simulate multiple calls
    sample_calls = [
        CallRequest(call_id=f"call-{i}", audio_data=b"sample_audio", user_id=f"user-{i}")
        for i in range(1, 6)
    ]
    
    results = []
    for call_request in sample_calls:
        print(f"\n   Processing Call {call_request.call_id}:")
        
        response = await voice_ai.process_call(call_request)
        results.append(response)
        
        print(f"     - STT: '{response.text_response[:50]}...'")
        print(f"     - Processing Time: {response.processing_time_ms:.2f}ms")
        print(f"     - Services Used: {', '.join(response.services_used)}")
    
    print("\n3. Service Metrics:")
    metrics = voice_ai.get_all_metrics()
    
    for service_metrics in metrics["services"]:
        print(f"   {service_metrics['service_type']} Service:")
        print(f"     - Requests: {service_metrics['request_count']}")
        print(f"     - Avg Latency: {service_metrics.get('avg_latency_ms', 'N/A')}ms")
        if 'active_sessions' in service_metrics:
            print(f"     - Active Sessions: {service_metrics['active_sessions']}")
    
    print(f"\n   Total Requests: {metrics['total_requests']}")
    
    print("\n4. Microservices Benefits Demonstrated:")
    print("   ✓ Independent scaling of each service")
    print("   ✓ Isolated failure domains")
    print("   ✓ Technology diversity (each service can use different tech)")
    print("   ✓ Independent deployment and updates")
    print("   ✓ Granular monitoring and metrics")
    
    print("\n5. Scaling Considerations:")
    print("   - STT Service: High CPU usage, scale based on audio processing")
    print("   - NLP Service: Moderate CPU, scale based on text analysis")
    print("   - TTS Service: High CPU usage, scale based on speech synthesis")
    print("   - Session Service: High memory usage, scale based on active sessions")
    
    return voice_ai

if __name__ == "__main__":
    asyncio.run(simulate_microservices_demo())
