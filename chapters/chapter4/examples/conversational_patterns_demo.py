#!/usr/bin/env python3
"""
Conversational Design Patterns Demo - Chapter 4
Demonstrates good vs bad conversational design patterns for voice AI.
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

class PatternType(Enum):
    """Types of conversational patterns"""
    GREETING = "greeting"
    INTENT_CAPTURE = "intent_capture"
    ERROR_RECOVERY = "error_recovery"
    CONTEXT_RETENTION = "context_retention"
    CONFIRMATION = "confirmation"
    ESCALATION = "escalation"
    CLOSING = "closing"

@dataclass
class ConversationPattern:
    """Represents a conversational pattern"""
    pattern_type: PatternType
    name: str
    bad_example: str
    good_example: str
    explanation: str
    best_practices: List[str]

@dataclass
class ConversationFlow:
    """Represents a complete conversation flow"""
    name: str
    turns: List[Dict]
    context: Dict
    metrics: Dict

class ConversationalPatternsDemo:
    """Demonstrates conversational design patterns"""
    
    def __init__(self):
        # Define conversation patterns
        self.patterns = [
            ConversationPattern(
                pattern_type=PatternType.GREETING,
                name="Greeting and Welcome",
                bad_example="Welcome to ACME Corporation. For billing press 1, for technical support press 2, for sales press 3, for account management press 4, for password reset press 5, for order tracking press 6...",
                good_example="Welcome to ACME. How can I help you today?",
                explanation="Keep greetings short and open-ended. Let the customer tell you what they need.",
                best_practices=[
                    "Keep it under 10 seconds",
                    "Use open-ended questions",
                    "Avoid overwhelming menus",
                    "Sound natural and friendly"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.INTENT_CAPTURE,
                name="Intent Recognition",
                bad_example="Customer: 'I need help with my invoice'\nAI: 'I'm sorry, I didn't understand. Please say billing, support, or sales.'",
                good_example="Customer: 'I need help with my invoice'\nAI: 'Got it. You need billing support. I'll connect you now.'",
                explanation="Recognize natural language and respond appropriately. Don't force rigid menu options.",
                best_practices=[
                    "Use natural language understanding",
                    "Confirm understanding",
                    "Provide immediate value",
                    "Don't force menu choices"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.ERROR_RECOVERY,
                name="Error Recovery",
                bad_example="'Invalid option. Please try again. Invalid option. Goodbye.'",
                good_example="'I didn't quite get that. You can say things like 'track my order', 'technical support', or 'billing questions'.",
                explanation="When errors occur, provide helpful guidance and examples. Never give up on the customer.",
                best_practices=[
                    "Acknowledge the error",
                    "Provide helpful examples",
                    "Give multiple retry opportunities",
                    "Offer escalation as last resort"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.CONTEXT_RETENTION,
                name="Context Retention",
                bad_example="Customer: 'I want to check my order'\nAI: 'Okay. Please give me your order number.'\nCustomer: 'It's 44321'\nAI: 'What do you want to do with your order?'",
                good_example="Customer: 'I want to check my order'\nAI: 'Sure. What's the order number?'\nCustomer: '44321'\nAI: 'Order 44321 was shipped yesterday and will arrive tomorrow.'",
                explanation="Remember what the customer said and use that context. Don't ask them to repeat information.",
                best_practices=[
                    "Maintain conversation context",
                    "Don't ask for repeated information",
                    "Use context to provide better service",
                    "Reference previous parts of conversation"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.CONFIRMATION,
                name="Critical Information Confirmation",
                bad_example="Customer: 'My order number is 12345'\nAI: 'Processing order 12345...'",
                good_example="Customer: 'My order number is 12345'\nAI: 'Did you say order number 1-2-3-4-5?'\nCustomer: 'Yes'\nAI: 'Thank you. Processing order 12345...'",
                explanation="Always confirm critical information like account numbers, amounts, or personal details.",
                best_practices=[
                    "Confirm account numbers",
                    "Confirm dollar amounts",
                    "Confirm personal information",
                    "Use clear, distinct pronunciation"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.ESCALATION,
                name="Graceful Escalation",
                bad_example="'I'm sorry, I can't help you. Goodbye.'",
                good_example="'I understand this is important. Let me connect you with a specialist who can better assist you.'",
                explanation="Make escalation feel natural and helpful, not like a failure. Transfer context to human agents.",
                best_practices=[
                    "Acknowledge the customer's need",
                    "Explain why escalation is helpful",
                    "Transfer context to human agent",
                    "Make it feel like a positive step"
                ]
            ),
            ConversationPattern(
                pattern_type=PatternType.CLOSING,
                name="Natural Closing",
                bad_example="'Thank you for calling. Goodbye.'",
                good_example="'Is there anything else I can help you with today?'\nCustomer: 'No, that's all'\nAI: 'Great! Thank you for calling ACME. Have a wonderful day.'",
                explanation="End conversations naturally and politely. Always offer additional help before closing.",
                best_practices=[
                    "Offer additional assistance",
                    "Thank the customer",
                    "End on a positive note",
                    "Use natural, friendly language"
                ]
            )
        ]
        
        # Define complete conversation flows
        self.conversation_flows = [
            {
                "name": "Balance Check - Good Design",
                "turns": [
                    {"speaker": "AI", "text": "Welcome to ACME Bank. How can I help you today?"},
                    {"speaker": "Customer", "text": "I want to check my account balance"},
                    {"speaker": "AI", "text": "I can help you check your balance. For security, I'll need to verify your identity. What's the last 4 digits of your social security number?"},
                    {"speaker": "Customer", "text": "1234"},
                    {"speaker": "AI", "text": "Did you say 1-2-3-4?"},
                    {"speaker": "Customer", "text": "Yes"},
                    {"speaker": "AI", "text": "Thank you. Your account balance is $2,456.78. Is there anything else I can help you with today?"},
                    {"speaker": "Customer", "text": "No, that's all"},
                    {"speaker": "AI", "text": "Great! Thank you for calling ACME Bank. Have a wonderful day."}
                ]
            },
            {
                "name": "Balance Check - Bad Design",
                "turns": [
                    {"speaker": "AI", "text": "Welcome to ACME Bank. For balance inquiry press 1, for transfers press 2, for bill payments press 3, for account management press 4, for technical support press 5..."},
                    {"speaker": "Customer", "text": "I want to check my balance"},
                    {"speaker": "AI", "text": "I'm sorry, I didn't understand. Please say 'balance', 'transfer', 'payment', or 'support'."},
                    {"speaker": "Customer", "text": "Balance"},
                    {"speaker": "AI", "text": "Please provide your account number."},
                    {"speaker": "Customer", "text": "123456789"},
                    {"speaker": "AI", "text": "What would you like to do with your account?"},
                    {"speaker": "Customer", "text": "Check balance"},
                    {"speaker": "AI", "text": "Your balance is $2,456.78. Goodbye."}
                ]
            }
        ]

    def analyze_pattern_quality(self, pattern: ConversationPattern) -> Dict:
        """Analyze the quality of a conversational pattern"""
        analysis = {
            "pattern_type": pattern.pattern_type.value,
            "name": pattern.name,
            "bad_example_score": self.score_example(pattern.bad_example),
            "good_example_score": self.score_example(pattern.good_example),
            "improvement": 0,
            "issues": [],
            "strengths": []
        }
        
        # Calculate improvement
        analysis["improvement"] = analysis["good_example_score"] - analysis["bad_example_score"]
        
        # Identify issues in bad example
        bad_issues = self.identify_issues(pattern.bad_example)
        analysis["issues"] = bad_issues
        
        # Identify strengths in good example
        good_strengths = self.identify_strengths(pattern.good_example)
        analysis["strengths"] = good_strengths
        
        return analysis

    def score_example(self, text: str) -> float:
        """Score a conversational example (0-100)"""
        score = 100.0
        
        # Penalize for length (too long is bad)
        if len(text) > 200:
            score -= 20
        elif len(text) > 100:
            score -= 10
        
        # Penalize for formal language
        formal_words = ["greetings", "esteemed", "may I", "please be advised", "kindly"]
        for word in formal_words:
            if word.lower() in text.lower():
                score -= 15
        
        # Penalize for overwhelming options
        if text.count(",") > 5:
            score -= 20
        
        # Penalize for robotic language
        robotic_phrases = ["invalid option", "please try again", "goodbye"]
        for phrase in robotic_phrases:
            if phrase.lower() in text.lower():
                score -= 25
        
        # Reward for natural language
        natural_phrases = ["how can I help", "got it", "sure", "great", "thank you"]
        for phrase in natural_phrases:
            if phrase.lower() in text.lower():
                score += 10
        
        # Reward for empathy
        empathetic_phrases = ["I understand", "I can help", "let me", "sure"]
        for phrase in empathetic_phrases:
            if phrase.lower() in text.lower():
                score += 5
        
        return max(0, min(100, score))

    def identify_issues(self, text: str) -> List[str]:
        """Identify issues in a conversational example"""
        issues = []
        
        if len(text) > 200:
            issues.append("Too long and overwhelming")
        
        if any(word in text.lower() for word in ["greetings", "esteemed", "may I"]):
            issues.append("Too formal and robotic")
        
        if text.count(",") > 5:
            issues.append("Too many options at once")
        
        if "invalid option" in text.lower():
            issues.append("Poor error handling")
        
        if "goodbye" in text.lower() and len(text) < 50:
            issues.append("Abrupt ending")
        
        if not any(word in text.lower() for word in ["how", "what", "can I help"]):
            issues.append("Not conversational")
        
        return issues

    def identify_strengths(self, text: str) -> List[str]:
        """Identify strengths in a conversational example"""
        strengths = []
        
        if len(text) < 100:
            strengths.append("Concise and clear")
        
        if any(word in text.lower() for word in ["how can I help", "got it", "sure"]):
            strengths.append("Natural and conversational")
        
        if any(word in text.lower() for word in ["I understand", "I can help"]):
            strengths.append("Shows empathy")
        
        if "thank you" in text.lower():
            strengths.append("Polite and courteous")
        
        if "anything else" in text.lower():
            strengths.append("Offers additional help")
        
        if text.endswith(".") and not text.endswith("..."):
            strengths.append("Complete thoughts")
        
        return strengths

    def analyze_conversation_flow(self, flow: Dict) -> ConversationFlow:
        """Analyze a complete conversation flow"""
        turns = flow["turns"]
        context = {}
        metrics = {
            "total_turns": len(turns),
            "ai_turns": len([t for t in turns if t["speaker"] == "AI"]),
            "customer_turns": len([t for t in turns if t["speaker"] == "Customer"]),
            "avg_turn_length": sum(len(t["text"]) for t in turns) / len(turns),
            "context_retention_score": 0,
            "naturalness_score": 0,
            "efficiency_score": 0
        }
        
        # Analyze context retention
        context_retention = 0
        for i, turn in enumerate(turns):
            if turn["speaker"] == "AI" and i > 0:
                # Check if AI maintains context from previous turns
                prev_customer_text = turns[i-1]["text"] if turns[i-1]["speaker"] == "Customer" else ""
                if any(word in turn["text"].lower() for word in prev_customer_text.lower().split()):
                    context_retention += 1
        
        metrics["context_retention_score"] = (context_retention / max(1, len([t for t in turns if t["speaker"] == "AI"]))) * 100
        
        # Analyze naturalness
        natural_phrases = ["how can I help", "got it", "sure", "great", "thank you", "I can help"]
        natural_count = sum(1 for turn in turns if turn["speaker"] == "AI" and 
                          any(phrase in turn["text"].lower() for phrase in natural_phrases))
        metrics["naturalness_score"] = (natural_count / max(1, len([t for t in turns if t["speaker"] == "AI"]))) * 100
        
        # Analyze efficiency
        metrics["efficiency_score"] = 100 - (metrics["total_turns"] * 10)  # Fewer turns = more efficient
        
        return ConversationFlow(
            name=flow["name"],
            turns=turns,
            context=context,
            metrics=metrics
        )

    def print_pattern_analysis(self, pattern: ConversationPattern):
        """Print detailed analysis of a conversation pattern"""
        analysis = self.analyze_pattern_quality(pattern)
        
        print(f"\n{'='*80}")
        print(f"PATTERN ANALYSIS: {pattern.name}")
        print(f"{'='*80}")
        
        print(f"\nPattern Type: {pattern.pattern_type.value}")
        print(f"Explanation: {pattern.explanation}")
        
        print(f"\nBad Example:")
        print(f"   '{pattern.bad_example}'")
        print(f"   Score: {analysis['bad_example_score']:.1f}/100")
        print(f"   Issues: {', '.join(analysis['issues'])}")
        
        print(f"\nGood Example:")
        print(f"   '{pattern.good_example}'")
        print(f"   Score: {analysis['good_example_score']:.1f}/100")
        print(f"   Strengths: {', '.join(analysis['strengths'])}")
        
        print(f"\nImprovement: +{analysis['improvement']:.1f} points")
        
        print(f"\nBest Practices:")
        for i, practice in enumerate(pattern.best_practices, 1):
            print(f"   {i}. {practice}")

    def print_conversation_flow_analysis(self, flow: ConversationFlow):
        """Print analysis of a complete conversation flow"""
        print(f"\n{'='*80}")
        print(f"CONVERSATION FLOW: {flow.name}")
        print(f"{'='*80}")
        
        print(f"\nConversation:")
        for i, turn in enumerate(flow.turns, 1):
            speaker = turn["speaker"]
            text = turn["text"]
            print(f"   {i}. {speaker}: '{text}'")
        
        print(f"\nMetrics:")
        print(f"   Total Turns: {flow.metrics['total_turns']}")
        print(f"   AI Turns: {flow.metrics['ai_turns']}")
        print(f"   Customer Turns: {flow.metrics['customer_turns']}")
        print(f"   Average Turn Length: {flow.metrics['avg_turn_length']:.1f} characters")
        print(f"   Context Retention Score: {flow.metrics['context_retention_score']:.1f}%")
        print(f"   Naturalness Score: {flow.metrics['naturalness_score']:.1f}%")
        print(f"   Efficiency Score: {flow.metrics['efficiency_score']:.1f}%")
        
        # Overall assessment
        overall_score = (flow.metrics['context_retention_score'] + 
                        flow.metrics['naturalness_score'] + 
                        flow.metrics['efficiency_score']) / 3
        
        print(f"\nOverall Assessment:")
        if overall_score >= 80:
            print(f"   Excellent Design (Score: {overall_score:.1f}%)")
        elif overall_score >= 60:
            print(f"   Good Design (Score: {overall_score:.1f}%)")
        elif overall_score >= 40:
            print(f"   Fair Design (Score: {overall_score:.1f}%)")
        else:
            print(f"   Poor Design (Score: {overall_score:.1f}%)")

    def run_demo(self):
        """Run the conversational patterns demo"""
        print("Conversational Design Patterns Demo - Chapter 4")
        print("="*80)
        print("Analyzing good vs bad conversational design patterns...")
        
        # Analyze individual patterns
        print(f"\nAnalyzing {len(self.patterns)} conversation patterns...")
        for pattern in self.patterns:
            self.print_pattern_analysis(pattern)
        
        # Analyze complete conversation flows
        print(f"\nAnalyzing complete conversation flows...")
        for flow_data in self.conversation_flows:
            flow = self.analyze_conversation_flow(flow_data)
            self.print_conversation_flow_analysis(flow)
        
        # Summary and recommendations
        print(f"\n{'='*80}")
        print("SUMMARY AND RECOMMENDATIONS")
        print(f"{'='*80}")
        
        print(f"\nKey Insights:")
        print(f"   • Good conversational design focuses on clarity and naturalness")
        print(f"   • Bad design often overwhelms users with too many options")
        print(f"   • Context retention is crucial for good user experience")
        print(f"   • Error handling should be helpful, not frustrating")
        
        print(f"\nDesign Principles:")
        print(f"   1. Keep it simple and conversational")
        print(f"   2. Maintain context throughout the conversation")
        print(f"   3. Provide helpful error recovery")
        print(f"   4. Always offer escalation as an option")
        print(f"   5. End conversations naturally and politely")
        
        print(f"\nConversational design demo completed!")
        print("   Remember: Good design is more important than advanced technology.")

if __name__ == "__main__":
    demo = ConversationalPatternsDemo()
    demo.run_demo()
