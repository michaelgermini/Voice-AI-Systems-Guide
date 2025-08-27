#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Example: Observability at Scale

This example demonstrates observability patterns for voice AI services,
including distributed tracing, centralized logging, and monitoring.
"""

import time
import json
import uuid
import asyncio
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import math

@dataclass
class TraceSpan:
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    service_name: str
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime]
    duration_ms: Optional[float]
    tags: Dict[str, Any]
    logs: List[Dict[str, Any]]

@dataclass
class LogEntry:
    timestamp: datetime
    level: str  # DEBUG, INFO, WARN, ERROR, CRITICAL
    service_name: str
    trace_id: Optional[str]
    span_id: Optional[str]
    message: str
    fields: Dict[str, Any]

@dataclass
class Metric:
    name: str
    value: float
    unit: str
    timestamp: datetime
    labels: Dict[str, str]
    service_name: str

class DistributedTracer:
    """Distributed tracing implementation for voice AI services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans = []
        self.active_spans = {}
        self.trace_sampler = 1.0  # 100% sampling for demo
    
    def start_span(self, operation_name: str, trace_id: Optional[str] = None, 
                  parent_span_id: Optional[str] = None, tags: Optional[Dict[str, Any]] = None) -> str:
        """Start a new span"""
        if random.random() > self.trace_sampler:
            return None
        
        span_id = f"span-{uuid.uuid4().hex[:8]}"
        if not trace_id:
            trace_id = f"trace-{uuid.uuid4().hex[:8]}"
        
        span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            service_name=self.service_name,
            operation_name=operation_name,
            start_time=datetime.utcnow(),
            end_time=None,
            duration_ms=None,
            tags=tags or {},
            logs=[]
        )
        
        self.spans.append(span)
        self.active_spans[span_id] = span
        
        return span_id
    
    def end_span(self, span_id: str, tags: Optional[Dict[str, Any]] = None):
        """End a span"""
        if span_id not in self.active_spans:
            return
        
        span = self.active_spans[span_id]
        span.end_time = datetime.utcnow()
        span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
        
        if tags:
            span.tags.update(tags)
        
        del self.active_spans[span_id]
    
    def add_span_log(self, span_id: str, message: str, fields: Optional[Dict[str, Any]] = None):
        """Add a log entry to a span"""
        if span_id not in self.active_spans:
            return
        
        span = self.active_spans[span_id]
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "fields": fields or {}
        }
        span.logs.append(log_entry)
    
    def add_span_tag(self, span_id: str, key: str, value: Any):
        """Add a tag to a span"""
        if span_id not in self.active_spans:
            return
        
        span = self.active_spans[span_id]
        span.tags[key] = value
    
    def get_trace(self, trace_id: str) -> List[TraceSpan]:
        """Get all spans for a trace"""
        return [span for span in self.spans if span.trace_id == trace_id]
    
    def get_service_spans(self, service_name: str) -> List[TraceSpan]:
        """Get all spans for a service"""
        return [span for span in self.spans if span.service_name == service_name]
    
    def get_trace_metrics(self) -> Dict[str, Any]:
        """Get tracing metrics"""
        if not self.spans:
            return {}
        
        durations = [span.duration_ms for span in self.spans if span.duration_ms is not None]
        
        return {
            "total_spans": len(self.spans),
            "active_spans": len(self.active_spans),
            "total_traces": len(set(span.trace_id for span in self.spans)),
            "avg_span_duration_ms": sum(durations) / len(durations) if durations else 0,
            "max_span_duration_ms": max(durations) if durations else 0,
            "min_span_duration_ms": min(durations) if durations else 0
        }

class CentralizedLogger:
    """Centralized logging for voice AI services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logs = []
        self.log_levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
        self.current_level = "INFO"
    
    def log(self, level: str, message: str, trace_id: Optional[str] = None, 
            span_id: Optional[str] = None, fields: Optional[Dict[str, Any]] = None):
        """Log a message"""
        if self.log_levels.index(level) < self.log_levels.index(self.current_level):
            return
        
        log_entry = LogEntry(
            timestamp=datetime.utcnow(),
            level=level,
            service_name=self.service_name,
            trace_id=trace_id,
            span_id=span_id,
            message=message,
            fields=fields or {}
        )
        
        self.logs.append(log_entry)
        
        # In real implementation, this would send to centralized logging system
        # like ELK stack, Fluentd, or cloud logging service
    
    def debug(self, message: str, **kwargs):
        self.log("DEBUG", message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self.log("INFO", message, **kwargs)
    
    def warn(self, message: str, **kwargs):
        self.log("WARN", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log("ERROR", message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self.log("CRITICAL", message, **kwargs)
    
    def search_logs(self, filters: Dict[str, Any]) -> List[LogEntry]:
        """Search logs with filters"""
        filtered_logs = self.logs
        
        if "level" in filters:
            filtered_logs = [log for log in filtered_logs if log.level == filters["level"]]
        
        if "trace_id" in filters:
            filtered_logs = [log for log in filtered_logs if log.trace_id == filters["trace_id"]]
        
        if "service_name" in filters:
            filtered_logs = [log for log in filtered_logs if log.service_name == filters["service_name"]]
        
        if "start_time" in filters:
            filtered_logs = [log for log in filtered_logs if log.timestamp >= filters["start_time"]]
        
        if "end_time" in filters:
            filtered_logs = [log for log in filtered_logs if log.timestamp <= filters["end_time"]]
        
        return filtered_logs
    
    def get_log_metrics(self) -> Dict[str, Any]:
        """Get logging metrics"""
        if not self.logs:
            return {}
        
        level_counts = {}
        for level in self.log_levels:
            level_counts[level] = len([log for log in self.logs if log.level == level])
        
        return {
            "total_logs": len(self.logs),
            "logs_by_level": level_counts,
            "logs_with_trace": len([log for log in self.logs if log.trace_id]),
            "logs_with_span": len([log for log in self.logs if log.span_id])
        }

class MetricsCollector:
    """Metrics collection for voice AI services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.metrics = []
        self.metric_types = ["counter", "gauge", "histogram", "summary"]
    
    def record_metric(self, name: str, value: float, unit: str, 
                     metric_type: str = "gauge", labels: Optional[Dict[str, str]] = None):
        """Record a metric"""
        metric = Metric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.utcnow(),
            labels=labels or {},
            service_name=self.service_name
        )
        
        self.metrics.append(metric)
    
    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        self.record_metric(name, 1.0, "count", "counter", labels)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric"""
        self.record_metric(name, value, "value", "gauge", labels)
    
    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a histogram metric"""
        self.record_metric(name, value, "value", "histogram", labels)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        if not self.metrics:
            return {}
        
        # Group metrics by name
        metrics_by_name = {}
        for metric in self.metrics:
            if metric.name not in metrics_by_name:
                metrics_by_name[metric.name] = []
            metrics_by_name[metric.name].append(metric)
        
        summary = {}
        for name, metric_list in metrics_by_name.items():
            values = [m.value for m in metric_list]
            summary[name] = {
                "count": len(values),
                "sum": sum(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "unit": metric_list[0].unit,
                "type": "counter" if name.endswith("_total") else "gauge"
            }
        
        return summary

class VoiceAIObservability:
    """Comprehensive observability for voice AI services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.tracer = DistributedTracer(service_name)
        self.logger = CentralizedLogger(service_name)
        self.metrics = MetricsCollector(service_name)
    
    async def trace_call_processing(self, call_id: str, user_id: str):
        """Trace a complete call processing flow"""
        trace_id = f"trace-{uuid.uuid4().hex[:8]}"
        
        # Start root span
        root_span_id = self.tracer.start_span(
            "process_call",
            trace_id=trace_id,
            tags={"call_id": call_id, "user_id": user_id}
        )
        
        self.logger.info("Starting call processing", trace_id=trace_id, span_id=root_span_id,
                        fields={"call_id": call_id, "user_id": user_id})
        
        try:
            # Simulate STT processing
            stt_span_id = self.tracer.start_span(
                "stt_processing",
                trace_id=trace_id,
                parent_span_id=root_span_id,
                tags={"call_id": call_id}
            )
            
            self.logger.debug("Starting STT processing", trace_id=trace_id, span_id=stt_span_id)
            
            # Simulate processing time
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Record STT metrics
            stt_latency = random.uniform(100, 300)
            self.metrics.record_histogram("stt_latency_ms", stt_latency, {"call_id": call_id})
            self.metrics.increment_counter("stt_requests_total", {"call_id": call_id})
            
            self.tracer.add_span_tag(stt_span_id, "stt_latency_ms", stt_latency)
            self.tracer.add_span_log(stt_span_id, "STT processing completed", {"latency_ms": stt_latency})
            
            self.tracer.end_span(stt_span_id)
            
            # Simulate NLP processing
            nlp_span_id = self.tracer.start_span(
                "nlp_processing",
                trace_id=trace_id,
                parent_span_id=root_span_id,
                tags={"call_id": call_id}
            )
            
            self.logger.debug("Starting NLP processing", trace_id=trace_id, span_id=nlp_span_id)
            
            await asyncio.sleep(random.uniform(0.05, 0.15))
            
            # Record NLP metrics
            nlp_latency = random.uniform(20, 100)
            self.metrics.record_histogram("nlp_latency_ms", nlp_latency, {"call_id": call_id})
            self.metrics.increment_counter("nlp_requests_total", {"call_id": call_id})
            
            self.tracer.add_span_tag(nlp_span_id, "nlp_latency_ms", nlp_latency)
            self.tracer.add_span_log(nlp_span_id, "NLP processing completed", {"latency_ms": nlp_latency})
            
            self.tracer.end_span(nlp_span_id)
            
            # Simulate TTS processing
            tts_span_id = self.tracer.start_span(
                "tts_processing",
                trace_id=trace_id,
                parent_span_id=root_span_id,
                tags={"call_id": call_id}
            )
            
            self.logger.debug("Starting TTS processing", trace_id=trace_id, span_id=tts_span_id)
            
            await asyncio.sleep(random.uniform(0.2, 0.4))
            
            # Record TTS metrics
            tts_latency = random.uniform(150, 400)
            self.metrics.record_histogram("tts_latency_ms", tts_latency, {"call_id": call_id})
            self.metrics.increment_counter("tts_requests_total", {"call_id": call_id})
            
            self.tracer.add_span_tag(tts_span_id, "tts_latency_ms", tts_latency)
            self.tracer.add_span_log(tts_span_id, "TTS processing completed", {"latency_ms": tts_latency})
            
            self.tracer.end_span(tts_span_id)
            
            # Record overall metrics
            total_latency = stt_latency + nlp_latency + tts_latency
            self.metrics.record_histogram("total_call_latency_ms", total_latency, {"call_id": call_id})
            self.metrics.increment_counter("calls_processed_total", {"call_id": call_id})
            
            self.logger.info("Call processing completed successfully", trace_id=trace_id, span_id=root_span_id,
                           fields={"total_latency_ms": total_latency})
            
            self.tracer.end_span(root_span_id, {"total_latency_ms": total_latency})
            
        except Exception as e:
            self.logger.error("Call processing failed", trace_id=trace_id, span_id=root_span_id,
                            fields={"error": str(e)})
            self.metrics.increment_counter("calls_failed_total", {"call_id": call_id, "error": str(e)})
            self.tracer.end_span(root_span_id, {"error": str(e)})
            raise
    
    def get_observability_summary(self) -> Dict[str, Any]:
        """Get comprehensive observability summary"""
        trace_metrics = self.tracer.get_trace_metrics()
        log_metrics = self.logger.get_log_metrics()
        metrics_summary = self.metrics.get_metrics_summary()
        
        return {
            "service_name": self.service_name,
            "timestamp": datetime.utcnow().isoformat(),
            "tracing": trace_metrics,
            "logging": log_metrics,
            "metrics": metrics_summary
        }

async def simulate_observability_demo():
    """Demonstrate observability capabilities"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Example: Observability at Scale")
    print("=" * 60)
    
    # Initialize observability for multiple services
    services = {
        "voice-ai-gateway": VoiceAIObservability("voice-ai-gateway"),
        "stt-service": VoiceAIObservability("stt-service"),
        "nlp-service": VoiceAIObservability("nlp-service"),
        "tts-service": VoiceAIObservability("tts-service")
    }
    
    print("\n1. Observability Components:")
    print("   - Distributed Tracing: Track request flow across services")
    print("   - Centralized Logging: Structured logs with correlation IDs")
    print("   - Metrics Collection: Performance and business metrics")
    print("   - Service Discovery: Automatic service identification")
    
    print("\n2. Tracing Simulation:")
    print("   Processing 20 calls with distributed tracing...")
    
    # Simulate call processing with observability
    call_results = []
    for i in range(20):
        call_id = f"call-{uuid.uuid4().hex[:8]}"
        user_id = f"user-{random.randint(1, 100)}"
        
        try:
            await services["voice-ai-gateway"].trace_call_processing(call_id, user_id)
            call_results.append((call_id, "success"))
        except Exception as e:
            call_results.append((call_id, f"failed: {str(e)}"))
    
    print(f"   Processed {len([r for r in call_results if r[1] == 'success'])} calls successfully")
    
    print("\n3. Observability Summary:")
    
    # Collect observability data from all services
    all_summaries = {}
    for service_name, service in services.items():
        summary = service.get_observability_summary()
        all_summaries[service_name] = summary
        
        print(f"\n   {service_name}:")
        print(f"     Traces: {summary['tracing'].get('total_traces', 0)}")
        print(f"     Spans: {summary['tracing'].get('total_spans', 0)}")
        print(f"     Logs: {summary['logging'].get('total_logs', 0)}")
        print(f"     Metrics: {len(summary['metrics'])}")
    
    print("\n4. Distributed Tracing Analysis:")
    
    # Analyze traces across services
    all_traces = set()
    all_spans = []
    
    for service_name, service in services.items():
        service_traces = service.tracer.spans
        all_spans.extend(service_traces)
        all_traces.update(span.trace_id for span in service_traces)
    
    print(f"   Total Unique Traces: {len(all_traces)}")
    print(f"   Total Spans: {len(all_spans)}")
    
    # Calculate average trace depth
    trace_depths = {}
    for span in all_spans:
        if span.trace_id not in trace_depths:
            trace_depths[span.trace_id] = 0
        trace_depths[span.trace_id] += 1
    
    avg_depth = sum(trace_depths.values()) / len(trace_depths) if trace_depths else 0
    print(f"   Average Spans per Trace: {avg_depth:.1f}")
    
    print("\n5. Performance Metrics:")
    
    # Aggregate metrics across services
    all_metrics = {}
    for service_name, service in services.items():
        service_metrics = service.metrics.get_metrics_summary()
        for metric_name, metric_data in service_metrics.items():
            if metric_name not in all_metrics:
                all_metrics[metric_name] = {"services": {}}
            all_metrics[metric_name]["services"][service_name] = metric_data
    
    # Display key metrics
    key_metrics = ["stt_latency_ms", "nlp_latency_ms", "tts_latency_ms", "total_call_latency_ms"]
    for metric_name in key_metrics:
        if metric_name in all_metrics:
            print(f"   {metric_name}:")
            for service_name, metric_data in all_metrics[metric_name]["services"].items():
                print(f"     {service_name}: {metric_data['avg']:.1f}ms avg")
    
    print("\n6. Log Analysis:")
    
    # Search for error logs
    error_logs = []
    for service_name, service in services.items():
        service_errors = service.logger.search_logs({"level": "ERROR"})
        error_logs.extend(service_errors)
    
    print(f"   Total Error Logs: {len(error_logs)}")
    if error_logs:
        print("   Recent Errors:")
        for log in error_logs[-3:]:  # Show last 3 errors
            print(f"     {log.timestamp}: {log.service_name} - {log.message}")
    
    print("\n7. Observability Benefits:")
    print("   ✓ End-to-end request tracing across services")
    print("   ✓ Performance bottleneck identification")
    print("   ✓ Error correlation and debugging")
    print("   ✓ Service dependency mapping")
    print("   ✓ Real-time monitoring and alerting")
    print("   ✓ Capacity planning and optimization")
    print("   ✓ SLA monitoring and compliance")
    
    return services, all_summaries

if __name__ == "__main__":
    asyncio.run(simulate_observability_demo())
