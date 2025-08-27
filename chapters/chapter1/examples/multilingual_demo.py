#!/usr/bin/env python3
"""
Multilingual TTS Demo - Chapter 1
Demonstrates multilingual capabilities for global contact centers.
"""

import os
import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LanguageConfig:
    """Configuration for supported languages"""
    code: str
    name: str
    native_name: str
    voice_options: List[str]
    greeting: str
    account_info: str
    support_options: str

class MultilingualTTSDemo:
    """Demonstrates multilingual TTS capabilities"""
    
    def __init__(self):
        self.languages = {
            "en-US": LanguageConfig(
                code="en-US",
                name="English (US)",
                native_name="English",
                voice_options=["JennyNeural", "GuyNeural", "AriaNeural"],
                greeting="Hello, welcome to our customer service. How may I help you today?",
                account_info="Your account balance is $1,234.56. Your last transaction was on March 15th.",
                support_options="Please press 1 for sales, 2 for technical support, or 3 to speak with an agent."
            ),
            "fr-FR": LanguageConfig(
                code="fr-FR",
                name="French",
                native_name="Français",
                voice_options=["DeniseNeural", "HenriNeural", "BrigitteNeural"],
                greeting="Bonjour, bienvenue au service client. Comment puis-je vous aider aujourd'hui?",
                account_info="Votre solde de compte est de 1 234,56 €. Votre dernière transaction était le 15 mars.",
                support_options="Veuillez appuyer sur 1 pour les ventes, 2 pour le support technique, ou 3 pour parler avec un agent."
            ),
            "es-ES": LanguageConfig(
                code="es-ES",
                name="Spanish",
                native_name="Español",
                voice_options=["ElviraNeural", "AlvaroNeural", "CarmenNeural"],
                greeting="Hola, bienvenido a nuestro servicio al cliente. ¿Cómo puedo ayudarle hoy?",
                account_info="Su saldo de cuenta es de 1.234,56 €. Su última transacción fue el 15 de marzo.",
                support_options="Por favor, pulse 1 para ventas, 2 para soporte técnico, o 3 para hablar con un agente."
            ),
            "de-DE": LanguageConfig(
                code="de-DE",
                name="German",
                native_name="Deutsch",
                voice_options=["KatjaNeural", "ConradNeural", "AmalaNeural"],
                greeting="Hallo, willkommen beim Kundenservice. Wie kann ich Ihnen heute helfen?",
                account_info="Ihr Kontostand beträgt 1.234,56 €. Ihre letzte Transaktion war am 15. März.",
                support_options="Bitte drücken Sie 1 für Verkauf, 2 für technischen Support oder 3, um mit einem Agenten zu sprechen."
            ),
            "it-IT": LanguageConfig(
                code="it-IT",
                name="Italian",
                native_name="Italiano",
                voice_options=["IsabellaNeural", "DiegoNeural", "ElsaNeural"],
                greeting="Ciao, benvenuto al servizio clienti. Come posso aiutarti oggi?",
                account_info="Il saldo del tuo account è di 1.234,56 €. La tua ultima transazione è stata il 15 marzo.",
                support_options="Premi 1 per le vendite, 2 per il supporto tecnico, o 3 per parlare con un agente."
            ),
            "pt-BR": LanguageConfig(
                code="pt-BR",
                name="Portuguese (Brazil)",
                native_name="Português",
                voice_options=["FranciscaNeural", "AntonioNeural", "BrendaNeural"],
                greeting="Olá, bem-vindo ao nosso serviço ao cliente. Como posso ajudá-lo hoje?",
                account_info="Seu saldo da conta é de R$ 1.234,56. Sua última transação foi em 15 de março.",
                support_options="Pressione 1 para vendas, 2 para suporte técnico, ou 3 para falar com um agente."
            ),
            "ja-JP": LanguageConfig(
                code="ja-JP",
                name="Japanese",
                native_name="日本語",
                voice_options=["NanamiNeural", "KeitaNeural", "NaokiNeural"],
                greeting="こんにちは、カスタマーサービスへようこそ。今日はどのようにお手伝いできますか？",
                account_info="お客様の口座残高は1,234.56ドルです。最後の取引は3月15日でした。",
                support_options="営業については1、技術サポートについては2、オペレーターとの通話については3を押してください。"
            ),
            "zh-CN": LanguageConfig(
                code="zh-CN",
                name="Chinese (Simplified)",
                native_name="中文",
                voice_options=["XiaoxiaoNeural", "YunxiNeural", "YunyangNeural"],
                greeting="您好，欢迎致电客户服务。今天我能为您做些什么？",
                account_info="您的账户余额为1,234.56美元。您的最后一笔交易是在3月15日。",
                support_options="请按1查询销售，按2查询技术支持，或按3与客服代表通话。"
            )
        }
        
        # Contact center scenarios
        self.scenarios = {
            "greeting": "greeting",
            "account_info": "account_info", 
            "support_options": "support_options"
        }

    def simulate_multilingual_tts(self, language_code: str, text: str, voice: str = None) -> Dict:
        """Simulate TTS generation for a specific language"""
        lang_config = self.languages[language_code]
        
        if voice is None:
            voice = lang_config.voice_options[0]
        
        # Simulate different processing times based on language complexity
        base_latency = 500  # Base latency in ms
        char_multiplier = {
            "en-US": 2.0,
            "fr-FR": 2.2,
            "es-ES": 2.1,
            "de-DE": 2.3,
            "it-IT": 2.1,
            "pt-BR": 2.0,
            "ja-JP": 3.0,  # Japanese characters are more complex
            "zh-CN": 2.8   # Chinese characters are more complex
        }
        
        latency = base_latency + (len(text) * char_multiplier.get(language_code, 2.0))
        time.sleep(latency / 1000)  # Simulate processing time
        
        return {
            "language_code": language_code,
            "language_name": lang_config.name,
            "native_name": lang_config.native_name,
            "voice": voice,
            "text": text,
            "latency_ms": latency,
            "audio_url": f"https://tts.example.com/{language_code}/{voice}/{hash(text)}.mp3",
            "success": True
        }

    def run_language_comparison(self) -> Dict[str, List[Dict]]:
        """Run TTS comparison across all languages"""
        results = {}
        
        for scenario_name, scenario_key in self.scenarios.items():
            results[scenario_name] = []
            
            logger.info(f"Running scenario: {scenario_name}")
            
            for lang_code, lang_config in self.languages.items():
                text = getattr(lang_config, scenario_key)
                
                logger.info(f"  Generating {lang_config.name} ({lang_config.native_name})")
                result = self.simulate_multilingual_tts(lang_code, text)
                results[scenario_name].append(result)
        
        return results

    def analyze_multilingual_performance(self, results: Dict[str, List[Dict]]) -> Dict:
        """Analyze performance across different languages"""
        analysis = {
            "language_stats": {},
            "scenario_stats": {},
            "voice_quality_ranking": [],
            "recommendations": []
        }
        
        # Language statistics
        all_results = []
        for scenario_results in results.values():
            all_results.extend(scenario_results)
        
        for lang_code in self.languages.keys():
            lang_results = [r for r in all_results if r["language_code"] == lang_code]
            
            avg_latency = sum(r["latency_ms"] for r in lang_results) / len(lang_results)
            total_chars = sum(len(r["text"]) for r in lang_results)
            
            analysis["language_stats"][lang_code] = {
                "name": self.languages[lang_code].name,
                "native_name": self.languages[lang_code].native_name,
                "avg_latency_ms": avg_latency,
                "total_chars": total_chars,
                "scenarios_tested": len(lang_results)
            }
        
        # Scenario statistics
        for scenario_name, scenario_results in results.items():
            avg_latency = sum(r["latency_ms"] for r in scenario_results) / len(scenario_results)
            analysis["scenario_stats"][scenario_name] = {
                "avg_latency_ms": avg_latency,
                "languages_tested": len(scenario_results)
            }
        
        # Voice quality ranking (simulated based on language complexity)
        quality_scores = {
            "en-US": 9.5, "fr-FR": 9.3, "es-ES": 9.2, "de-DE": 9.1,
            "it-IT": 9.0, "pt-BR": 8.9, "ja-JP": 8.7, "zh-CN": 8.8
        }
        
        analysis["voice_quality_ranking"] = sorted(
            [(lang_code, quality_scores[lang_code]) for lang_code in self.languages.keys()],
            key=lambda x: x[1], reverse=True
        )
        
        # Generate recommendations
        fastest_lang = min(analysis["language_stats"].items(), key=lambda x: x[1]["avg_latency_ms"])
        best_quality = max(analysis["voice_quality_ranking"], key=lambda x: x[1])
        
        analysis["recommendations"] = [
            f"Fastest Language: {fastest_lang[1]['name']} ({fastest_lang[1]['avg_latency_ms']:.0f}ms average)",
            f"Best Quality: {self.languages[best_quality[0]].name} (Score: {best_quality[1]})",
            "For global deployment: Consider regional TTS servers for lower latency",
            "Japanese and Chinese require more processing time due to character complexity"
        ]
        
        return analysis

    def print_multilingual_report(self, results: Dict[str, List[Dict]], analysis: Dict):
        """Print detailed multilingual comparison report"""
        print("\n" + "="*80)
        print("MULTILINGUAL TTS COMPARISON REPORT - Chapter 1")
        print("="*80)
        
        # Scenario results
        for scenario_name, scenario_results in results.items():
            print(f"\n📝 Scenario: {scenario_name.upper()}")
            print("-" * 80)
            print(f"{'Language':<20} {'Native':<15} {'Voice':<15} {'Latency':<10} {'Chars':<8}")
            print("-" * 80)
            
            for result in scenario_results:
                print(f"{result['language_name']:<20} {result['native_name']:<15} "
                      f"{result['voice']:<15} {result['latency_ms']:<10.0f} {len(result['text']):<8}")
        
        # Analysis summary
        print("\n" + "="*80)
        print("📊 MULTILINGUAL ANALYSIS")
        print("="*80)
        
        print("\n🌍 Language Performance:")
        for lang_code, stats in analysis["language_stats"].items():
            print(f"  {stats['name']} ({stats['native_name']}): {stats['avg_latency_ms']:.0f}ms average")
        
        print("\n🎯 Scenario Performance:")
        for scenario, stats in analysis["scenario_stats"].items():
            print(f"  {scenario}: {stats['avg_latency_ms']:.0f}ms average across {stats['languages_tested']} languages")
        
        print("\n🏆 Voice Quality Ranking:")
        for i, (lang_code, score) in enumerate(analysis["voice_quality_ranking"], 1):
            lang_name = self.languages[lang_code].name
            print(f"  {i}. {lang_name}: {score}")
        
        print("\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"  • {rec}")
        
        print("\n" + "="*80)

    def demonstrate_contact_center_flow(self):
        """Demonstrate a complete multilingual contact center flow"""
        print("\n🎯 MULTILINGUAL CONTACT CENTER FLOW DEMO")
        print("="*50)
        
        # Simulate a customer calling from different regions
        customer_scenarios = [
            {"region": "US", "language": "en-US", "name": "John"},
            {"region": "France", "language": "fr-FR", "name": "Marie"},
            {"region": "Spain", "language": "es-ES", "name": "Carlos"},
            {"region": "Germany", "language": "de-DE", "name": "Hans"},
            {"region": "Japan", "language": "ja-JP", "name": "Yuki"}
        ]
        
        for customer in customer_scenarios:
            lang_code = customer["language"]
            lang_config = self.languages[lang_code]
            
            print(f"\n📞 Customer: {customer['name']} from {customer['region']}")
            print(f"   Language: {lang_config.name} ({lang_config.native_name})")
            
            # Generate greeting
            greeting_result = self.simulate_multilingual_tts(
                lang_code, lang_config.greeting
            )
            print(f"   Greeting: {lang_config.greeting}")
            print(f"   Generated in: {greeting_result['latency_ms']:.0f}ms")
            
            # Generate account info
            account_result = self.simulate_multilingual_tts(
                lang_code, lang_config.account_info
            )
            print(f"   Account Info: {lang_config.account_info[:50]}...")
            print(f"   Generated in: {account_result['latency_ms']:.0f}ms")
            
            print("   " + "-" * 40)

    def run_demo(self):
        """Run the complete multilingual demonstration"""
        print("🌍 Chapter 1: Multilingual TTS Demo")
        print("="*50)
        
        # Run language comparison
        results = self.run_language_comparison()
        
        # Analyze results
        analysis = self.analyze_multilingual_performance(results)
        
        # Print report
        self.print_multilingual_report(results, analysis)
        
        # Demonstrate contact center flow
        self.demonstrate_contact_center_flow()
        
        print("\n✅ Multilingual demo completed!")
        print("   This demonstrates global TTS capabilities for international contact centers.")

if __name__ == "__main__":
    demo = MultilingualTTSDemo()
    demo.run_demo()
