#!/usr/bin/env python3
"""
Chapter 1 Demo Runner
Runs all Chapter 1 demonstrations in sequence.
"""

import sys
import os
import time
import asyncio

# Add the examples directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))

def run_basic_tts_demo():
    """Run the basic TTS generation comparison demo"""
    print("\n" + "="*60)
    print("🎤 RUNNING: Basic TTS Generation Comparison")
    print("="*60)
    
    try:
        from basic_tts_demo import TTSDemo
        demo = TTSDemo()
        demo.run_demo()
        return True
    except Exception as e:
        print(f"❌ Error running basic TTS demo: {e}")
        return False

async def run_platform_comparison():
    """Run the platform comparison demo"""
    print("\n" + "="*60)
    print("🔍 RUNNING: TTS Platform Comparison")
    print("="*60)
    
    try:
        from platform_comparison import TTSPlatformComparison
        comparison = TTSPlatformComparison()
        results = await comparison.run_platform_comparison()
        analysis = comparison.analyze_results(results)
        comparison.print_comparison_report(results, analysis)
        return True
    except Exception as e:
        print(f"❌ Error running platform comparison: {e}")
        return False

def run_multilingual_demo():
    """Run the multilingual TTS demo"""
    print("\n" + "="*60)
    print("🌍 RUNNING: Multilingual TTS Demo")
    print("="*60)
    
    try:
        from multilingual_demo import MultilingualTTSDemo
        demo = MultilingualTTSDemo()
        demo.run_demo()
        return True
    except Exception as e:
        print(f"❌ Error running multilingual demo: {e}")
        return False

def run_voice_quality_metrics():
    """Run the voice quality metrics demo"""
    print("\n" + "="*60)
    print("📊 RUNNING: Voice Quality Metrics")
    print("="*60)
    
    try:
        from voice_quality_metrics import VoiceQualityEvaluator
        evaluator = VoiceQualityEvaluator()
        evaluator.run_evaluation()
        return True
    except Exception as e:
        print(f"❌ Error running voice quality metrics: {e}")
        return False

def print_chapter_summary():
    """Print a summary of Chapter 1 concepts"""
    print("\n" + "="*80)
    print("📚 CHAPTER 1 SUMMARY: Introduction to Voice Synthesis")
    print("="*80)
    
    summary_points = [
        "✅ Evolution of TTS: From concatenative to neural approaches",
        "✅ Platform Comparison: Azure, Amazon, Google Cloud TTS",
        "✅ Multilingual Support: 8 languages demonstrated",
        "✅ Quality Metrics: Naturalness, intelligibility, prosody",
        "✅ Cost Analysis: Pricing comparison across platforms",
        "✅ Use Case Assessment: IVR, conversational AI, premium service"
    ]
    
    for point in summary_points:
        print(f"   {point}")
    
    print("\n🎯 Key Takeaways:")
    print("   • Neural TTS provides human-like quality but higher cost")
    print("   • Platform choice depends on use case requirements")
    print("   • Multilingual support enables global contact centers")
    print("   • Quality metrics help optimize for specific scenarios")
    
    print("\n📖 Next: Chapter 2 - Natural Language Processing in Call Centers")
    print("="*80)

async def main():
    """Run all Chapter 1 demonstrations"""
    print("🎤 Chapter 1: Introduction to Voice Synthesis")
    print("Complete Demo Suite")
    print("="*50)
    
    start_time = time.time()
    results = []
    
    # Run all demos
    print("\n🚀 Starting Chapter 1 demonstrations...")
    
    # Basic TTS Demo
    results.append(("Basic TTS Demo", run_basic_tts_demo()))
    
    # Platform Comparison (async)
    results.append(("Platform Comparison", await run_platform_comparison()))
    
    # Multilingual Demo
    results.append(("Multilingual Demo", run_multilingual_demo()))
    
    # Voice Quality Metrics
    results.append(("Voice Quality Metrics", run_voice_quality_metrics()))
    
    # Print results summary
    print("\n" + "="*60)
    print("📋 DEMO RESULTS SUMMARY")
    print("="*60)
    
    successful_demos = 0
    for demo_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {demo_name}: {status}")
        if success:
            successful_demos += 1
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Results: {successful_demos}/{len(results)} demos completed successfully")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    # Print chapter summary
    print_chapter_summary()
    
    if successful_demos == len(results):
        print("\n🎉 All Chapter 1 demonstrations completed successfully!")
        print("   You now have a comprehensive understanding of voice synthesis fundamentals.")
    else:
        print(f"\n⚠️  {len(results) - successful_demos} demo(s) failed.")
        print("   Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    asyncio.run(main())
