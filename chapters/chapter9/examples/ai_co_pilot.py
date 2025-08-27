#!/usr/bin/env python3
"""
Chapter 9 - The Future of Voice AI in Contact Centers
AI Co-Pilot Demo

This script demonstrates intelligent agent assistance including:
- Real-time agent support
- Knowledge augmentation
- Quality assurance
- Training and development
- AI-powered summarization
"""

import json
import time
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum

class AssistanceType(Enum):
    KNOWLEDGE_AUGMENTATION = "knowledge_augmentation"
    REAL_TIME_SUPPORT = "real_time_support"
    QUALITY_ASSURANCE = "quality_assurance"
    TRAINING_GUIDANCE = "training_guidance"
    SUMMARIZATION = "summarization"

class AgentSkill(Enum):
    TECHNICAL_EXPERTISE = "technical_expertise"
    CUSTOMER_SERVICE = "customer_service"
    BILLING_SPECIALIST = "billing_specialist"
    DE_ESCALATION = "de_escalation"
    PRODUCT_KNOWLEDGE = "product_knowledge"

class InteractionQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"

@dataclass
class AgentProfile:
    """Agent profile and capabilities"""
    agent_id: str
    name: str
    skills: List[AgentSkill]
    experience_level: str  # junior, intermediate, senior
    performance_score: float
    current_session: Optional[str] = None
    assistance_history: List[Dict[str, Any]] = None

@dataclass
class CustomerInteraction:
    """Customer interaction data"""
    interaction_id: str
    customer_id: str
    agent_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    conversation_transcript: List[Dict[str, Any]]
    customer_sentiment: str
    resolution_status: str
    quality_score: float
    assistance_requests: List[Dict[str, Any]]

@dataclass
class CoPilotSuggestion:
    """AI co-pilot suggestion"""
    suggestion_id: str
    assistance_type: AssistanceType
    content: str
    confidence: float
    context: Dict[str, Any]
    timestamp: datetime
    accepted: bool = False
    implemented: bool = False

@dataclass
class KnowledgeArticle:
    """Knowledge base article"""
    article_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    relevance_score: float
    last_updated: datetime

class AICoPilot:
    """Intelligent AI co-pilot for contact center agents"""
    
    def __init__(self):
        self.agents: Dict[str, AgentProfile] = {}
        self.active_interactions: Dict[str, CustomerInteraction] = {}
        self.knowledge_base: Dict[str, KnowledgeArticle] = {}
        self.suggestions_history: List[CoPilotSuggestion] = []
        self.quality_metrics: Dict[str, List[float]] = {}
        self.load_data()
    
    def load_data(self):
        """Load sample data for the co-pilot system"""
        # Sample agents
        self.agents = {
            "AGENT001": AgentProfile(
                agent_id="AGENT001",
                name="Sarah Johnson",
                skills=[AgentSkill.CUSTOMER_SERVICE, AgentSkill.DE_ESCALATION],
                experience_level="intermediate",
                performance_score=4.2,
                assistance_history=[]
            ),
            "AGENT002": AgentProfile(
                agent_id="AGENT002",
                name="Mike Chen",
                skills=[AgentSkill.TECHNICAL_EXPERTISE, AgentSkill.PRODUCT_KNOWLEDGE],
                experience_level="senior",
                performance_score=4.8,
                assistance_history=[]
            ),
            "AGENT003": AgentProfile(
                agent_id="AGENT003",
                name="Lisa Rodriguez",
                skills=[AgentSkill.BILLING_SPECIALIST, AgentSkill.CUSTOMER_SERVICE],
                experience_level="junior",
                performance_score=3.9,
                assistance_history=[]
            )
        }
        
        # Sample knowledge base
        self.knowledge_base = {
            "KB001": KnowledgeArticle(
                article_id="KB001",
                title="Password Reset Process",
                content="Step-by-step guide for resetting customer passwords...",
                category="Technical Support",
                tags=["password", "reset", "authentication"],
                relevance_score=0.9,
                last_updated=datetime.now() - timedelta(days=5)
            ),
            "KB002": KnowledgeArticle(
                article_id="KB002",
                title="Billing Dispute Resolution",
                content="How to handle billing disputes and customer complaints...",
                category="Billing",
                tags=["billing", "dispute", "resolution"],
                relevance_score=0.85,
                last_updated=datetime.now() - timedelta(days=2)
            ),
            "KB003": KnowledgeArticle(
                article_id="KB003",
                title="Product Feature Guide",
                content="Complete guide to product features and capabilities...",
                category="Product Knowledge",
                tags=["features", "guide", "product"],
                relevance_score=0.8,
                last_updated=datetime.now() - timedelta(days=10)
            )
        }
    
    def start_interaction(self, customer_id: str, agent_id: str) -> str:
        """Start a new customer interaction"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        interaction_id = f"interaction_{customer_id}_{agent_id}_{int(time.time())}"
        
        interaction = CustomerInteraction(
            interaction_id=interaction_id,
            customer_id=customer_id,
            agent_id=agent_id,
            start_time=datetime.now(),
            conversation_transcript=[],
            customer_sentiment="neutral",
            resolution_status="in_progress",
            quality_score=0.0,
            assistance_requests=[]
        )
        
        self.active_interactions[interaction_id] = interaction
        self.agents[agent_id].current_session = interaction_id
        
        print(f"Started interaction {interaction_id} with agent {agent_id}")
        
        return interaction_id
    
    def provide_real_time_support(self, interaction_id: str, 
                                current_context: Dict[str, Any]) -> List[CoPilotSuggestion]:
        """Provide real-time support to agent during interaction"""
        if interaction_id not in self.active_interactions:
            return []
        
        interaction = self.active_interactions[interaction_id]
        agent = self.agents[interaction.agent_id]
        
        suggestions = []
        
        # Analyze current context and provide suggestions
        customer_sentiment = current_context.get("customer_sentiment", "neutral")
        conversation_topic = current_context.get("topic", "general")
        agent_experience = agent.experience_level
        
        # Sentiment-based suggestions
        if customer_sentiment == "frustrated":
            suggestions.append(CoPilotSuggestion(
                suggestion_id=f"suggestion_{len(suggestions)}",
                assistance_type=AssistanceType.REAL_TIME_SUPPORT,
                content="Customer appears frustrated. Consider using empathy statements and offering immediate solutions.",
                confidence=0.85,
                context={"trigger": "negative_sentiment", "experience_level": agent_experience},
                timestamp=datetime.now()
            ))
        
        # Topic-based knowledge suggestions
        if conversation_topic in ["billing", "payment", "charges"]:
            knowledge_articles = self.find_relevant_knowledge(conversation_topic)
            if knowledge_articles:
                suggestions.append(CoPilotSuggestion(
                    suggestion_id=f"suggestion_{len(suggestions)}",
                    assistance_type=AssistanceType.KNOWLEDGE_AUGMENTATION,
                    content=f"Relevant knowledge article: {knowledge_articles[0].title}",
                    confidence=0.9,
                    context={"topic": conversation_topic, "article_id": knowledge_articles[0].article_id},
                    timestamp=datetime.now()
                ))
        
        # Experience-based guidance
        if agent_experience == "junior":
            suggestions.append(CoPilotSuggestion(
                suggestion_id=f"suggestion_{len(suggestions)}",
                assistance_type=AssistanceType.TRAINING_GUIDANCE,
                content="As a junior agent, remember to confirm understanding and ask clarifying questions.",
                confidence=0.75,
                context={"experience_level": agent_experience},
                timestamp=datetime.now()
            ))
        
        # Add suggestions to history
        self.suggestions_history.extend(suggestions)
        
        return suggestions
    
    def find_relevant_knowledge(self, topic: str) -> List[KnowledgeArticle]:
        """Find relevant knowledge articles for a topic"""
        relevant_articles = []
        
        for article in self.knowledge_base.values():
            # Simple keyword matching (in real implementation, would use semantic search)
            if (topic.lower() in article.title.lower() or 
                topic.lower() in article.content.lower() or
                topic.lower() in [tag.lower() for tag in article.tags]):
                relevant_articles.append(article)
        
        # Sort by relevance score
        relevant_articles.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return relevant_articles[:3]  # Return top 3 most relevant
    
    def monitor_quality(self, interaction_id: str, 
                       conversation_segment: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor interaction quality in real-time"""
        if interaction_id not in self.active_interactions:
            return {"error": "Interaction not found"}
        
        interaction = self.active_interactions[interaction_id]
        
        # Analyze conversation segment
        quality_metrics = self.analyze_conversation_quality(conversation_segment)
        
        # Update interaction quality score
        if interaction.quality_score == 0.0:
            interaction.quality_score = quality_metrics["overall_score"]
        else:
            # Rolling average
            interaction.quality_score = (interaction.quality_score + quality_metrics["overall_score"]) / 2
        
        # Store quality metrics
        if interaction_id not in self.quality_metrics:
            self.quality_metrics[interaction_id] = []
        self.quality_metrics[interaction_id].append(quality_metrics["overall_score"])
        
        return quality_metrics
    
    def analyze_conversation_quality(self, conversation_segment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quality of conversation segment"""
        # Simulated quality analysis
        agent_response_time = conversation_segment.get("agent_response_time", 5.0)
        customer_sentiment = conversation_segment.get("customer_sentiment", "neutral")
        resolution_progress = conversation_segment.get("resolution_progress", 0.5)
        
        # Calculate quality scores
        response_time_score = max(0, 1.0 - (agent_response_time - 3.0) / 10.0)
        sentiment_score = {"positive": 1.0, "neutral": 0.7, "negative": 0.3}.get(customer_sentiment, 0.5)
        resolution_score = resolution_progress
        
        # Weighted overall score
        overall_score = (response_time_score * 0.3 + 
                        sentiment_score * 0.4 + 
                        resolution_score * 0.3)
        
        return {
            "overall_score": overall_score,
            "response_time_score": response_time_score,
            "sentiment_score": sentiment_score,
            "resolution_score": resolution_score,
            "quality_level": self.get_quality_level(overall_score),
            "improvement_suggestions": self.get_improvement_suggestions(overall_score, conversation_segment)
        }
    
    def get_quality_level(self, score: float) -> str:
        """Get quality level based on score"""
        if score >= 0.9:
            return InteractionQuality.EXCELLENT.value
        elif score >= 0.8:
            return InteractionQuality.GOOD.value
        elif score >= 0.6:
            return InteractionQuality.AVERAGE.value
        elif score >= 0.4:
            return InteractionQuality.POOR.value
        else:
            return InteractionQuality.UNACCEPTABLE.value
    
    def get_improvement_suggestions(self, score: float, 
                                  conversation_segment: Dict[str, Any]) -> List[str]:
        """Get suggestions for improvement"""
        suggestions = []
        
        if score < 0.6:
            suggestions.append("Consider using more empathy and active listening techniques")
            suggestions.append("Focus on resolving the customer's primary concern")
        
        if conversation_segment.get("agent_response_time", 0) > 8.0:
            suggestions.append("Work on reducing response time to improve customer experience")
        
        if conversation_segment.get("customer_sentiment") == "negative":
            suggestions.append("Use de-escalation techniques to improve customer sentiment")
        
        return suggestions
    
    def generate_interaction_summary(self, interaction_id: str) -> Dict[str, Any]:
        """Generate AI-powered summary of interaction"""
        if interaction_id not in self.active_interactions:
            return {"error": "Interaction not found"}
        
        interaction = self.active_interactions[interaction_id]
        
        # Analyze conversation transcript
        transcript_analysis = self.analyze_transcript(interaction.conversation_transcript)
        
        # Generate summary
        summary = {
            "interaction_id": interaction_id,
            "customer_id": interaction.customer_id,
            "agent_id": interaction.agent_id,
            "duration_minutes": (interaction.end_time - interaction.start_time).total_seconds() / 60 if interaction.end_time else 0,
            "resolution_status": interaction.resolution_status,
            "final_quality_score": interaction.quality_score,
            "customer_sentiment_trend": transcript_analysis["sentiment_trend"],
            "key_topics": transcript_analysis["key_topics"],
            "action_items": transcript_analysis["action_items"],
            "assistance_requests": len(interaction.assistance_requests),
            "ai_suggestions_provided": len([s for s in self.suggestions_history if s.assistance_type == AssistanceType.REAL_TIME_SUPPORT]),
            "summary_text": self.generate_summary_text(interaction, transcript_analysis)
        }
        
        return summary
    
    def analyze_transcript(self, transcript: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze conversation transcript"""
        # Simulated transcript analysis
        sentiments = [entry.get("sentiment", "neutral") for entry in transcript]
        topics = [entry.get("topic", "general") for entry in transcript]
        
        # Sentiment trend
        sentiment_trend = "improving" if len(sentiments) > 2 and sentiments[-1] == "positive" else "stable"
        
        # Key topics (most frequent)
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        key_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Action items (simulated)
        action_items = [
            "Follow up with customer within 24 hours",
            "Update customer profile with new preferences",
            "Escalate technical issue to engineering team"
        ]
        
        return {
            "sentiment_trend": sentiment_trend,
            "key_topics": [topic for topic, count in key_topics],
            "action_items": action_items,
            "total_exchanges": len(transcript)
        }
    
    def generate_summary_text(self, interaction: CustomerInteraction, 
                            analysis: Dict[str, Any]) -> str:
        """Generate human-readable summary text"""
        duration = (interaction.end_time - interaction.start_time).total_seconds() / 60 if interaction.end_time else 0
        
        summary = f"Interaction with customer {interaction.customer_id} lasted {duration:.1f} minutes. "
        summary += f"The conversation focused on {', '.join(analysis['key_topics'])}. "
        summary += f"Customer sentiment trend was {analysis['sentiment_trend']}. "
        summary += f"Final quality score was {interaction.quality_score:.2f}/1.0. "
        summary += f"Resolution status: {interaction.resolution_status}."
        
        return summary
    
    def end_interaction(self, interaction_id: str, 
                       final_status: str = "resolved") -> Dict[str, Any]:
        """End customer interaction and generate final report"""
        if interaction_id not in self.active_interactions:
            return {"error": "Interaction not found"}
        
        interaction = self.active_interactions[interaction_id]
        interaction.end_time = datetime.now()
        interaction.resolution_status = final_status
        
        # Generate final summary
        summary = self.generate_interaction_summary(interaction_id)
        
        # Update agent performance
        agent = self.agents[interaction.agent_id]
        agent.current_session = None
        
        # Calculate performance impact
        performance_impact = self.calculate_performance_impact(interaction)
        
        # Store interaction data
        del self.active_interactions[interaction_id]
        
        return {
            "interaction_ended": True,
            "final_summary": summary,
            "performance_impact": performance_impact,
            "agent_feedback": self.generate_agent_feedback(interaction)
        }
    
    def calculate_performance_impact(self, interaction: CustomerInteraction) -> Dict[str, Any]:
        """Calculate impact of interaction on agent performance"""
        # Simulated performance calculation
        quality_impact = interaction.quality_score * 0.1
        resolution_impact = 0.05 if interaction.resolution_status == "resolved" else -0.02
        
        return {
            "quality_impact": quality_impact,
            "resolution_impact": resolution_impact,
            "total_impact": quality_impact + resolution_impact,
            "recommendations": self.get_performance_recommendations(interaction)
        }
    
    def generate_agent_feedback(self, interaction: CustomerInteraction) -> List[str]:
        """Generate feedback for the agent"""
        feedback = []
        
        if interaction.quality_score >= 0.8:
            feedback.append("Excellent interaction! Maintain this high level of service.")
        elif interaction.quality_score >= 0.6:
            feedback.append("Good interaction. Consider focusing on customer sentiment improvement.")
        else:
            feedback.append("This interaction needs improvement. Review de-escalation techniques.")
        
        if len(interaction.assistance_requests) > 3:
            feedback.append("Consider reviewing knowledge base articles to reduce assistance requests.")
        
        return feedback
    
    def get_performance_recommendations(self, interaction: CustomerInteraction) -> List[str]:
        """Get performance improvement recommendations"""
        recommendations = []
        
        if interaction.quality_score < 0.7:
            recommendations.append("Complete advanced customer service training")
            recommendations.append("Practice active listening techniques")
        
        if interaction.resolution_status != "resolved":
            recommendations.append("Focus on first-call resolution strategies")
        
        return recommendations

def demo_ai_co_pilot():
    """Demonstrate AI co-pilot capabilities"""
    print("=" * 60)
    print("Chapter 9: AI Co-Pilot Demo")
    print("=" * 60)
    
    # Initialize the co-pilot
    co_pilot = AICoPilot()
    
    # Demo 1: Start interactions
    print("\n1. Starting Customer Interactions")
    print("-" * 30)
    
    interactions = []
    for i, agent_id in enumerate(["AGENT001", "AGENT002", "AGENT003"]):
        customer_id = f"CUST00{i+1}"
        interaction_id = co_pilot.start_interaction(customer_id, agent_id)
        interactions.append(interaction_id)
        print(f"  Started interaction {interaction_id} with agent {agent_id}")
    
    # Demo 2: Real-time support
    print("\n2. Real-time Support")
    print("-" * 30)
    
    for interaction_id in interactions:
        print(f"\nProviding support for interaction {interaction_id}:")
        
        # Simulate different contexts
        contexts = [
            {"customer_sentiment": "frustrated", "topic": "billing"},
            {"customer_sentiment": "neutral", "topic": "technical_support"},
            {"customer_sentiment": "positive", "topic": "product_inquiry"}
        ]
        
        for context in contexts:
            suggestions = co_pilot.provide_real_time_support(interaction_id, context)
            print(f"  Context: {context}")
            for suggestion in suggestions:
                print(f"    Suggestion: {suggestion.content}")
                print(f"    Type: {suggestion.assistance_type.value}")
                print(f"    Confidence: {suggestion.confidence:.2f}")
    
    # Demo 3: Quality monitoring
    print("\n3. Quality Monitoring")
    print("-" * 30)
    
    for interaction_id in interactions:
        print(f"\nMonitoring quality for interaction {interaction_id}:")
        
        # Simulate conversation segments
        segments = [
            {"agent_response_time": 3.0, "customer_sentiment": "positive", "resolution_progress": 0.8},
            {"agent_response_time": 8.0, "customer_sentiment": "negative", "resolution_progress": 0.3},
            {"agent_response_time": 5.0, "customer_sentiment": "neutral", "resolution_progress": 0.6}
        ]
        
        for i, segment in enumerate(segments):
            quality_metrics = co_pilot.monitor_quality(interaction_id, segment)
            print(f"  Segment {i+1}:")
            print(f"    Overall Score: {quality_metrics['overall_score']:.2f}")
            print(f"    Quality Level: {quality_metrics['quality_level']}")
            print(f"    Suggestions: {len(quality_metrics['improvement_suggestions'])}")
    
    # Demo 4: Knowledge augmentation
    print("\n4. Knowledge Augmentation")
    print("-" * 30)
    
    topics = ["billing", "technical_support", "product_features"]
    for topic in topics:
        articles = co_pilot.find_relevant_knowledge(topic)
        print(f"\nKnowledge for topic '{topic}':")
        for article in articles:
            print(f"  Article: {article.title}")
            print(f"  Relevance: {article.relevance_score:.2f}")
            print(f"  Category: {article.category}")
    
    # Demo 5: End interactions and generate summaries
    print("\n5. Interaction Summaries")
    print("-" * 30)
    
    for interaction_id in interactions:
        print(f"\nEnding interaction {interaction_id}:")
        result = co_pilot.end_interaction(interaction_id, "resolved")
        
        summary = result["final_summary"]
        print(f"  Duration: {summary['duration_minutes']:.1f} minutes")
        print(f"  Quality Score: {summary['final_quality_score']:.2f}")
        print(f"  Resolution Status: {summary['resolution_status']}")
        print(f"  AI Suggestions: {summary['ai_suggestions_provided']}")
        print(f"  Summary: {summary['summary_text']}")
        
        feedback = result["agent_feedback"]
        print(f"  Agent Feedback: {feedback}")
    
    print("\n" + "=" * 60)
    print("AI Co-Pilot Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("  ✓ Real-time agent support")
    print("  ✓ Knowledge augmentation")
    print("  ✓ Quality monitoring")
    print("  ✓ Performance tracking")
    print("  ✓ AI-powered summarization")
    print("  ✓ Training guidance")
    print("  ✓ Intelligent suggestions")

if __name__ == "__main__":
    demo_ai_co_pilot()
