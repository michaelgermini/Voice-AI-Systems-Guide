#!/usr/bin/env python3
"""
Basic TTS Demo - Chapter 1
Demonstrates the evolution of TTS technology from concatenative to neural approaches.
"""

import os
import time
import json
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TTSResult:
    """Container for TTS generation results"""
    platform: str
    generation: str
    text: str
    audio_url: Optional[str] = None
    latency_ms: Optional[float] = None
    quality_score: Optional[float] = None
    cost_per_1k_chars: Optional[float] = None

class TTSDemo:
    """Demonstrates different TTS generations and platforms"""
    
    def __init__(self):
        self.test_texts = {
            "greeting": "Welcome to our customer service. How may I help you today?",
            "account_info": "Your account balance is $1,234.56. Your last transaction was on March 15th.",
            "multilingual": "Bienvenue au service client. Comment puis-je vous aider aujourd'hui?",
            "technical": "Please press 1 for sales, 2 for technical support, or 3 to speak with an agent."
        }
        
        # Platform configurations (API keys would be loaded from environment)
        self.platforms = {
            "azure_neural": {
                "name": "Microsoft Azure Neural TTS",
                "generation": "Neural (NTTS)",
                "cost_per_1k": 16.00,  # $16 per 1M characters
                "quality_score": 9.2
            },
            "amazon_polly": {
                "name": "Amazon Polly Neural",
                "generation": "Neural (NTTS)", 
                "cost_per_1k": 4.00,   # $4 per 1M characters
                "quality_score": 8.8
            },
            "google_tts": {
                "name": "Google Cloud TTS",
                "generation": "Neural (NTTS)",
                "cost_per_1k": 4.00,   # $4 per 1M characters
                "quality_score": 8.9
            },
            "legacy_ivr": {
                "name": "Legacy Concatenative TTS",
                "generation": "Concatenative",
                "cost_per_1k": 0.50,   # Estimated cost
                "quality_score": 4.5
            }
        }

    def simulate_tts_generation(self, platform: str, text: str) -> TTSResult:
        """Simulate TTS generation for demonstration purposes"""
        config = self.platforms[platform]
        
        # Simulate different latencies based on generation type
        if config["generation"] == "Neural (NTTS)":
            latency = 800 + (len(text) * 2)  # Neural TTS is slower but higher quality
        else:
            latency = 200 + (len(text) * 0.5)  # Concatenative is faster but robotic
        
        # Simulate API call
        time.sleep(latency / 1000)  # Convert to seconds for demo
        
        return TTSResult(
            platform=config["name"],
            generation=config["generation"],
            text=text,
            audio_url=f"https://api.example.com/tts/{platform}/audio.mp3",
            latency_ms=latency,
            quality_score=config["quality_score"],
            cost_per_1k_chars=config["cost_per_1k"]
        )

    def compare_generations(self) -> Dict[str, List[TTSResult]]:
        """Compare different TTS generations using the same text"""
        results = {}
        
        for text_name, text in self.test_texts.items():
            results[text_name] = []
            
            for platform in self.platforms.keys():
                logger.info(f"Generating TTS for {platform} with text: {text[:50]}...")
                result = self.simulate_tts_generation(platform, text)
                results[text_name].append(result)
        
        return results

    def analyze_performance(self, results: Dict[str, List[TTSResult]]) -> Dict:
        """Analyze performance metrics across platforms"""
        analysis = {
            "average_latency": {},
            "cost_comparison": {},
            "quality_ranking": [],
            "recommendations": []
        }
        
        # Calculate average latency per platform
        platform_latencies = {}
        platform_costs = {}
        
        for text_results in results.values():
            for result in text_results:
                platform = result.platform
                if platform not in platform_latencies:
                    platform_latencies[platform] = []
                    platform_costs[platform] = []
                
                platform_latencies[platform].append(result.latency_ms)
                platform_costs[platform].append(result.cost_per_1k_chars)
        
        # Calculate averages
        for platform, latencies in platform_latencies.items():
            analysis["average_latency"][platform] = sum(latencies) / len(latencies)
            analysis["cost_comparison"][platform] = platform_costs[platform][0]  # Same for all texts
        
        # Quality ranking
        quality_scores = [(result.platform, result.quality_score) 
                         for results_list in results.values() 
                         for result in results_list]
        analysis["quality_ranking"] = sorted(set(quality_scores), 
                                           key=lambda x: x[1], reverse=True)
        
        # Generate recommendations
        best_quality = max(analysis["quality_ranking"], key=lambda x: x[1])
        fastest = min(analysis["average_latency"].items(), key=lambda x: x[1])
        cheapest = min(analysis["cost_comparison"].items(), key=lambda x: x[1])
        
        analysis["recommendations"] = [
            f"Best Quality: {best_quality[0]} (Score: {best_quality[1]})",
            f"Fastest: {fastest[0]} ({fastest[1]:.0f}ms average)",
            f"Most Cost-Effective: {cheapest[0]} (${cheapest[1]:.2f}/1K chars)"
        ]
        
        return analysis

    def print_comparison_table(self, results: Dict[str, List[TTSResult]]):
        """Print a formatted comparison table"""
        print("\n" + "="*80)
        print("TTS GENERATION COMPARISON - Chapter 1 Demo")
        print("="*80)
        
        for text_name, text_results in results.items():
            print(f"\n📝 Text: {text_name}")
            print(f"Content: {text_results[0].text[:60]}...")
            print("-" * 80)
            print(f"{'Platform':<25} {'Generation':<15} {'Latency':<10} {'Quality':<8} {'Cost/1K':<10}")
            print("-" * 80)
            
            for result in text_results:
                print(f"{result.platform:<25} {result.generation:<15} "
                      f"{result.latency_ms:<10.0f} {result.quality_score:<8.1f} "
                      f"${result.cost_per_1k_chars:<9.2f}")
        
        print("\n" + "="*80)

    def run_demo(self):
        """Run the complete TTS demonstration"""
        print("🎤 Chapter 1: TTS Generation Evolution Demo")
        print("="*50)
        
        # Run comparison
        results = self.compare_generations()
        
        # Print results
        self.print_comparison_table(results)
        
        # Analyze performance
        analysis = self.analyze_performance(results)
        
        # Print analysis
        print("\n📊 PERFORMANCE ANALYSIS")
        print("="*30)
        
        print("\n🏆 Quality Ranking:")
        for i, (platform, score) in enumerate(analysis["quality_ranking"], 1):
            print(f"  {i}. {platform}: {score}")
        
        print("\n⚡ Average Latency:")
        for platform, latency in analysis["average_latency"].items():
            print(f"  {platform}: {latency:.0f}ms")
        
        print("\n💰 Cost per 1,000 characters:")
        for platform, cost in analysis["cost_comparison"].items():
            print(f"  {platform}: ${cost:.2f}")
        
        print("\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"  • {rec}")
        
        print("\n" + "="*50)
        print("✅ Demo completed! This demonstrates the evolution from")
        print("   concatenative to neural TTS in contact center applications.")

if __name__ == "__main__":
    demo = TTSDemo()
    demo.run_demo()
