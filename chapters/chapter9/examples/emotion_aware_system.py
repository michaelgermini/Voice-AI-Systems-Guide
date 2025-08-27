#!/usr/bin/env python3
"""
Chapter 9 - The Future of Voice AI in Contact Centers
Emotion-Aware System Demo

This script demonstrates advanced emotion detection and response including:
- Real-time emotion analysis
- Proactive intervention
- Sentiment-driven optimization
- Emotional routing
"""

import json
import time
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    FRUSTRATION = "frustration"
    ANXIETY = "anxiety"
    EXCITEMENT = "excitement"

class StressLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class InterventionType(Enum):
    NONE = "none"
    DE_ESCALATION = "de_escalation"
    ESCALATION = "escalation"
    EMPATHY = "empathy"
    CLARIFICATION = "clarification"
    PROACTIVE_HELP = "proactive_help"

@dataclass
class EmotionalState:
    """Current emotional state of the customer"""
    primary_emotion: EmotionType
    secondary_emotion: Optional[EmotionType] = None
    intensity: float = 0.5  # 0.0 to 1.0
    confidence: float = 0.8  # 0.0 to 1.0
    stress_level: StressLevel = StressLevel.LOW
    engagement_level: float = 0.7  # 0.0 to 1.0
    trust_indicators: List[str] = None
    micro_expressions: List[str] = None

@dataclass
class EmotionalTrigger:
    """Trigger that caused emotional change"""
    trigger_type: str  # "voice_tone", "content", "system_response", "wait_time"
    description: str
    timestamp: datetime
    impact_score: float  # 0.0 to 1.0

@dataclass
class InterventionAction:
    """Action taken based on emotional analysis"""
    intervention_type: InterventionType
    description: str
    timestamp: datetime
    success_probability: float
    agent_skills_required: List[str]
    escalation_priority: int  # 1-5, 5 being highest

@dataclass
class EmotionSession:
    """Emotion tracking session"""
    session_id: str
    customer_id: str
    start_time: datetime
    emotional_states: List[EmotionalState]
    triggers: List[EmotionalTrigger]
    interventions: List[InterventionAction]
    escalation_events: List[Dict[str, Any]]
    current_emotion: EmotionalState

class EmotionAwareSystem:
    """Advanced emotion-aware voice AI system"""
    
    def __init__(self):
        self.active_sessions: Dict[str, EmotionSession] = {}
        self.emotion_patterns = {}
        self.intervention_strategies = {}
        self.agent_skills_database = {}
        self.load_emotion_data()
    
    def load_emotion_data(self):
        """Load emotion patterns and intervention strategies"""
        self.emotion_patterns = {
            EmotionType.FRUSTRATION: {
                "triggers": ["long_wait", "repetitive_questions", "system_errors"],
                "escalation_risk": "high",
                "de_escalation_techniques": ["acknowledge_frustration", "offer_immediate_help", "apologize"],
                "agent_skills": ["de_escalation", "patience", "problem_solving"]
            },
            EmotionType.ANXIETY: {
                "triggers": ["complex_processes", "uncertainty", "technical_issues"],
                "escalation_risk": "medium",
                "de_escalation_techniques": ["provide_clarity", "step_by_step_guidance", "reassurance"],
                "agent_skills": ["empathy", "clarity", "technical_expertise"]
            },
            EmotionType.ANGER: {
                "triggers": ["billing_errors", "service_outages", "incompetent_agents"],
                "escalation_risk": "critical",
                "de_escalation_techniques": ["immediate_escalation", "supervisor_involvement", "compensation_offers"],
                "agent_skills": ["crisis_management", "supervisor_skills", "compensation_authority"]
            },
            EmotionType.EXCITEMENT: {
                "triggers": ["new_features", "positive_outcomes", "quick_resolutions"],
                "escalation_risk": "low",
                "de_escalation_techniques": ["capitalize_on_momentum", "offer_additional_help", "positive_reinforcement"],
                "agent_skills": ["enthusiasm", "product_knowledge", "upselling"]
            }
        }
        
        self.intervention_strategies = {
            InterventionType.DE_ESCALATION: {
                "techniques": ["active_listening", "empathy_statements", "solution_focus"],
                "success_rate": 0.85,
                "time_to_effect": 30  # seconds
            },
            InterventionType.ESCALATION: {
                "techniques": ["supervisor_transfer", "specialist_routing", "priority_handling"],
                "success_rate": 0.95,
                "time_to_effect": 60  # seconds
            },
            InterventionType.EMPATHY: {
                "techniques": ["emotional_validation", "personal_connection", "understanding_statements"],
                "success_rate": 0.78,
                "time_to_effect": 45  # seconds
            },
            InterventionType.CLARIFICATION: {
                "techniques": ["step_by_step_explanation", "visual_aids", "confirmation_checks"],
                "success_rate": 0.82,
                "time_to_effect": 40  # seconds
            },
            InterventionType.PROACTIVE_HELP: {
                "techniques": ["anticipate_needs", "offer_solutions", "prevent_issues"],
                "success_rate": 0.88,
                "time_to_effect": 20  # seconds
            }
        }
        
        self.agent_skills_database = {
            "de_escalation": ["empathy", "patience", "crisis_management"],
            "technical_expertise": ["product_knowledge", "troubleshooting", "problem_solving"],
            "billing_specialist": ["payment_processing", "account_management", "dispute_resolution"],
            "supervisor": ["team_management", "escalation_authority", "compensation_approval"],
            "empathy": ["emotional_intelligence", "active_listening", "personal_connection"]
        }
    
    def start_emotion_session(self, customer_id: str) -> str:
        """Start emotion tracking for a customer"""
        session_id = f"emotion_{customer_id}_{int(time.time())}"
        
        initial_emotion = EmotionalState(
            primary_emotion=EmotionType.NEUTRAL,
            intensity=0.3,
            confidence=0.9,
            stress_level=StressLevel.LOW,
            engagement_level=0.8,
            trust_indicators=["cooperative_tone", "clear_communication"],
            micro_expressions=["neutral_expression"]
        )
        
        session = EmotionSession(
            session_id=session_id,
            customer_id=customer_id,
            start_time=datetime.now(),
            emotional_states=[initial_emotion],
            triggers=[],
            interventions=[],
            escalation_events=[],
            current_emotion=initial_emotion
        )
        
        self.active_sessions[session_id] = session
        print(f"Started emotion tracking session {session_id}")
        
        return session_id
    
    def analyze_voice_emotion(self, audio_sample: str, session_id: str) -> EmotionalState:
        """Analyze emotion from voice sample"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        # Simulated emotion analysis
        emotions = list(EmotionType)
        stress_levels = list(StressLevel)
        
        # Simulate emotional progression based on session duration
        session_duration = (datetime.now() - session.start_time).total_seconds()
        
        # Simulate increasing frustration over time (for demo purposes)
        if session_duration > 120:  # After 2 minutes
            primary_emotion = EmotionType.FRUSTRATION
            intensity = min(0.8, 0.3 + (session_duration - 120) / 300)  # Gradual increase
            stress_level = StressLevel.MEDIUM if intensity > 0.5 else StressLevel.LOW
        else:
            primary_emotion = random.choice(emotions)
            intensity = random.uniform(0.2, 0.7)
            stress_level = random.choice(stress_levels)
        
        # Generate trust indicators and micro-expressions
        trust_indicators = []
        micro_expressions = []
        
        if primary_emotion == EmotionType.FRUSTRATION:
            trust_indicators = ["defensive_tone", "short_responses"]
            micro_expressions = ["furrowed_brow", "tightened_jaw"]
        elif primary_emotion == EmotionType.EXCITEMENT:
            trust_indicators = ["enthusiastic_tone", "engaged_responses"]
            micro_expressions = ["raised_eyebrows", "smile"]
        elif primary_emotion == EmotionType.ANXIETY:
            trust_indicators = ["hesitant_speech", "uncertain_tone"]
            micro_expressions = ["fidgeting", "avoiding_eye_contact"]
        
        emotional_state = EmotionalState(
            primary_emotion=primary_emotion,
            secondary_emotion=random.choice(emotions) if random.random() > 0.7 else None,
            intensity=intensity,
            confidence=random.uniform(0.7, 0.95),
            stress_level=stress_level,
            engagement_level=random.uniform(0.4, 0.9),
            trust_indicators=trust_indicators,
            micro_expressions=micro_expressions
        )
        
        # Update session
        session.emotional_states.append(emotional_state)
        session.current_emotion = emotional_state
        
        return emotional_state
    
    def detect_emotional_triggers(self, session_id: str, event_type: str, 
                                event_description: str) -> List[EmotionalTrigger]:
        """Detect emotional triggers from events"""
        if session_id not in self.active_sessions:
            return []
        
        session = self.active_sessions[session_id]
        
        # Analyze event for potential triggers
        triggers = []
        impact_score = 0.0
        
        if "wait" in event_description.lower():
            impact_score = 0.6
            triggers.append(EmotionalTrigger(
                trigger_type="wait_time",
                description="Customer experienced waiting time",
                timestamp=datetime.now(),
                impact_score=impact_score
            ))
        
        elif "error" in event_description.lower():
            impact_score = 0.8
            triggers.append(EmotionalTrigger(
                trigger_type="system_error",
                description="System error occurred",
                timestamp=datetime.now(),
                impact_score=impact_score
            ))
        
        elif "repeat" in event_description.lower():
            impact_score = 0.7
            triggers.append(EmotionalTrigger(
                trigger_type="repetitive_questions",
                description="Customer had to repeat information",
                timestamp=datetime.now(),
                impact_score=impact_score
            ))
        
        # Add triggers to session
        session.triggers.extend(triggers)
        
        return triggers
    
    def determine_intervention(self, session_id: str) -> InterventionAction:
        """Determine appropriate intervention based on emotional state"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        current_emotion = session.current_emotion
        
        # Get emotion pattern
        pattern = self.emotion_patterns.get(current_emotion.primary_emotion, {})
        escalation_risk = pattern.get("escalation_risk", "low")
        
        # Determine intervention type
        if escalation_risk == "critical" or current_emotion.intensity > 0.8:
            intervention_type = InterventionType.ESCALATION
            priority = 5
        elif escalation_risk == "high" or current_emotion.intensity > 0.6:
            intervention_type = InterventionType.DE_ESCALATION
            priority = 4
        elif current_emotion.primary_emotion in [EmotionType.ANXIETY, EmotionType.FEAR]:
            intervention_type = InterventionType.CLARIFICATION
            priority = 3
        elif current_emotion.primary_emotion == EmotionType.EXCITEMENT:
            intervention_type = InterventionType.PROACTIVE_HELP
            priority = 2
        else:
            intervention_type = InterventionType.EMPATHY
            priority = 1
        
        # Get intervention strategy
        strategy = self.intervention_strategies[intervention_type]
        
        # Determine required agent skills
        required_skills = pattern.get("agent_skills", [])
        if intervention_type == InterventionType.ESCALATION:
            required_skills.extend(["supervisor", "crisis_management"])
        
        intervention = InterventionAction(
            intervention_type=intervention_type,
            description=f"Intervention for {current_emotion.primary_emotion.value} emotion",
            timestamp=datetime.now(),
            success_probability=strategy["success_rate"],
            agent_skills_required=required_skills,
            escalation_priority=priority
        )
        
        # Add to session
        session.interventions.append(intervention)
        
        return intervention
    
    def generate_emotional_response(self, session_id: str, 
                                  intervention: InterventionAction) -> Dict[str, Any]:
        """Generate emotionally appropriate response"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        current_emotion = session.current_emotion
        
        # Generate response based on intervention type
        if intervention.intervention_type == InterventionType.DE_ESCALATION:
            if current_emotion.primary_emotion == EmotionType.FRUSTRATION:
                response = {
                    "voice_response": "I completely understand your frustration, and I apologize for the inconvenience. Let me help you resolve this right away.",
                    "tone": "empathetic",
                    "pace": "slower",
                    "volume": "normal",
                    "ssml_marks": ["<emphasis level='moderate'>completely understand</emphasis>", "<break time='500ms'/>"]
                }
            else:
                response = {
                    "voice_response": "I can see this is important to you. Let me take care of this for you right now.",
                    "tone": "caring",
                    "pace": "normal",
                    "volume": "normal",
                    "ssml_marks": ["<emphasis level='moderate'>important</emphasis>"]
                }
        
        elif intervention.intervention_type == InterventionType.ESCALATION:
            response = {
                "voice_response": "I want to make sure you get the best possible help. Let me connect you with a specialist who can resolve this immediately.",
                "tone": "professional",
                "pace": "slightly_faster",
                "volume": "normal",
                "ssml_marks": ["<emphasis level='strong'>best possible help</emphasis>"]
            }
        
        elif intervention.intervention_type == InterventionType.CLARIFICATION:
            response = {
                "voice_response": "Let me break this down step by step so it's crystal clear. I'll guide you through each part.",
                "tone": "patient",
                "pace": "slower",
                "volume": "clear",
                "ssml_marks": ["<break time='300ms'/>", "<emphasis level='moderate'>crystal clear</emphasis>"]
            }
        
        elif intervention.intervention_type == InterventionType.EMPATHY:
            response = {
                "voice_response": "I hear you, and I want you to know that I'm here to help. Your concerns are important to me.",
                "tone": "warm",
                "pace": "normal",
                "volume": "normal",
                "ssml_marks": ["<emphasis level='moderate'>important to me</emphasis>"]
            }
        
        else:  # PROACTIVE_HELP
            response = {
                "voice_response": "That's great! While I'm helping you with this, let me also show you some additional features that might be useful.",
                "tone": "enthusiastic",
                "pace": "normal",
                "volume": "normal",
                "ssml_marks": ["<emphasis level='moderate'>great</emphasis>"]
            }
        
        # Add emotional context
        response.update({
            "emotional_context": {
                "primary_emotion": current_emotion.primary_emotion.value,
                "intensity": current_emotion.intensity,
                "stress_level": current_emotion.stress_level.value,
                "intervention_type": intervention.intervention_type.value,
                "escalation_priority": intervention.escalation_priority
            }
        })
        
        return response
    
    def predict_escalation_risk(self, session_id: str) -> Dict[str, Any]:
        """Predict escalation risk based on emotional patterns"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        # Analyze recent emotional states
        recent_states = session.emotional_states[-5:] if len(session.emotional_states) >= 5 else session.emotional_states
        
        # Calculate risk factors
        high_intensity_count = sum(1 for state in recent_states if state.intensity > 0.7)
        negative_emotion_count = sum(1 for state in recent_states 
                                   if state.primary_emotion in [EmotionType.FRUSTRATION, EmotionType.ANGER, EmotionType.ANXIETY])
        trigger_count = len(session.triggers)
        
        # Calculate risk score
        risk_score = (high_intensity_count * 0.3 + 
                     negative_emotion_count * 0.4 + 
                     trigger_count * 0.3) / len(recent_states) if recent_states else 0
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = "critical"
            time_to_escalation = "immediate"
        elif risk_score > 0.5:
            risk_level = "high"
            time_to_escalation = "within_2_minutes"
        elif risk_score > 0.3:
            risk_level = "medium"
            time_to_escalation = "within_5_minutes"
        else:
            risk_level = "low"
            time_to_escalation = "unlikely"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "time_to_escalation": time_to_escalation,
            "risk_factors": {
                "high_intensity_emotions": high_intensity_count,
                "negative_emotions": negative_emotion_count,
                "emotional_triggers": trigger_count
            },
            "recommended_actions": self.get_risk_mitigation_actions(risk_level)
        }
    
    def get_risk_mitigation_actions(self, risk_level: str) -> List[str]:
        """Get recommended actions for risk mitigation"""
        actions = {
            "critical": [
                "Immediate escalation to supervisor",
                "Offer compensation or goodwill gesture",
                "Provide direct phone number for follow-up"
            ],
            "high": [
                "Proactive de-escalation techniques",
                "Offer immediate resolution",
                "Prepare escalation path"
            ],
            "medium": [
                "Monitor emotional state closely",
                "Use empathy and clarification",
                "Provide regular updates"
            ],
            "low": [
                "Continue normal interaction",
                "Maintain positive engagement",
                "Monitor for changes"
            ]
        }
        
        return actions.get(risk_level, ["Continue monitoring"])
    
    def get_session_insights(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive emotional insights for the session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        duration = (datetime.now() - session.start_time).total_seconds()
        
        # Analyze emotional progression
        emotion_counts = {}
        for state in session.emotional_states:
            emotion = state.primary_emotion.value
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate average intensity
        avg_intensity = sum(state.intensity for state in session.emotional_states) / len(session.emotional_states) if session.emotional_states else 0
        
        # Get escalation prediction
        escalation_prediction = self.predict_escalation_risk(session_id)
        
        return {
            "session_id": session_id,
            "customer_id": session.customer_id,
            "duration_seconds": duration,
            "emotional_states_count": len(session.emotional_states),
            "triggers_count": len(session.triggers),
            "interventions_count": len(session.interventions),
            "escalation_events_count": len(session.escalation_events),
            "current_emotion": {
                "primary": session.current_emotion.primary_emotion.value,
                "intensity": session.current_emotion.intensity,
                "stress_level": session.current_emotion.stress_level.value
            },
            "emotion_distribution": emotion_counts,
            "average_intensity": avg_intensity,
            "escalation_prediction": escalation_prediction,
            "recent_triggers": [asdict(trigger) for trigger in session.triggers[-3:]],
            "recent_interventions": [asdict(intervention) for intervention in session.interventions[-3:]]
        }
    
    def end_emotion_session(self, session_id: str) -> Dict[str, Any]:
        """End emotion tracking session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        insights = self.get_session_insights(session_id)
        
        del self.active_sessions[session_id]
        
        return {
            "message": f"Emotion session {session_id} ended",
            "final_insights": insights
        }

def demo_emotion_aware_system():
    """Demonstrate emotion-aware system capabilities"""
    print("=" * 60)
    print("Chapter 9: Emotion-Aware System Demo")
    print("=" * 60)
    
    # Initialize the system
    system = EmotionAwareSystem()
    
    # Demo 1: Start emotion tracking
    print("\n1. Starting Emotion Tracking")
    print("-" * 30)
    
    session_id = system.start_emotion_session("CUST001")
    print(f"Started emotion tracking for customer CUST001")
    
    # Demo 2: Simulate emotional progression
    print("\n2. Emotional Progression Simulation")
    print("-" * 30)
    
    # Simulate various events and emotional responses
    events = [
        ("system_response", "Welcome to our service. How can I help you?"),
        ("customer_input", "I need help with my account"),
        ("system_response", "I'll help you with your account. Please provide your account number."),
        ("customer_input", "I already told you my account number"),
        ("system_response", "I apologize, but I need you to provide your account number again."),
        ("customer_input", "This is ridiculous! I've been waiting for 10 minutes!"),
        ("system_response", "I understand your frustration. Let me help you immediately.")
    ]
    
    for i, (event_type, event_description) in enumerate(events):
        print(f"\nEvent {i+1}: {event_type} - '{event_description}'")
        
        # Analyze emotion
        emotion = system.analyze_voice_emotion("audio_sample", session_id)
        print(f"  Detected Emotion: {emotion.primary_emotion.value} (Intensity: {emotion.intensity:.2f})")
        print(f"  Stress Level: {emotion.stress_level.value}")
        
        # Detect triggers
        triggers = system.detect_emotional_triggers(session_id, event_type, event_description)
        if triggers:
            print(f"  Emotional Triggers: {len(triggers)} detected")
        
        # Determine intervention
        intervention = system.determine_intervention(session_id)
        if intervention:
            print(f"  Intervention: {intervention.intervention_type.value} (Priority: {intervention.escalation_priority})")
            
            # Generate response
            response = system.generate_emotional_response(session_id, intervention)
            print(f"  Response: {response['voice_response']}")
            print(f"  Tone: {response['tone']}")
    
    # Demo 3: Escalation Risk Prediction
    print("\n3. Escalation Risk Prediction")
    print("-" * 30)
    
    escalation_prediction = system.predict_escalation_risk(session_id)
    print(f"Risk Score: {escalation_prediction['risk_score']:.2f}")
    print(f"Risk Level: {escalation_prediction['risk_level']}")
    print(f"Time to Escalation: {escalation_prediction['time_to_escalation']}")
    print(f"Risk Factors:")
    for factor, value in escalation_prediction['risk_factors'].items():
        print(f"  {factor}: {value}")
    print(f"Recommended Actions:")
    for action in escalation_prediction['recommended_actions']:
        print(f"  - {action}")
    
    # Demo 4: Session Insights
    print("\n4. Session Insights")
    print("-" * 30)
    
    insights = system.get_session_insights(session_id)
    print(f"Session Duration: {insights['duration_seconds']:.1f} seconds")
    print(f"Emotional States Tracked: {insights['emotional_states_count']}")
    print(f"Emotional Triggers: {insights['triggers_count']}")
    print(f"Interventions Applied: {insights['interventions_count']}")
    print(f"Current Emotion: {insights['current_emotion']['primary']} (Intensity: {insights['current_emotion']['intensity']:.2f})")
    print(f"Average Intensity: {insights['average_intensity']:.2f}")
    print(f"Emotion Distribution:")
    for emotion, count in insights['emotion_distribution'].items():
        print(f"  {emotion}: {count}")
    
    # Demo 5: End Session
    print("\n5. Ending Emotion Session")
    print("-" * 30)
    
    end_result = system.end_emotion_session(session_id)
    print(f"Session ended: {end_result['message']}")
    
    print("\n" + "=" * 60)
    print("Emotion-Aware System Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("  ✓ Real-time emotion detection")
    print("  ✓ Emotional trigger analysis")
    print("  ✓ Proactive intervention")
    print("  ✓ Escalation risk prediction")
    print("  ✓ Emotion-driven responses")
    print("  ✓ Session insights and analytics")
    print("  ✓ Agent skill matching")

if __name__ == "__main__":
    demo_emotion_aware_system()
