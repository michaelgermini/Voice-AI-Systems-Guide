#!/usr/bin/env python3
"""
Voice Quality Metrics Demo - Chapter 1
Demonstrates how to measure and evaluate TTS performance for contact centers.
"""

import os
import time
import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VoiceQualityMetrics:
    """Container for voice quality metrics"""
    platform: str
    voice_id: str
    text_length: int
    latency_ms: float
    naturalness_score: float
    intelligibility_score: float
    prosody_score: float
    overall_score: float
    cost_per_1k_chars: float
    timestamp: datetime

class VoiceQualityEvaluator:
    """Evaluates voice quality metrics for TTS systems"""
    
    def __init__(self):
        self.test_phrases = [
            "Welcome to our customer service center.",
            "Your account balance is $1,234.56.",
            "Please press 1 for sales, 2 for support.",
            "Thank you for calling. Have a great day!",
            "I understand your concern. Let me help you with that.",
            "Your request has been processed successfully.",
            "Please hold while I transfer you to an agent.",
            "We apologize for the inconvenience.",
            "Your order number is 123456789.",
            "The estimated delivery time is 3-5 business days."
        ]
        
        # Quality thresholds for different use cases
        self.quality_thresholds = {
            "ivr_prompts": {
                "min_naturalness": 6.0,
                "min_intelligibility": 8.5,
                "max_latency_ms": 1000
            },
            "conversational_ai": {
                "min_naturalness": 8.0,
                "min_intelligibility": 9.0,
                "max_latency_ms": 800
            },
            "premium_service": {
                "min_naturalness": 9.0,
                "min_intelligibility": 9.5,
                "max_latency_ms": 500
            }
        }

    def simulate_voice_quality_measurement(self, platform: str, voice: str, text: str) -> VoiceQualityMetrics:
        """Simulate voice quality measurement for demonstration"""
        
        # Simulate different quality characteristics based on platform
        platform_characteristics = {
            "azure_neural": {
                "base_naturalness": 9.2,
                "base_intelligibility": 9.4,
                "base_prosody": 9.1,
                "latency_factor": 1.2,
                "cost_per_1k": 16.00
            },
            "amazon_polly": {
                "base_naturalness": 8.8,
                "base_intelligibility": 9.2,
                "base_prosody": 8.9,
                "latency_factor": 1.0,
                "cost_per_1k": 4.00
            },
            "google_tts": {
                "base_naturalness": 8.9,
                "base_intelligibility": 9.3,
                "base_prosody": 8.8,
                "latency_factor": 1.1,
                "cost_per_1k": 4.00
            },
            "legacy_concatenative": {
                "base_naturalness": 4.5,
                "base_intelligibility": 7.8,
                "base_prosody": 3.2,
                "latency_factor": 0.3,
                "cost_per_1k": 0.50
            }
        }
        
        char = platform_characteristics.get(platform, platform_characteristics["amazon_polly"])
        
        # Calculate latency based on text length and platform
        base_latency = 200 + (len(text) * char["latency_factor"])
        latency = base_latency + (time.time() % 100)  # Add some randomness
        
        # Calculate quality scores with some variation
        naturalness = char["base_naturalness"] + (time.time() % 0.6) - 0.3
        intelligibility = char["base_intelligibility"] + (time.time() % 0.4) - 0.2
        prosody = char["base_prosody"] + (time.time() % 0.5) - 0.25
        
        # Clamp scores to valid range
        naturalness = max(1.0, min(10.0, naturalness))
        intelligibility = max(1.0, min(10.0, intelligibility))
        prosody = max(1.0, min(10.0, prosody))
        
        # Calculate overall score (weighted average)
        overall_score = (naturalness * 0.4 + intelligibility * 0.4 + prosody * 0.2)
        
        return VoiceQualityMetrics(
            platform=platform,
            voice_id=voice,
            text_length=len(text),
            latency_ms=latency,
            naturalness_score=naturalness,
            intelligibility_score=intelligibility,
            prosody_score=prosody,
            overall_score=overall_score,
            cost_per_1k_chars=char["cost_per_1k"],
            timestamp=datetime.now()
        )

    def evaluate_platform_performance(self, platform: str, voice: str) -> List[VoiceQualityMetrics]:
        """Evaluate performance across all test phrases"""
        results = []
        
        logger.info(f"Evaluating {platform} with voice {voice}")
        
        for phrase in self.test_phrases:
            metrics = self.simulate_voice_quality_measurement(platform, voice, phrase)
            results.append(metrics)
            
            # Simulate processing time
            time.sleep(0.1)
        
        return results

    def calculate_platform_statistics(self, metrics_list: List[VoiceQualityMetrics]) -> Dict:
        """Calculate comprehensive statistics for a platform"""
        if not metrics_list:
            return {}
        
        # Calculate averages
        avg_latency = sum(m.latency_ms for m in metrics_list) / len(metrics_list)
        avg_naturalness = sum(m.naturalness_score for m in metrics_list) / len(metrics_list)
        avg_intelligibility = sum(m.intelligibility_score for m in metrics_list) / len(metrics_list)
        avg_prosody = sum(m.prosody_score for m in metrics_list) / len(metrics_list)
        avg_overall = sum(m.overall_score for m in metrics_list) / len(metrics_list)
        
        # Calculate standard deviations
        latency_std = math.sqrt(sum((m.latency_ms - avg_latency) ** 2 for m in metrics_list) / len(metrics_list))
        naturalness_std = math.sqrt(sum((m.naturalness_score - avg_naturalness) ** 2 for m in metrics_list) / len(metrics_list))
        
        # Calculate cost efficiency
        total_chars = sum(m.text_length for m in metrics_list)
        total_cost = sum(m.text_length * m.cost_per_1k_chars / 1000 for m in metrics_list)
        cost_per_char = total_cost / total_chars if total_chars > 0 else 0
        
        return {
            "platform": metrics_list[0].platform,
            "voice": metrics_list[0].voice_id,
            "test_count": len(metrics_list),
            "total_chars": total_chars,
            "avg_latency_ms": avg_latency,
            "latency_std_ms": latency_std,
            "avg_naturalness": avg_naturalness,
            "naturalness_std": naturalness_std,
            "avg_intelligibility": avg_intelligibility,
            "avg_prosody": avg_prosody,
            "avg_overall_score": avg_overall,
            "total_cost": total_cost,
            "cost_per_char": cost_per_char,
            "cost_per_1k_chars": metrics_list[0].cost_per_1k_chars
        }

    def assess_use_case_suitability(self, stats: Dict, use_case: str) -> Dict:
        """Assess suitability for specific use cases"""
        thresholds = self.quality_thresholds.get(use_case, self.quality_thresholds["ivr_prompts"])
        
        assessment = {
            "use_case": use_case,
            "platform": stats["platform"],
            "voice": stats["voice"],
            "passes_naturalness": stats["avg_naturalness"] >= thresholds["min_naturalness"],
            "passes_intelligibility": stats["avg_intelligibility"] >= thresholds["min_intelligibility"],
            "passes_latency": stats["avg_latency_ms"] <= thresholds["max_latency_ms"],
            "overall_suitable": True,
            "recommendations": []
        }
        
        # Check each criterion
        if not assessment["passes_naturalness"]:
            assessment["overall_suitable"] = False
            assessment["recommendations"].append(
                f"Naturalness score ({stats['avg_naturalness']:.1f}) below threshold ({thresholds['min_naturalness']})"
            )
        
        if not assessment["passes_intelligibility"]:
            assessment["overall_suitable"] = False
            assessment["recommendations"].append(
                f"Intelligibility score ({stats['avg_intelligibility']:.1f}) below threshold ({thresholds['min_intelligibility']})"
            )
        
        if not assessment["passes_latency"]:
            assessment["overall_suitable"] = False
            assessment["recommendations"].append(
                f"Latency ({stats['avg_latency_ms']:.0f}ms) above threshold ({thresholds['max_latency_ms']}ms)"
            )
        
        if assessment["overall_suitable"]:
            assessment["recommendations"].append("Platform suitable for this use case")
        
        return assessment

    def generate_quality_report(self, all_stats: List[Dict]) -> Dict:
        """Generate comprehensive quality report"""
        report = {
            "summary": {},
            "rankings": {},
            "use_case_assessments": {},
            "recommendations": []
        }
        
        # Overall summary
        report["summary"] = {
            "platforms_tested": len(all_stats),
            "total_tests": sum(s["test_count"] for s in all_stats),
            "total_chars_processed": sum(s["total_chars"] for s in all_stats),
            "total_cost": sum(s["total_cost"] for s in all_stats)
        }
        
        # Rankings
        report["rankings"] = {
            "by_overall_score": sorted(all_stats, key=lambda x: x["avg_overall_score"], reverse=True),
            "by_latency": sorted(all_stats, key=lambda x: x["avg_latency_ms"]),
            "by_cost_efficiency": sorted(all_stats, key=lambda x: x["cost_per_char"]),
            "by_naturalness": sorted(all_stats, key=lambda x: x["avg_naturalness"], reverse=True)
        }
        
        # Use case assessments
        use_cases = ["ivr_prompts", "conversational_ai", "premium_service"]
        for use_case in use_cases:
            report["use_case_assessments"][use_case] = [
                self.assess_use_case_suitability(stats, use_case) for stats in all_stats
            ]
        
        # Generate recommendations
        best_overall = report["rankings"]["by_overall_score"][0]
        fastest = report["rankings"]["by_latency"][0]
        cheapest = report["rankings"]["by_cost_efficiency"][0]
        
        report["recommendations"] = [
            f"Best Overall Quality: {best_overall['platform']} ({best_overall['avg_overall_score']:.1f})",
            f"Fastest: {fastest['platform']} ({fastest['avg_latency_ms']:.0f}ms average)",
            f"Most Cost-Effective: {cheapest['platform']} (${cheapest['cost_per_char']:.6f} per character)",
            "For IVR: Consider latency and intelligibility over naturalness",
            "For Conversational AI: Prioritize naturalness and overall quality",
            "For Premium Service: All metrics should meet high thresholds"
        ]
        
        return report

    def print_quality_report(self, report: Dict):
        """Print formatted quality report"""
        print("\n" + "="*80)
        print("VOICE QUALITY METRICS REPORT - Chapter 1")
        print("="*80)
        
        # Summary
        summary = report["summary"]
        print(f"\n📊 SUMMARY")
        print(f"   Platforms Tested: {summary['platforms_tested']}")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Characters Processed: {summary['total_chars_processed']:,}")
        print(f"   Total Cost: ${summary['total_cost']:.4f}")
        
        # Rankings
        print(f"\n🏆 RANKINGS")
        
        print(f"\n   Overall Quality:")
        for i, platform in enumerate(report["rankings"]["by_overall_score"], 1):
            print(f"     {i}. {platform['platform']}: {platform['avg_overall_score']:.1f}")
        
        print(f"\n   Latency (Fastest First):")
        for i, platform in enumerate(report["rankings"]["by_latency"], 1):
            print(f"     {i}. {platform['platform']}: {platform['avg_latency_ms']:.0f}ms")
        
        print(f"\n   Cost Efficiency (Cheapest First):")
        for i, platform in enumerate(report["rankings"]["by_cost_efficiency"], 1):
            print(f"     {i}. {platform['platform']}: ${platform['cost_per_char']:.6f}/char")
        
        # Use case assessments
        print(f"\n🎯 USE CASE ASSESSMENTS")
        for use_case, assessments in report["use_case_assessments"].items():
            print(f"\n   {use_case.upper().replace('_', ' ')}:")
            for assessment in assessments:
                status = "✅" if assessment["overall_suitable"] else "❌"
                print(f"     {status} {assessment['platform']}: {assessment['avg_overall_score']:.1f}")
                if not assessment["overall_suitable"]:
                    for rec in assessment["recommendations"]:
                        print(f"        - {rec}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        for rec in report["recommendations"]:
            print(f"   • {rec}")
        
        print("\n" + "="*80)

    def run_evaluation(self):
        """Run complete voice quality evaluation"""
        print("🎤 Chapter 1: Voice Quality Metrics Demo")
        print("="*50)
        
        # Test platforms
        platforms_to_test = [
            ("azure_neural", "JennyNeural"),
            ("amazon_polly", "Joanna"),
            ("google_tts", "en-US-Standard-A"),
            ("legacy_concatenative", "SystemVoice")
        ]
        
        all_stats = []
        
        # Evaluate each platform
        for platform, voice in platforms_to_test:
            logger.info(f"Evaluating {platform}...")
            metrics = self.evaluate_platform_performance(platform, voice)
            stats = self.calculate_platform_statistics(metrics)
            all_stats.append(stats)
        
        # Generate and print report
        report = self.generate_quality_report(all_stats)
        self.print_quality_report(report)
        
        print("\n✅ Voice quality evaluation completed!")
        print("   This demonstrates how to measure and compare TTS performance for contact centers.")

if __name__ == "__main__":
    evaluator = VoiceQualityEvaluator()
    evaluator.run_evaluation()
