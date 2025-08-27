#!/usr/bin/env python3
"""
Performance Monitor - Chapter 6
Real-time performance tracking and KPI calculation for voice AI systems.
"""

import os
import time
import json
import random
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque

class MetricType(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    ACCURACY = "accuracy"
    SATISFACTION = "satisfaction"

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    timestamp: datetime
    metric_type: str
    value: float
    unit: str
    session_id: Optional[str] = None
    call_id: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class KPIThreshold:
    """KPI threshold configuration"""
    metric_name: str
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str

class PerformanceMonitor:
    """Real-time performance monitor for voice AI systems"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics = defaultdict(lambda: deque(maxlen=window_size))
        self.kpi_thresholds = self._initialize_kpi_thresholds()
        self.alerts = []
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Performance counters
        self.call_count = 0
        self.error_count = 0
        self.escalation_count = 0
        self.total_duration = 0.0
        
        # Real-time calculations
        self.current_tts_latency = deque(maxlen=50)
        self.current_stt_latency = deque(maxlen=50)
        self.current_intent_accuracy = deque(maxlen=50)
    
    def _initialize_kpi_thresholds(self) -> Dict[str, KPIThreshold]:
        """Initialize KPI thresholds"""
        return {
            "tts_latency_ms": KPIThreshold(
                metric_name="TTS Latency",
                warning_threshold=500,
                critical_threshold=1000,
                unit="milliseconds",
                description="Text-to-Speech response time"
            ),
            "stt_latency_ms": KPIThreshold(
                metric_name="STT Latency",
                warning_threshold=300,
                critical_threshold=600,
                unit="milliseconds",
                description="Speech-to-Text processing time"
            ),
            "intent_accuracy": KPIThreshold(
                metric_name="Intent Accuracy",
                warning_threshold=0.85,
                critical_threshold=0.75,
                unit="percentage",
                description="Intent recognition accuracy"
            ),
            "error_rate": KPIThreshold(
                metric_name="Error Rate",
                warning_threshold=0.05,
                critical_threshold=0.10,
                unit="percentage",
                description="System error rate"
            ),
            "call_completion_rate": KPIThreshold(
                metric_name="Call Completion Rate",
                warning_threshold=0.85,
                critical_threshold=0.75,
                unit="percentage",
                description="Percentage of calls completed successfully"
            )
        }
    
    def record_metric(self, metric_type: str, value: float, unit: str,
                     session_id: Optional[str] = None, call_id: Optional[str] = None,
                     metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            unit=unit,
            session_id=session_id,
            call_id=call_id,
            metadata=metadata or {}
        )
        
        self.metrics[metric_type].append(metric)
        
        # Check thresholds and generate alerts
        self._check_thresholds(metric)
        
        # Update real-time calculations
        self._update_real_time_metrics(metric)
    
    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds thresholds"""
        if metric.metric_type in self.kpi_thresholds:
            threshold = self.kpi_thresholds[metric.metric_type]
            
            if metric.value >= threshold.critical_threshold:
                self._generate_alert("CRITICAL", metric, threshold)
            elif metric.value >= threshold.warning_threshold:
                self._generate_alert("WARNING", metric, threshold)
    
    def _generate_alert(self, severity: str, metric: PerformanceMetric, threshold: KPIThreshold):
        """Generate performance alert"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "metric_name": threshold.metric_name,
            "current_value": metric.value,
            "threshold": threshold.critical_threshold if severity == "CRITICAL" else threshold.warning_threshold,
            "unit": threshold.unit,
            "description": threshold.description,
            "session_id": metric.session_id,
            "call_id": metric.call_id
        }
        
        self.alerts.append(alert)
        print(f"ALERT [{severity}]: {threshold.metric_name} = {metric.value} {threshold.unit} "
              f"(threshold: {alert['threshold']} {threshold.unit})")
    
    def _update_real_time_metrics(self, metric: PerformanceMetric):
        """Update real-time metric calculations"""
        if metric.metric_type == "tts_latency_ms":
            self.current_tts_latency.append(metric.value)
        elif metric.metric_type == "stt_latency_ms":
            self.current_stt_latency.append(metric.value)
        elif metric.metric_type == "intent_accuracy":
            self.current_intent_accuracy.append(metric.value)
    
    def record_call_event(self, event_type: str, duration: Optional[float] = None):
        """Record call-related events"""
        if event_type == "call_start":
            self.call_count += 1
        elif event_type == "call_end":
            if duration:
                self.total_duration += duration
        elif event_type == "error":
            self.error_count += 1
        elif event_type == "escalation":
            self.escalation_count += 1
    
    def get_current_kpis(self) -> Dict[str, Any]:
        """Get current KPI values"""
        kpis = {}
        
        # Calculate averages for recent metrics
        for metric_type, metrics in self.metrics.items():
            if metrics:
                recent_values = [m.value for m in list(metrics)[-10:]]  # Last 10 values
                kpis[f"{metric_type}_avg"] = sum(recent_values) / len(recent_values)
                kpis[f"{metric_type}_min"] = min(recent_values)
                kpis[f"{metric_type}_max"] = max(recent_values)
        
        # Calculate business KPIs
        if self.call_count > 0:
            kpis["error_rate"] = (self.error_count / self.call_count) * 100
            kpis["escalation_rate"] = (self.escalation_count / self.call_count) * 100
            kpis["completion_rate"] = ((self.call_count - self.error_count - self.escalation_count) / self.call_count) * 100
            kpis["average_call_duration"] = self.total_duration / self.call_count if self.call_count > 0 else 0
        
        # Real-time metrics
        if self.current_tts_latency:
            kpis["current_tts_latency"] = sum(self.current_tts_latency) / len(self.current_tts_latency)
        if self.current_stt_latency:
            kpis["current_stt_latency"] = sum(self.current_stt_latency) / len(self.current_stt_latency)
        if self.current_intent_accuracy:
            kpis["current_intent_accuracy"] = sum(self.current_intent_accuracy) / len(self.current_intent_accuracy)
        
        return kpis
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        kpis = self.get_current_kpis()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "call_statistics": {
                "total_calls": self.call_count,
                "error_count": self.error_count,
                "escalation_count": self.escalation_count,
                "error_rate": kpis.get("error_rate", 0),
                "escalation_rate": kpis.get("escalation_rate", 0),
                "completion_rate": kpis.get("completion_rate", 0),
                "average_duration": kpis.get("average_call_duration", 0)
            },
            "performance_metrics": {
                "tts_latency_ms": {
                    "current": kpis.get("current_tts_latency", 0),
                    "average": kpis.get("tts_latency_ms_avg", 0),
                    "min": kpis.get("tts_latency_ms_min", 0),
                    "max": kpis.get("tts_latency_ms_max", 0)
                },
                "stt_latency_ms": {
                    "current": kpis.get("current_stt_latency", 0),
                    "average": kpis.get("stt_latency_ms_avg", 0),
                    "min": kpis.get("stt_latency_ms_min", 0),
                    "max": kpis.get("stt_latency_ms_max", 0)
                },
                "intent_accuracy": {
                    "current": kpis.get("current_intent_accuracy", 0),
                    "average": kpis.get("intent_accuracy_avg", 0),
                    "min": kpis.get("intent_accuracy_min", 0),
                    "max": kpis.get("intent_accuracy_max", 0)
                }
            },
            "alerts": {
                "total_alerts": len(self.alerts),
                "critical_alerts": len([a for a in self.alerts if a["severity"] == "CRITICAL"]),
                "warning_alerts": len([a for a in self.alerts if a["severity"] == "WARNING"]),
                "recent_alerts": self.alerts[-5:] if self.alerts else []
            }
        }
        
        return summary
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("Performance monitoring started...")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("Performance monitoring stopped.")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Generate summary every 30 seconds
                summary = self.get_performance_summary()
                
                # Print status
                print(f"\n--- Performance Summary ({datetime.now().strftime('%H:%M:%S')}) ---")
                print(f"Calls: {summary['call_statistics']['total_calls']} | "
                      f"Errors: {summary['call_statistics']['error_rate']:.1f}% | "
                      f"Escalations: {summary['call_statistics']['escalation_rate']:.1f}%")
                print(f"TTS Latency: {summary['performance_metrics']['tts_latency_ms']['current']:.0f}ms | "
                      f"STT Latency: {summary['performance_metrics']['stt_latency_ms']['current']:.0f}ms | "
                      f"Intent Accuracy: {summary['performance_metrics']['intent_accuracy']['current']:.1%}")
                print(f"Alerts: {summary['alerts']['total_alerts']} total "
                      f"({summary['alerts']['critical_alerts']} critical, {summary['alerts']['warning_alerts']} warnings)")
                
                time.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)

def simulate_voice_system_performance():
    """Simulate voice system performance monitoring"""
    print("Performance Monitor - Chapter 6")
    print("="*80)
    print("Demonstrating real-time performance tracking...")
    
    # Create performance monitor
    monitor = PerformanceMonitor()
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Simulate voice system activity
    print("\nSimulating voice system activity...")
    
    for i in range(20):  # Simulate 20 calls
        session_id = f"session_{i+1}"
        call_id = f"call_{i+1}"
        
        # Simulate call start
        monitor.record_call_event("call_start")
        
        # Simulate TTS latency (with some variation)
        tts_latency = random.normalvariate(200, 50)  # Mean 200ms, std 50ms
        monitor.record_metric("tts_latency_ms", tts_latency, "milliseconds", session_id, call_id)
        
        # Simulate STT latency
        stt_latency = random.normalvariate(150, 30)  # Mean 150ms, std 30ms
        monitor.record_metric("stt_latency_ms", stt_latency, "milliseconds", session_id, call_id)
        
        # Simulate intent accuracy
        intent_accuracy = random.uniform(0.75, 0.98)  # 75% to 98%
        monitor.record_metric("intent_accuracy", intent_accuracy, "percentage", session_id, call_id)
        
        # Simulate call duration
        call_duration = random.uniform(30, 120)  # 30 to 120 seconds
        
        # Simulate some errors and escalations
        if random.random() < 0.1:  # 10% error rate
            monitor.record_call_event("error")
        elif random.random() < 0.15:  # 15% escalation rate
            monitor.record_call_event("escalation")
        
        # Simulate call end
        monitor.record_call_event("call_end", call_duration)
        
        # Add some delay between calls
        time.sleep(2)
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Get final summary
    final_summary = monitor.get_performance_summary()
    
    print(f"\n{'='*80}")
    print("FINAL PERFORMANCE SUMMARY")
    print(f"{'='*80}")
    
    print(f"\nCall Statistics:")
    stats = final_summary["call_statistics"]
    print(f"  Total Calls: {stats['total_calls']}")
    print(f"  Error Rate: {stats['error_rate']:.1f}%")
    print(f"  Escalation Rate: {stats['escalation_rate']:.1f}%")
    print(f"  Completion Rate: {stats['completion_rate']:.1f}%")
    print(f"  Average Duration: {stats['average_duration']:.1f} seconds")
    
    print(f"\nPerformance Metrics:")
    perf = final_summary["performance_metrics"]
    print(f"  TTS Latency: {perf['tts_latency_ms']['current']:.0f}ms (avg: {perf['tts_latency_ms']['average']:.0f}ms)")
    print(f"  STT Latency: {perf['stt_latency_ms']['current']:.0f}ms (avg: {perf['stt_latency_ms']['average']:.0f}ms)")
    print(f"  Intent Accuracy: {perf['intent_accuracy']['current']:.1%} (avg: {perf['intent_accuracy']['average']:.1%})")
    
    print(f"\nAlert Summary:")
    alerts = final_summary["alerts"]
    print(f"  Total Alerts: {alerts['total_alerts']}")
    print(f"  Critical Alerts: {alerts['critical_alerts']}")
    print(f"  Warning Alerts: {alerts['warning_alerts']}")
    
    if alerts['recent_alerts']:
        print(f"\nRecent Alerts:")
        for alert in alerts['recent_alerts']:
            print(f"  [{alert['severity']}] {alert['metric_name']}: {alert['current_value']} {alert['unit']}")
    
    print(f"\nPerformance monitoring demo completed!")
    print("   This demonstrates real-time KPI tracking for voice AI systems.")

if __name__ == "__main__":
    simulate_voice_system_performance()
