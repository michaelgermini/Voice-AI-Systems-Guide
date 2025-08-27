#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Example: Auto-scaling Configuration

This example demonstrates how to configure auto-scaling for voice AI services
using Kubernetes HPA and custom metrics.
"""

import time
import json
import uuid
import asyncio
import threading
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import math

@dataclass
class ScalingMetrics:
    cpu_utilization: float
    memory_utilization: float
    concurrent_calls: int
    stt_latency_ms: float
    tts_latency_ms: float
    error_rate: float
    timestamp: datetime

@dataclass
class ScalingDecision:
    action: str  # "scale_up", "scale_down", "maintain"
    reason: str
    current_replicas: int
    target_replicas: int
    metrics: ScalingMetrics
    timestamp: datetime

class VoiceAIMetricsCollector:
    """Collects and manages voice AI metrics for scaling decisions"""
    
    def __init__(self):
        self.metrics_history = []
        self.current_metrics = ScalingMetrics(
            cpu_utilization=0.0,
            memory_utilization=0.0,
            concurrent_calls=0,
            stt_latency_ms=0.0,
            tts_latency_ms=0.0,
            error_rate=0.0,
            timestamp=datetime.utcnow()
        )
        self.max_history_size = 1000
    
    def update_metrics(self, metrics: ScalingMetrics):
        """Update current metrics and add to history"""
        self.current_metrics = metrics
        self.metrics_history.append(metrics)
        
        # Keep only recent history
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history.pop(0)
    
    def get_average_metrics(self, minutes: int = 5) -> Optional[ScalingMetrics]:
        """Get average metrics over the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return None
        
        # Calculate averages
        avg_cpu = sum(m.cpu_utilization for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_utilization for m in recent_metrics) / len(recent_metrics)
        avg_concurrent = sum(m.concurrent_calls for m in recent_metrics) / len(recent_metrics)
        avg_stt_latency = sum(m.stt_latency_ms for m in recent_metrics) / len(recent_metrics)
        avg_tts_latency = sum(m.tts_latency_ms for m in recent_metrics) / len(recent_metrics)
        avg_error_rate = sum(m.error_rate for m in recent_metrics) / len(recent_metrics)
        
        return ScalingMetrics(
            cpu_utilization=avg_cpu,
            memory_utilization=avg_memory,
            concurrent_calls=avg_concurrent,
            stt_latency_ms=avg_stt_latency,
            tts_latency_ms=avg_tts_latency,
            error_rate=avg_error_rate,
            timestamp=datetime.utcnow()
        )

class VoiceAIAutoScaler:
    """Auto-scaling controller for voice AI services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.metrics_collector = VoiceAIMetricsCollector()
        self.current_replicas = 2
        self.min_replicas = 2
        self.max_replicas = 20
        self.target_cpu_utilization = 70.0
        self.target_memory_utilization = 80.0
        self.max_concurrent_calls_per_replica = 50
        self.max_latency_ms = 500
        self.max_error_rate = 0.05  # 5%
        
        # Scaling thresholds
        self.scale_up_thresholds = {
            'cpu_utilization': 80.0,
            'memory_utilization': 85.0,
            'concurrent_calls': 45,
            'stt_latency_ms': 400,
            'tts_latency_ms': 400,
            'error_rate': 0.03
        }
        
        self.scale_down_thresholds = {
            'cpu_utilization': 30.0,
            'memory_utilization': 40.0,
            'concurrent_calls': 10,
            'stt_latency_ms': 200,
            'tts_latency_ms': 200,
            'error_rate': 0.01
        }
        
        # Scaling history
        self.scaling_history = []
        self.last_scale_time = datetime.utcnow()
        self.scale_cooldown_minutes = 5
    
    def should_scale_up(self, metrics: ScalingMetrics) -> bool:
        """Determine if scaling up is needed"""
        # Check cooldown period
        if datetime.utcnow() - self.last_scale_time < timedelta(minutes=self.scale_cooldown_minutes):
            return False
        
        # Check if we're already at max replicas
        if self.current_replicas >= self.max_replicas:
            return False
        
        # Check various scaling triggers
        triggers = []
        
        if metrics.cpu_utilization > self.scale_up_thresholds['cpu_utilization']:
            triggers.append(f"CPU utilization {metrics.cpu_utilization:.1f}% > {self.scale_up_thresholds['cpu_utilization']}%")
        
        if metrics.memory_utilization > self.scale_up_thresholds['memory_utilization']:
            triggers.append(f"Memory utilization {metrics.memory_utilization:.1f}% > {self.scale_up_thresholds['memory_utilization']}%")
        
        if metrics.concurrent_calls > self.scale_up_thresholds['concurrent_calls']:
            triggers.append(f"Concurrent calls {metrics.concurrent_calls} > {self.scale_up_thresholds['concurrent_calls']}")
        
        if metrics.stt_latency_ms > self.scale_up_thresholds['stt_latency_ms']:
            triggers.append(f"STT latency {metrics.stt_latency_ms:.1f}ms > {self.scale_up_thresholds['stt_latency_ms']}ms")
        
        if metrics.tts_latency_ms > self.scale_up_thresholds['tts_latency_ms']:
            triggers.append(f"TTS latency {metrics.tts_latency_ms:.1f}ms > {self.scale_up_thresholds['tts_latency_ms']}ms")
        
        if metrics.error_rate > self.scale_up_thresholds['error_rate']:
            triggers.append(f"Error rate {metrics.error_rate:.3f} > {self.scale_up_thresholds['error_rate']:.3f}")
        
        return len(triggers) > 0, triggers
    
    def should_scale_down(self, metrics: ScalingMetrics) -> bool:
        """Determine if scaling down is needed"""
        # Check cooldown period
        if datetime.utcnow() - self.last_scale_time < timedelta(minutes=self.scale_cooldown_minutes):
            return False
        
        # Check if we're already at min replicas
        if self.current_replicas <= self.min_replicas:
            return False
        
        # Check various scaling triggers
        triggers = []
        
        if metrics.cpu_utilization < self.scale_down_thresholds['cpu_utilization']:
            triggers.append(f"CPU utilization {metrics.cpu_utilization:.1f}% < {self.scale_down_thresholds['cpu_utilization']}%")
        
        if metrics.memory_utilization < self.scale_down_thresholds['memory_utilization']:
            triggers.append(f"Memory utilization {metrics.memory_utilization:.1f}% < {self.scale_down_thresholds['memory_utilization']}%")
        
        if metrics.concurrent_calls < self.scale_down_thresholds['concurrent_calls']:
            triggers.append(f"Concurrent calls {metrics.concurrent_calls} < {self.scale_down_thresholds['concurrent_calls']}")
        
        if metrics.stt_latency_ms < self.scale_down_thresholds['stt_latency_ms']:
            triggers.append(f"STT latency {metrics.stt_latency_ms:.1f}ms < {self.scale_down_thresholds['stt_latency_ms']}ms")
        
        if metrics.tts_latency_ms < self.scale_down_thresholds['tts_latency_ms']:
            triggers.append(f"TTS latency {metrics.tts_latency_ms:.1f}ms < {self.scale_down_thresholds['tts_latency_ms']}ms")
        
        if metrics.error_rate < self.scale_down_thresholds['error_rate']:
            triggers.append(f"Error rate {metrics.error_rate:.3f} < {self.scale_down_thresholds['error_rate']:.3f}")
        
        return len(triggers) > 0, triggers
    
    def calculate_target_replicas(self, metrics: ScalingMetrics, action: str) -> int:
        """Calculate target number of replicas based on metrics"""
        if action == "scale_up":
            # Scale up based on the most critical metric
            scale_factors = []
            
            # CPU-based scaling
            if metrics.cpu_utilization > self.target_cpu_utilization:
                cpu_factor = metrics.cpu_utilization / self.target_cpu_utilization
                scale_factors.append(cpu_factor)
            
            # Memory-based scaling
            if metrics.memory_utilization > self.target_memory_utilization:
                memory_factor = metrics.memory_utilization / self.target_memory_utilization
                scale_factors.append(memory_factor)
            
            # Concurrent calls-based scaling
            if metrics.concurrent_calls > self.max_concurrent_calls_per_replica:
                calls_factor = metrics.concurrent_calls / self.max_concurrent_calls_per_replica
                scale_factors.append(calls_factor)
            
            # Latency-based scaling
            if metrics.stt_latency_ms > self.max_latency_ms:
                latency_factor = metrics.stt_latency_ms / self.max_latency_ms
                scale_factors.append(latency_factor)
            
            if scale_factors:
                # Use the highest scaling factor
                max_factor = max(scale_factors)
                target_replicas = math.ceil(self.current_replicas * max_factor)
            else:
                # Conservative scale up
                target_replicas = self.current_replicas + 1
                
        else:  # scale_down
            # Conservative scale down
            target_replicas = max(self.min_replicas, self.current_replicas - 1)
        
        # Ensure within bounds
        target_replicas = max(self.min_replicas, min(self.max_replicas, target_replicas))
        return target_replicas
    
    def evaluate_scaling(self, metrics: ScalingMetrics) -> ScalingDecision:
        """Evaluate if scaling is needed and return decision"""
        self.metrics_collector.update_metrics(metrics)
        
        # Check for scale up
        should_scale_up, up_triggers = self.should_scale_up(metrics)
        if should_scale_up:
            target_replicas = self.calculate_target_replicas(metrics, "scale_up")
            decision = ScalingDecision(
                action="scale_up",
                reason="; ".join(up_triggers),
                current_replicas=self.current_replicas,
                target_replicas=target_replicas,
                metrics=metrics,
                timestamp=datetime.utcnow()
            )
            self.current_replicas = target_replicas
            self.last_scale_time = datetime.utcnow()
            self.scaling_history.append(decision)
            return decision
        
        # Check for scale down
        should_scale_down, down_triggers = self.should_scale_down(metrics)
        if should_scale_down:
            target_replicas = self.calculate_target_replicas(metrics, "scale_down")
            decision = ScalingDecision(
                action="scale_down",
                reason="; ".join(down_triggers),
                current_replicas=self.current_replicas,
                target_replicas=target_replicas,
                metrics=metrics,
                timestamp=datetime.utcnow()
            )
            self.current_replicas = target_replicas
            self.last_scale_time = datetime.utcnow()
            self.scaling_history.append(decision)
            return decision
        
        # No scaling needed
        return ScalingDecision(
            action="maintain",
            reason="All metrics within acceptable ranges",
            current_replicas=self.current_replicas,
            target_replicas=self.current_replicas,
            metrics=metrics,
            timestamp=datetime.utcnow()
        )
    
    def get_scaling_summary(self) -> Dict[str, Any]:
        """Get summary of scaling activity"""
        recent_scaling = [
            s for s in self.scaling_history 
            if s.timestamp >= datetime.utcnow() - timedelta(hours=1)
        ]
        
        return {
            "service_name": self.service_name,
            "current_replicas": self.current_replicas,
            "min_replicas": self.min_replicas,
            "max_replicas": self.max_replicas,
            "scaling_events_last_hour": len(recent_scaling),
            "total_scaling_events": len(self.scaling_history),
            "last_scale_time": self.last_scale_time.isoformat(),
            "current_metrics": asdict(self.metrics_collector.current_metrics)
        }

class KubernetesHPA:
    """Simulates Kubernetes Horizontal Pod Autoscaler configuration"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.hpa_config = self._generate_hpa_config()
    
    def _generate_hpa_config(self) -> Dict[str, Any]:
        """Generate Kubernetes HPA configuration"""
        return {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{self.service_name}-hpa",
                "namespace": "voice-ai"
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": f"{self.service_name}-deployment"
                },
                "minReplicas": 2,
                "maxReplicas": 20,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 70
                            }
                        }
                    },
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 80
                            }
                        }
                    }
                ],
                "behavior": {
                    "scaleUp": {
                        "stabilizationWindowSeconds": 60,
                        "policies": [
                            {
                                "type": "Percent",
                                "value": 100,
                                "periodSeconds": 15
                            }
                        ]
                    },
                    "scaleDown": {
                        "stabilizationWindowSeconds": 300,
                        "policies": [
                            {
                                "type": "Percent",
                                "value": 10,
                                "periodSeconds": 60
                            }
                        ]
                    }
                }
            }
        }
    
    def get_hpa_yaml(self) -> str:
        """Return HPA configuration as YAML"""
        import yaml
        return yaml.dump(self.hpa_config, default_flow_style=False, sort_keys=False)

class CustomMetricsService:
    """Service for exposing custom metrics to Kubernetes"""
    
    def __init__(self):
        self.metrics = {}
        self.metrics_server_url = "http://metrics-server:8080"
    
    def expose_custom_metric(self, metric_name: str, value: float, labels: Dict[str, str]):
        """Expose a custom metric to Kubernetes metrics server"""
        metric = {
            "name": metric_name,
            "value": value,
            "labels": labels,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        self.metrics[metric_name].append(metric)
        
        # Keep only recent metrics
        if len(self.metrics[metric_name]) > 100:
            self.metrics[metric_name] = self.metrics[metric_name][-100:]
    
    def get_custom_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all custom metrics"""
        return self.metrics

async def simulate_autoscaling_demo():
    """Demonstrate auto-scaling configuration"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Example: Auto-scaling Configuration")
    print("=" * 60)
    
    # Initialize auto-scaler
    auto_scaler = VoiceAIAutoScaler("voice-ai-service")
    k8s_hpa = KubernetesHPA("voice-ai-service")
    metrics_service = CustomMetricsService()
    
    print("\n1. Kubernetes HPA Configuration:")
    print(k8s_hpa.get_hpa_yaml())
    
    print("\n2. Auto-scaling Simulation:")
    print("   Simulating 20 minutes of varying load...")
    
    # Simulate varying load over time
    simulation_minutes = 20
    scaling_decisions = []
    
    for minute in range(simulation_minutes):
        # Simulate different load patterns
        if minute < 5:
            # Low load
            load_factor = 0.3
        elif minute < 10:
            # High load
            load_factor = 1.5
        elif minute < 15:
            # Peak load
            load_factor = 2.0
        else:
            # Back to normal
            load_factor = 0.8
        
        # Generate metrics based on load
        metrics = ScalingMetrics(
            cpu_utilization=min(95, 20 + (load_factor * 50)),
            memory_utilization=min(90, 30 + (load_factor * 40)),
            concurrent_calls=int(5 + (load_factor * 40)),
            stt_latency_ms=100 + (load_factor * 300),
            tts_latency_ms=150 + (load_factor * 250),
            error_rate=0.01 + (load_factor * 0.04),
            timestamp=datetime.utcnow() + timedelta(minutes=minute)
        )
        
        # Evaluate scaling
        decision = auto_scaler.evaluate_scaling(metrics)
        scaling_decisions.append(decision)
        
        # Expose custom metrics
        metrics_service.expose_custom_metric(
            "concurrent_calls",
            metrics.concurrent_calls,
            {"service": "voice-ai-service"}
        )
        metrics_service.expose_custom_metric(
            "stt_latency_ms",
            metrics.stt_latency_ms,
            {"service": "voice-ai-service"}
        )
        
        # Print significant events
        if decision.action != "maintain":
            print(f"   Minute {minute}: {decision.action.upper()} - {decision.reason}")
            print(f"     Replicas: {decision.current_replicas} -> {decision.target_replicas}")
    
    print("\n3. Scaling Summary:")
    summary = auto_scaler.get_scaling_summary()
    print(f"   Current Replicas: {summary['current_replicas']}")
    print(f"   Scaling Events (Last Hour): {summary['scaling_events_last_hour']}")
    print(f"   Total Scaling Events: {summary['total_scaling_events']}")
    
    print("\n4. Custom Metrics Exposed:")
    custom_metrics = metrics_service.get_custom_metrics()
    for metric_name, metric_data in custom_metrics.items():
        if metric_data:
            latest_value = metric_data[-1]["value"]
            print(f"   {metric_name}: {latest_value}")
    
    print("\n5. Auto-scaling Benefits:")
    print("   ✓ Automatic response to load changes")
    print("   ✓ Cost optimization during low usage")
    print("   ✓ Performance maintenance during high load")
    print("   ✓ Multiple scaling triggers (CPU, memory, latency, calls)")
    print("   ✓ Cooldown periods prevent thrashing")
    print("   ✓ Custom metrics integration")
    
    return auto_scaler, k8s_hpa, metrics_service

if __name__ == "__main__":
    asyncio.run(simulate_autoscaling_demo())
