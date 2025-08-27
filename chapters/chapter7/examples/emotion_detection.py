#!/usr/bin/env python3
"""
Emotion Detection System - Chapter 7
Real-time emotion recognition from voice with adaptive responses.
"""

import os
import time
import json
import random
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EmotionType(Enum):
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

@dataclass
class AudioFeatures:
    """Audio features for emotion analysis"""
    pitch_mean: float
    pitch_std: float
    energy_mean: float
    energy_std: float
    mfcc_mean: float
    mfcc_std: float
    spectral_centroid: float
    spectral_rolloff: float
    zero_crossing_rate: float
    tempo: float

@dataclass
class EmotionResult:
    """Emotion detection result"""
    primary_emotion: str
    confidence: float
    all_emotions: Dict[str, float]
    audio_features: AudioFeatures
    timestamp: datetime

class EmotionDetector:
    """Advanced emotion detection from voice"""
    
    def __init__(self):
        self.emotion_thresholds = {
            'happiness': {'pitch_min': 180, 'energy_min': 0.08, 'tempo_min': 100},
            'sadness': {'pitch_max': 160, 'energy_max': 0.06, 'tempo_max': 90},
            'anger': {'energy_min': 0.12, 'pitch_std_min': 40, 'tempo_min': 110},
            'fear': {'pitch_min': 200, 'energy_max': 0.08, 'pitch_std_min': 30},
            'surprise': {'pitch_std_min': 60, 'energy_std_min': 0.05},
            'disgust': {'pitch_max': 170, 'energy_max': 0.07, 'tempo_max': 85}
        }
    
    def extract_audio_features(self, audio_data: np.ndarray, sample_rate: int) -> AudioFeatures:
        """Extract features for emotion analysis (simulated)"""
        
        # Simulate audio feature extraction
        # In a real implementation, you would use librosa or similar libraries
        
        # Simulate pitch features
        pitch_mean = random.uniform(120, 250)
        pitch_std = random.uniform(20, 80)
        
        # Simulate energy features
        energy_mean = random.uniform(0.03, 0.18)
        energy_std = random.uniform(0.01, 0.08)
        
        # Simulate MFCC features
        mfcc_mean = random.uniform(-5, 5)
        mfcc_std = random.uniform(1, 8)
        
        # Simulate spectral features
        spectral_centroid = random.uniform(1000, 4000)
        spectral_rolloff = random.uniform(2000, 6000)
        
        # Simulate other features
        zero_crossing_rate = random.uniform(0.01, 0.1)
        tempo = random.uniform(60, 140)
        
        return AudioFeatures(
            pitch_mean=pitch_mean,
            pitch_std=pitch_std,
            energy_mean=energy_mean,
            energy_std=energy_std,
            mfcc_mean=mfcc_mean,
            mfcc_std=mfcc_std,
            spectral_centroid=spectral_centroid,
            spectral_rolloff=spectral_rolloff,
            zero_crossing_rate=zero_crossing_rate,
            tempo=tempo
        )
    
    def detect_emotion(self, audio_features: AudioFeatures) -> EmotionResult:
        """Detect emotions from audio features"""
        
        emotions = {
            'happiness': 0.0,
            'sadness': 0.0,
            'anger': 0.0,
            'fear': 0.0,
            'surprise': 0.0,
            'disgust': 0.0,
            'neutral': 0.0
        }
        
        # Apply emotion detection rules
        emotions['happiness'] = self._calculate_happiness_score(audio_features)
        emotions['sadness'] = self._calculate_sadness_score(audio_features)
        emotions['anger'] = self._calculate_anger_score(audio_features)
        emotions['fear'] = self._calculate_fear_score(audio_features)
        emotions['surprise'] = self._calculate_surprise_score(audio_features)
        emotions['disgust'] = self._calculate_disgust_score(audio_features)
        
        # Calculate neutral score (inverse of other emotions)
        max_other_emotion = max(emotions.values())
        emotions['neutral'] = max(0.0, 1.0 - max_other_emotion)
        
        # Find primary emotion
        primary_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return EmotionResult(
            primary_emotion=primary_emotion[0],
            confidence=primary_emotion[1],
            all_emotions=emotions,
            audio_features=audio_features,
            timestamp=datetime.now()
        )
    
    def _calculate_happiness_score(self, features: AudioFeatures) -> float:
        """Calculate happiness score"""
        score = 0.0
        
        # High pitch, high energy, fast tempo
        if features.pitch_mean > self.emotion_thresholds['happiness']['pitch_min']:
            score += 0.3
        if features.energy_mean > self.emotion_thresholds['happiness']['energy_min']:
            score += 0.3
        if features.tempo > self.emotion_thresholds['happiness']['tempo_min']:
            score += 0.2
        
        # Additional factors
        if features.pitch_std > 30:  # Variable pitch
            score += 0.1
        if features.spectral_centroid > 2500:  # Bright timbre
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_sadness_score(self, features: AudioFeatures) -> float:
        """Calculate sadness score"""
        score = 0.0
        
        # Low pitch, low energy, slow tempo
        if features.pitch_mean < self.emotion_thresholds['sadness']['pitch_max']:
            score += 0.3
        if features.energy_mean < self.emotion_thresholds['sadness']['energy_max']:
            score += 0.3
        if features.tempo < self.emotion_thresholds['sadness']['tempo_max']:
            score += 0.2
        
        # Additional factors
        if features.pitch_std < 25:  # Monotone
            score += 0.1
        if features.spectral_centroid < 2000:  # Dull timbre
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_anger_score(self, features: AudioFeatures) -> float:
        """Calculate anger score"""
        score = 0.0
        
        # High energy, variable pitch, fast tempo
        if features.energy_mean > self.emotion_thresholds['anger']['energy_min']:
            score += 0.4
        if features.pitch_std > self.emotion_thresholds['anger']['pitch_std_min']:
            score += 0.3
        if features.tempo > self.emotion_thresholds['anger']['tempo_min']:
            score += 0.2
        
        # Additional factors
        if features.zero_crossing_rate > 0.05:  # Harsh quality
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_fear_score(self, features: AudioFeatures) -> float:
        """Calculate fear score"""
        score = 0.0
        
        # High pitch, low energy, variable pitch
        if features.pitch_mean > self.emotion_thresholds['fear']['pitch_min']:
            score += 0.3
        if features.energy_mean < self.emotion_thresholds['fear']['energy_max']:
            score += 0.3
        if features.pitch_std > self.emotion_thresholds['fear']['pitch_std_min']:
            score += 0.2
        
        # Additional factors
        if features.spectral_rolloff > 4000:  # High frequency content
            score += 0.1
        if features.tempo > 120:  # Fast speech
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_surprise_score(self, features: AudioFeatures) -> float:
        """Calculate surprise score"""
        score = 0.0
        
        # High pitch variability, high energy variability
        if features.pitch_std > self.emotion_thresholds['surprise']['pitch_std_min']:
            score += 0.4
        if features.energy_std > self.emotion_thresholds['surprise']['energy_std_min']:
            score += 0.3
        
        # Additional factors
        if features.spectral_centroid > 3000:  # Bright timbre
            score += 0.2
        if features.tempo > 130:  # Very fast speech
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_disgust_score(self, features: AudioFeatures) -> float:
        """Calculate disgust score"""
        score = 0.0
        
        # Low pitch, low energy, slow tempo
        if features.pitch_mean < self.emotion_thresholds['disgust']['pitch_max']:
            score += 0.3
        if features.energy_mean < self.emotion_thresholds['disgust']['energy_max']:
            score += 0.3
        if features.tempo < self.emotion_thresholds['disgust']['tempo_max']:
            score += 0.2
        
        # Additional factors
        if features.spectral_centroid < 1800:  # Nasal quality
            score += 0.1
        if features.mfcc_std < 3:  # Monotone quality
            score += 0.1
        
        return min(1.0, score)

class EmotionAwareIVR:
    """IVR system with emotion detection and adaptive responses"""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.response_templates = {
            'happiness': {
                'greeting': "I'm glad you're having a great day! How can I help you?",
                'confirmation': "Excellent! I'll get that sorted for you right away.",
                'closing': "It's been a pleasure helping you today. Have a wonderful day!",
                'escalation': "I'm happy to connect you with someone who can help even more!"
            },
            'sadness': {
                'greeting': "I understand this might be a difficult time. I'm here to help.",
                'confirmation': "I'll make sure to handle this carefully for you.",
                'closing': "I hope I've been able to help. Please don't hesitate to call back.",
                'escalation': "Let me connect you with someone who can provide more personalized assistance."
            },
            'anger': {
                'greeting': "I can see you're frustrated, and I want to help resolve this quickly.",
                'confirmation': "I understand this is important to you. Let me escalate this immediately.",
                'closing': "I appreciate your patience. We're working to resolve this for you.",
                'escalation': "I'm connecting you with a specialist who can address this right away."
            },
            'fear': {
                'greeting': "I'm here to help you. Let's take this step by step.",
                'confirmation': "I'll make sure everything is handled properly and safely.",
                'closing': "You're in good hands. We'll take care of this for you.",
                'escalation': "Let me connect you with someone who can provide immediate assistance."
            },
            'surprise': {
                'greeting': "I understand this might be unexpected. Let me help clarify things.",
                'confirmation': "I'll make sure to explain everything clearly.",
                'closing': "I hope I've been able to clarify everything for you.",
                'escalation': "Let me connect you with someone who can provide more detailed information."
            },
            'disgust': {
                'greeting': "I understand your concern. Let me help address this properly.",
                'confirmation': "I'll make sure this is handled appropriately.",
                'closing': "I appreciate you bringing this to our attention.",
                'escalation': "Let me connect you with someone who can address this concern directly."
            },
            'neutral': {
                'greeting': "How can I help you today?",
                'confirmation': "I'll help you with that.",
                'closing': "Thank you for calling. Have a good day.",
                'escalation': "Let me connect you with someone who can assist you further."
            }
        }
        
        # Escalation thresholds
        self.escalation_thresholds = {
            'anger': 0.7,
            'fear': 0.6,
            'sadness': 0.8,
            'disgust': 0.7
        }
    
    def process_customer_input(self, audio_data: np.ndarray, sample_rate: int, 
                             text_content: str, interaction_type: str = 'greeting') -> Dict[str, Any]:
        """Process customer input with emotion detection"""
        
        # Extract audio features and detect emotions
        audio_features = self.emotion_detector.extract_audio_features(audio_data, sample_rate)
        emotion_result = self.emotion_detector.detect_emotion(audio_features)
        
        # Generate appropriate response
        response = self._generate_emotion_aware_response(
            emotion_result.primary_emotion, 
            interaction_type,
            text_content
        )
        
        # Determine if escalation is needed
        escalation_needed = self._check_escalation_needed(emotion_result)
        
        # Generate escalation reason if needed
        escalation_reason = None
        if escalation_needed:
            escalation_reason = self._generate_escalation_reason(emotion_result)
        
        return {
            'text_response': response,
            'detected_emotion': emotion_result.primary_emotion,
            'emotion_confidence': emotion_result.confidence,
            'all_emotions': emotion_result.all_emotions,
            'escalation_needed': escalation_needed,
            'escalation_reason': escalation_reason,
            'audio_features': {
                'pitch_mean': audio_features.pitch_mean,
                'energy_mean': audio_features.energy_mean,
                'tempo': audio_features.tempo,
                'pitch_std': audio_features.pitch_std
            },
            'timestamp': emotion_result.timestamp.isoformat()
        }
    
    def _generate_emotion_aware_response(self, emotion: str, interaction_type: str, 
                                       user_input: str) -> str:
        """Generate emotion-aware response"""
        
        templates = self.response_templates.get(emotion, self.response_templates['neutral'])
        
        # Select response based on interaction type
        if interaction_type == 'greeting':
            base_response = templates['greeting']
        elif interaction_type == 'confirmation':
            base_response = templates['confirmation']
        elif interaction_type == 'closing':
            base_response = templates['closing']
        elif interaction_type == 'escalation':
            base_response = templates['escalation']
        else:
            base_response = templates['greeting']
        
        # Add personalization based on user input
        if 'name' in user_input.lower():
            # Extract name if mentioned
            name_start = user_input.lower().find('my name is') + 10
            if name_start > 9:
                name_end = user_input.find(' ', name_start)
                if name_end == -1:
                    name_end = len(user_input)
                name = user_input[name_start:name_end].strip()
                base_response = base_response.replace("you", f"{name}")
        
        return base_response
    
    def _check_escalation_needed(self, emotion_result: EmotionResult) -> bool:
        """Check if escalation to human agent is needed"""
        
        emotion = emotion_result.primary_emotion
        confidence = emotion_result.confidence
        
        # Check if emotion exceeds escalation threshold
        if emotion in self.escalation_thresholds:
            if confidence >= self.escalation_thresholds[emotion]:
                return True
        
        # Additional escalation conditions
        if emotion == 'anger' and confidence > 0.6:
            return True
        elif emotion == 'fear' and confidence > 0.5:
            return True
        
        return False
    
    def _generate_escalation_reason(self, emotion_result: EmotionResult) -> str:
        """Generate reason for escalation"""
        
        emotion = emotion_result.primary_emotion
        confidence = emotion_result.confidence
        
        reasons = {
            'anger': f"Customer appears frustrated (confidence: {confidence:.1%})",
            'fear': f"Customer seems concerned or anxious (confidence: {confidence:.1%})",
            'sadness': f"Customer appears distressed (confidence: {confidence:.1%})",
            'disgust': f"Customer expresses strong dissatisfaction (confidence: {confidence:.1%})"
        }
        
        return reasons.get(emotion, f"Emotional state detected: {emotion} (confidence: {confidence:.1%})")

def simulate_emotion_detection():
    """Simulate emotion detection system"""
    print("Emotion Detection System - Chapter 7")
    print("="*80)
    print("Demonstrating real-time emotion recognition from voice...")
    
    # Create emotion detection system
    emotion_ivr = EmotionAwareIVR()
    
    # Simulate different emotional scenarios
    scenarios = [
        {
            'name': 'Happy Customer',
            'description': 'Customer calling with positive energy',
            'expected_emotion': 'happiness',
            'interaction_type': 'greeting',
            'user_input': 'Hi, I want to check my account balance'
        },
        {
            'name': 'Frustrated Customer',
            'description': 'Customer with billing issues',
            'expected_emotion': 'anger',
            'interaction_type': 'confirmation',
            'user_input': 'I\'m really upset about this charge on my bill'
        },
        {
            'name': 'Concerned Customer',
            'description': 'Customer worried about account security',
            'expected_emotion': 'fear',
            'interaction_type': 'greeting',
            'user_input': 'I think someone might have accessed my account'
        },
        {
            'name': 'Sad Customer',
            'description': 'Customer dealing with loss',
            'expected_emotion': 'sadness',
            'interaction_type': 'closing',
            'user_input': 'My name is John and I need to close my account'
        },
        {
            'name': 'Neutral Customer',
            'description': 'Standard customer inquiry',
            'expected_emotion': 'neutral',
            'interaction_type': 'greeting',
            'user_input': 'What are your business hours?'
        }
    ]
    
    print(f"\nSimulating {len(scenarios)} emotional scenarios...")
    print("-" * 80)
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Expected Emotion: {scenario['expected_emotion']}")
        print(f"User Input: '{scenario['user_input']}'")
        
        # Simulate audio data (random numpy array)
        audio_data = np.random.randn(16000)  # 1 second at 16kHz
        sample_rate = 16000
        
        # Process with emotion detection
        result = emotion_ivr.process_customer_input(
            audio_data, 
            sample_rate, 
            scenario['user_input'],
            scenario['interaction_type']
        )
        
        # Display results
        print(f"\nResults:")
        print(f"  Detected Emotion: {result['detected_emotion']}")
        print(f"  Confidence: {result['emotion_confidence']:.1%}")
        print(f"  Response: {result['text_response']}")
        print(f"  Escalation Needed: {'Yes' if result['escalation_needed'] else 'No'}")
        
        if result['escalation_needed']:
            print(f"  Escalation Reason: {result['escalation_reason']}")
        
        # Show all emotion scores
        print(f"  All Emotions:")
        for emotion, score in result['all_emotions'].items():
            print(f"    {emotion}: {score:.1%}")
        
        # Show audio features
        print(f"  Audio Features:")
        features = result['audio_features']
        print(f"    Pitch Mean: {features['pitch_mean']:.1f} Hz")
        print(f"    Energy Mean: {features['energy_mean']:.3f}")
        print(f"    Tempo: {features['tempo']:.1f} BPM")
        print(f"    Pitch Std: {features['pitch_std']:.1f}")
        
        results.append({
            'scenario': scenario['name'],
            'expected': scenario['expected_emotion'],
            'detected': result['detected_emotion'],
            'confidence': result['emotion_confidence'],
            'escalation': result['escalation_needed']
        })
        
        print("-" * 40)
    
    # Summary
    print(f"\n{'='*80}")
    print("EMOTION DETECTION SUMMARY")
    print(f"{'='*80}")
    
    correct_detections = sum(1 for r in results if r['expected'] == r['detected'])
    total_scenarios = len(results)
    
    print(f"Total Scenarios: {total_scenarios}")
    print(f"Correct Detections: {correct_detections}")
    print(f"Accuracy: {(correct_detections/total_scenarios)*100:.1f}%")
    
    print(f"\nDetailed Results:")
    for result in results:
        status = "CORRECT" if result['expected'] == result['detected'] else "INCORRECT"
        escalation = "ESCALATED" if result['escalation'] else "HANDLED"
        print(f"  {status} - {result['scenario']}: {result['expected']} → {result['detected']} ({result['confidence']:.1%}) [{escalation}]")
    
    print(f"\nKey Features Demonstrated:")
    print(f"  • Real-time emotion detection from voice")
    print(f"  • Audio feature extraction and analysis")
    print(f"  • Emotion-aware response generation")
    print(f"  • Automatic escalation based on emotional state")
    print(f"  • Multi-emotion classification with confidence scores")
    print(f"  • Adaptive IVR responses based on customer emotions")
    
    print(f"\nEmotion detection demo completed!")
    print("   This demonstrates how voice AI can detect and respond to customer emotions.")

if __name__ == "__main__":
    simulate_emotion_detection()
