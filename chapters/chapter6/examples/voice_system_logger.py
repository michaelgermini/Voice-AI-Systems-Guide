#!/usr/bin/env python3
"""
Voice System Logger - Chapter 6
Structured logging implementation for voice AI systems with JSON formatting.
"""

import os
import time
import json
import uuid
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class EventType(Enum):
    CALL_START = "call_start"
    CALL_END = "call_end"
    USER_INPUT = "user_input"
    TTS_GENERATED = "tts_generated"
    INTENT_DETECTED = "intent_detected"
    STATE_TRANSITION = "state_transition"
    ERROR_OCCURRED = "error_occurred"
    PERFORMANCE_METRIC = "performance_metric"
    ESCALATION = "escalation"
    SESSION_TIMEOUT = "session_timeout"

@dataclass
class LogEntry:
    """Structured log entry for voice AI systems"""
    timestamp: str
    service_name: str
    event_type: str
    session_id: str
    call_id: Optional[str]
    user_id: Optional[str]
    phone_number: Optional[str]
    level: str
    message: str
    metadata: Dict[str, Any]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None

class VoiceSystemLogger:
    """Structured logger for voice AI systems"""
    
    def __init__(self, service_name: str, log_file: Optional[str] = None):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        
        # Configure logging
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler (optional)
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.INFO)
                self.logger.addHandler(file_handler)
            
            self.logger.addHandler(console_handler)
    
    def _generate_trace_id(self) -> str:
        """Generate a unique trace ID"""
        return str(uuid.uuid4())
    
    def _create_log_entry(self, event_type: EventType, session_id: str, 
                         level: LogLevel, message: str, metadata: Dict[str, Any],
                         call_id: Optional[str] = None, user_id: Optional[str] = None,
                         phone_number: Optional[str] = None, trace_id: Optional[str] = None) -> LogEntry:
        """Create a structured log entry"""
        return LogEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            service_name=self.service_name,
            event_type=event_type.value,
            session_id=session_id,
            call_id=call_id,
            user_id=user_id,
            phone_number=phone_number,
            level=level.value,
            message=message,
            metadata=metadata,
            trace_id=trace_id or self._generate_trace_id()
        )
    
    def _log_entry(self, log_entry: LogEntry):
        """Log a structured entry"""
        log_data = asdict(log_entry)
        self.logger.info(json.dumps(log_data))
    
    def log_call_start(self, session_id: str, call_id: str, phone_number: str, 
                      user_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log call start event"""
        log_entry = self._create_log_entry(
            event_type=EventType.CALL_START,
            session_id=session_id,
            level=LogLevel.INFO,
            message="Call started",
            metadata=metadata or {},
            call_id=call_id,
            user_id=user_id,
            phone_number=phone_number
        )
        self._log_entry(log_entry)
    
    def log_call_end(self, session_id: str, call_id: str, duration_seconds: float,
                    resolution_status: str, metadata: Dict[str, Any] = None):
        """Log call end event"""
        metadata = metadata or {}
        metadata.update({
            "duration_seconds": duration_seconds,
            "resolution_status": resolution_status
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.CALL_END,
            session_id=session_id,
            level=LogLevel.INFO,
            message="Call ended",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_user_input(self, session_id: str, user_input: str, confidence: float,
                      call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log user input event"""
        metadata = metadata or {}
        metadata.update({
            "user_input": user_input,
            "confidence": confidence
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.USER_INPUT,
            session_id=session_id,
            level=LogLevel.INFO,
            message="User input received",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_tts_generated(self, session_id: str, text: str, latency_ms: float,
                         voice_id: str, call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log TTS generation event"""
        metadata = metadata or {}
        metadata.update({
            "text": text,
            "latency_ms": latency_ms,
            "voice_id": voice_id
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.TTS_GENERATED,
            session_id=session_id,
            level=LogLevel.INFO,
            message="TTS response generated",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_intent_detected(self, session_id: str, intent: str, confidence: float,
                           entities: List[Dict], call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log intent detection event"""
        metadata = metadata or {}
        metadata.update({
            "intent": intent,
            "confidence": confidence,
            "entities": entities
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.INTENT_DETECTED,
            session_id=session_id,
            level=LogLevel.INFO,
            message="Intent detected",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_state_transition(self, session_id: str, from_state: str, to_state: str,
                           trigger: str, call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log state transition event"""
        metadata = metadata or {}
        metadata.update({
            "from_state": from_state,
            "to_state": to_state,
            "trigger": trigger
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.STATE_TRANSITION,
            session_id=session_id,
            level=LogLevel.INFO,
            message="State transition",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_error(self, session_id: str, error_type: str, error_message: str,
                 stack_trace: Optional[str] = None, call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log error event"""
        metadata = metadata or {}
        metadata.update({
            "error_type": error_type,
            "error_message": error_message
        })
        
        if stack_trace:
            metadata["stack_trace"] = stack_trace
        
        log_entry = self._create_log_entry(
            event_type=EventType.ERROR_OCCURRED,
            session_id=session_id,
            level=LogLevel.ERROR,
            message="Error occurred",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_performance_metric(self, session_id: str, metric_name: str, value: float,
                             unit: str, call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log performance metric"""
        metadata = metadata or {}
        metadata.update({
            "metric_name": metric_name,
            "value": value,
            "unit": unit
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.PERFORMANCE_METRIC,
            session_id=session_id,
            level=LogLevel.INFO,
            message="Performance metric recorded",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_escalation(self, session_id: str, escalation_reason: str, agent_id: Optional[str] = None,
                      call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log escalation event"""
        metadata = metadata or {}
        metadata.update({
            "escalation_reason": escalation_reason,
            "agent_id": agent_id
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.ESCALATION,
            session_id=session_id,
            level=LogLevel.WARN,
            message="Call escalated to human agent",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)
    
    def log_session_timeout(self, session_id: str, timeout_duration: float,
                           call_id: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Log session timeout event"""
        metadata = metadata or {}
        metadata.update({
            "timeout_duration": timeout_duration
        })
        
        log_entry = self._create_log_entry(
            event_type=EventType.SESSION_TIMEOUT,
            session_id=session_id,
            level=LogLevel.WARN,
            message="Session timed out",
            metadata=metadata,
            call_id=call_id
        )
        self._log_entry(log_entry)

class VoiceSystemMonitor:
    """Monitor for analyzing voice system logs"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []
    
    def load_logs(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
        """Load logs from file with optional time filtering"""
        self.logs = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.strip())
                    
                    # Time filtering
                    if start_time or end_time:
                        log_timestamp = datetime.fromisoformat(log_entry["timestamp"].replace("Z", "+00:00"))
                        
                        if start_time and log_timestamp < start_time:
                            continue
                        if end_time and log_timestamp > end_time:
                            continue
                    
                    self.logs.append(log_entry)
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON lines
    
    def get_call_statistics(self) -> Dict[str, Any]:
        """Calculate call statistics from logs"""
        call_starts = [log for log in self.logs if log["event_type"] == "call_start"]
        call_ends = [log for log in self.logs if log["event_type"] == "call_end"]
        errors = [log for log in self.logs if log["event_type"] == "error_occurred"]
        escalations = [log for log in self.logs if log["event_type"] == "escalation"]
        
        total_calls = len(call_starts)
        completed_calls = len(call_ends)
        error_count = len(errors)
        escalation_count = len(escalations)
        
        # Calculate average call duration
        durations = []
        for call_end in call_ends:
            if "duration_seconds" in call_end["metadata"]:
                durations.append(call_end["metadata"]["duration_seconds"])
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "completion_rate": (completed_calls / total_calls * 100) if total_calls > 0 else 0,
            "error_count": error_count,
            "error_rate": (error_count / total_calls * 100) if total_calls > 0 else 0,
            "escalation_count": escalation_count,
            "escalation_rate": (escalation_count / total_calls * 100) if total_calls > 0 else 0,
            "average_duration_seconds": avg_duration
        }
    
    def get_performance_metrics(self) -> Dict[str, List[float]]:
        """Extract performance metrics from logs"""
        performance_logs = [log for log in self.logs if log["event_type"] == "performance_metric"]
        
        metrics = {}
        for log in performance_logs:
            metric_name = log["metadata"]["metric_name"]
            value = log["metadata"]["value"]
            
            if metric_name not in metrics:
                metrics[metric_name] = []
            
            metrics[metric_name].append(value)
        
        return metrics
    
    def get_error_analysis(self) -> Dict[str, int]:
        """Analyze error patterns"""
        error_logs = [log for log in self.logs if log["event_type"] == "error_occurred"]
        
        error_counts = {}
        for log in error_logs:
            error_type = log["metadata"]["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return error_counts

def simulate_voice_system_logging():
    """Simulate voice system logging for demonstration"""
    print("Voice System Logger - Chapter 6")
    print("="*80)
    print("Demonstrating structured logging for voice AI systems...")
    
    # Create logger
    logger = VoiceSystemLogger("voice_ai_service", "voice_system.log")
    
    # Simulate a complete call flow
    session_id = str(uuid.uuid4())
    call_id = f"CA{str(uuid.uuid4())[:16]}"
    phone_number = "+15551234567"
    user_id = "user_12345"
    
    print(f"\nSimulating call flow for session: {session_id}")
    print(f"Call ID: {call_id}")
    print(f"Phone: {phone_number}")
    
    # Call start
    logger.log_call_start(session_id, call_id, phone_number, user_id, {
        "source": "twilio",
        "language": "en-US"
    })
    
    # User input
    logger.log_user_input(session_id, "I want to check my balance", 0.92, call_id, {
        "input_type": "speech",
        "noise_level": "low"
    })
    
    # Intent detection
    logger.log_intent_detected(session_id, "CheckBalance", 0.89, [
        {"entity": "account_type", "value": "checking", "confidence": 0.85}
    ], call_id)
    
    # State transition
    logger.log_state_transition(session_id, "greeting", "collecting_account", "intent_detected", call_id)
    
    # TTS generation
    logger.log_tts_generated(session_id, "Please provide your account number", 180, "Polly.Joanna", call_id, {
        "ssml_used": True,
        "text_length": 28
    })
    
    # Performance metric
    logger.log_performance_metric(session_id, "tts_latency_ms", 180, "milliseconds", call_id)
    logger.log_performance_metric(session_id, "intent_detection_latency_ms", 45, "milliseconds", call_id)
    
    # User input (account number)
    logger.log_user_input(session_id, "12345678", 0.95, call_id, {
        "input_type": "speech",
        "noise_level": "low"
    })
    
    # Error (simulated)
    logger.log_error(session_id, "AccountNotFound", "Account number not found in database", 
                    call_id=call_id, metadata={
                        "account_number": "12345678",
                        "retry_count": 0
                    })
    
    # Escalation
    logger.log_escalation(session_id, "Account not found", "agent_456", call_id, {
        "escalation_type": "account_issue"
    })
    
    # Call end
    logger.log_call_end(session_id, call_id, 45.2, "escalated", {
        "final_state": "escalated",
        "total_turns": 4
    })
    
    print(f"\nCall flow simulation completed!")
    print(f"Log file created: voice_system.log")
    
    # Analyze logs
    print(f"\nAnalyzing logs...")
    monitor = VoiceSystemMonitor("voice_system.log")
    monitor.load_logs()
    
    # Get statistics
    stats = monitor.get_call_statistics()
    print(f"\nCall Statistics:")
    print(f"  Total Calls: {stats['total_calls']}")
    print(f"  Completion Rate: {stats['completion_rate']:.1f}%")
    print(f"  Error Rate: {stats['error_rate']:.1f}%")
    print(f"  Escalation Rate: {stats['escalation_rate']:.1f}%")
    print(f"  Average Duration: {stats['average_duration_seconds']:.1f} seconds")
    
    # Get performance metrics
    perf_metrics = monitor.get_performance_metrics()
    print(f"\nPerformance Metrics:")
    for metric_name, values in perf_metrics.items():
        avg_value = sum(values) / len(values)
        print(f"  {metric_name}: {avg_value:.1f} (avg of {len(values)} samples)")
    
    # Get error analysis
    error_analysis = monitor.get_error_analysis()
    print(f"\nError Analysis:")
    for error_type, count in error_analysis.items():
        print(f"  {error_type}: {count} occurrences")
    
    print(f"\nVoice system logging demo completed!")
    print("   This demonstrates structured logging for production voice AI systems.")

if __name__ == "__main__":
    simulate_voice_system_logging()
