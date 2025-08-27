#!/usr/bin/env python3
"""
Audit System Demo
Demonstrates comprehensive audit trails, monitoring, and compliance verification
for voice AI systems with detailed logging and analysis capabilities.
"""

import hashlib
import secrets
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

class AuditLevel(Enum):
    """Audit log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AuditCategory(Enum):
    """Audit event categories"""
    SECURITY = "security"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    USER_ACTIVITY = "user_activity"
    SYSTEM_OPERATION = "system_operation"
    DATA_ACCESS = "data_access"

@dataclass
class AuditEvent:
    """Audit event data structure"""
    event_id: str
    timestamp: datetime
    level: AuditLevel
    category: AuditCategory
    event_type: str
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: str
    user_agent: str
    action: str
    resource: str
    details: Dict[str, Any]
    metadata: Dict[str, Any]
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None

class VoiceAuditSystem:
    """Comprehensive audit system for voice AI applications"""
    
    def __init__(self):
        self.audit_events = []
        self.audit_config = {
            "retention_days": 2555,  # 7 years
            "log_levels": [level.value for level in AuditLevel],
            "sensitive_fields": [
                "password", "ssn", "credit_card", "api_key", 
                "token", "secret", "private_key"
            ],
            "correlation_enabled": True,
            "real_time_monitoring": True
        }
        
        # Real-time monitoring
        self.alert_thresholds = {
            "failed_authentications": 5,
            "data_access_frequency": 100,  # per hour
            "error_rate": 0.05,  # 5%
            "suspicious_activity_score": 0.8
        }
        
        self.monitoring_alerts = []
        self.correlation_events = {}
    
    def log_audit_event(self, level: AuditLevel, category: AuditCategory, 
                       event_type: str, user_id: Optional[str], 
                       action: str, resource: str, details: Dict[str, Any],
                       session_id: Optional[str] = None, 
                       correlation_id: Optional[str] = None,
                       parent_event_id: Optional[str] = None) -> str:
        """Log audit event with comprehensive details"""
        
        event_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Sanitize sensitive data
        sanitized_details = self._sanitize_details(details)
        
        # Generate metadata
        metadata = {
            "event_source": "voice_ai_system",
            "version": "1.0",
            "environment": "production",
            "component": "audit_system"
        }
        
        audit_event = AuditEvent(
            event_id=event_id,
            timestamp=datetime.now(),
            level=level,
            category=category,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            ip_address=self._get_client_ip(),
            user_agent=self._get_user_agent(),
            action=action,
            resource=resource,
            details=sanitized_details,
            metadata=metadata,
            correlation_id=correlation_id,
            parent_event_id=parent_event_id
        )
        
        self.audit_events.append(audit_event)
        
        # Store correlation event if enabled
        if self.audit_config["correlation_enabled"] and correlation_id:
            if correlation_id not in self.correlation_events:
                self.correlation_events[correlation_id] = []
            self.correlation_events[correlation_id].append(audit_event)
        
        # Real-time monitoring
        if self.audit_config["real_time_monitoring"]:
            self._check_real_time_alerts(audit_event)
        
        return event_id
    
    def _sanitize_details(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive information from audit details"""
        
        sanitized = details.copy()
        
        def sanitize_value(value):
            if isinstance(value, str):
                for field in self.audit_config["sensitive_fields"]:
                    if field.lower() in value.lower():
                        return "[REDACTED]"
            elif isinstance(value, dict):
                return {k: sanitize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [sanitize_value(v) for v in value]
            return value
        
        return sanitize_value(sanitized)
    
    def _get_client_ip(self) -> str:
        """Get client IP address (simulated)"""
        return "192.168.1.100"
    
    def _get_user_agent(self) -> str:
        """Get user agent (simulated)"""
        return "VoiceAI/1.0 (Python/3.9)"
    
    def _check_real_time_alerts(self, event: AuditEvent):
        """Check for real-time alert conditions"""
        
        # Check for failed authentications
        if event.event_type == "authentication_failed":
            recent_failures = len([
                e for e in self.audit_events[-100:]  # Last 100 events
                if e.event_type == "authentication_failed" and
                e.user_id == event.user_id and
                (datetime.now() - e.timestamp).seconds < 3600  # Last hour
            ])
            
            if recent_failures >= self.alert_thresholds["failed_authentications"]:
                self._generate_alert(
                    "HIGH_FAILURE_RATE",
                    f"User {event.user_id} has {recent_failures} failed authentication attempts",
                    event
                )
        
        # Check for suspicious activity
        if event.category == AuditCategory.SECURITY:
            suspicious_score = self._calculate_suspicious_activity_score(event)
            if suspicious_score >= self.alert_thresholds["suspicious_activity_score"]:
                self._generate_alert(
                    "SUSPICIOUS_ACTIVITY",
                    f"Suspicious activity detected with score {suspicious_score:.2f}",
                    event
                )
        
        # Check for high error rates
        if event.level in [AuditLevel.ERROR, AuditLevel.CRITICAL]:
            recent_errors = len([
                e for e in self.audit_events[-1000:]  # Last 1000 events
                if e.level in [AuditLevel.ERROR, AuditLevel.CRITICAL] and
                (datetime.now() - e.timestamp).seconds < 3600  # Last hour
            ])
            
            total_recent_events = len([
                e for e in self.audit_events[-1000:]
                if (datetime.now() - e.timestamp).seconds < 3600
            ])
            
            if total_recent_events > 0:
                error_rate = recent_errors / total_recent_events
                if error_rate >= self.alert_thresholds["error_rate"]:
                    self._generate_alert(
                        "HIGH_ERROR_RATE",
                        f"High error rate detected: {error_rate:.2%}",
                        event
                    )
    
    def _calculate_suspicious_activity_score(self, event: AuditEvent) -> float:
        """Calculate suspicious activity score"""
        
        score = 0.0
        
        # Check for unusual access patterns
        if event.category == AuditCategory.DATA_ACCESS:
            recent_access = len([
                e for e in self.audit_events[-100:]
                if e.category == AuditCategory.DATA_ACCESS and
                e.user_id == event.user_id and
                (datetime.now() - e.timestamp).seconds < 3600
            ])
            
            if recent_access > 50:  # More than 50 data access events per hour
                score += 0.3
        
        # Check for security-related events
        if event.category == AuditCategory.SECURITY:
            score += 0.2
        
        # Check for unusual times
        hour = event.timestamp.hour
        if hour < 6 or hour > 22:  # Outside business hours
            score += 0.1
        
        # Check for multiple failed attempts
        if event.event_type == "authentication_failed":
            score += 0.2
        
        return min(score, 1.0)
    
    def _generate_alert(self, alert_type: str, message: str, event: AuditEvent):
        """Generate monitoring alert"""
        
        alert = {
            "alert_id": f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "timestamp": datetime.now(),
            "alert_type": alert_type,
            "message": message,
            "severity": "HIGH" if alert_type in ["SUSPICIOUS_ACTIVITY", "HIGH_ERROR_RATE"] else "MEDIUM",
            "event_id": event.event_id,
            "user_id": event.user_id,
            "ip_address": event.ip_address
        }
        
        self.monitoring_alerts.append(alert)
        
        # In practice, send to monitoring system
        print(f"ALERT: {alert_type} - {message}")
    
    def search_audit_logs(self, filters: Dict[str, Any]) -> List[AuditEvent]:
        """Search audit logs with filters"""
        
        results = []
        
        for event in self.audit_events:
            match = True
            
            for key, value in filters.items():
                if hasattr(event, key):
                    event_value = getattr(event, key)
                    if isinstance(value, list):
                        if event_value not in value:
                            match = False
                            break
                    else:
                        if event_value != value:
                            match = False
                            break
                else:
                    match = False
                    break
            
            if match:
                results.append(event)
        
        return results
    
    def get_correlation_events(self, correlation_id: str) -> List[AuditEvent]:
        """Get all events for a specific correlation ID"""
        
        return self.correlation_events.get(correlation_id, [])
    
    def generate_audit_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        
        period_events = [
            event for event in self.audit_events
            if start_date <= event.timestamp <= end_date
        ]
        
        # Analyze by category
        category_counts = {}
        level_counts = {}
        event_type_counts = {}
        user_activity = {}
        
        for event in period_events:
            # Category breakdown
            category = event.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Level breakdown
            level = event.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
            
            # Event type breakdown
            event_type = event.event_type
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            # User activity
            if event.user_id:
                if event.user_id not in user_activity:
                    user_activity[event.user_id] = {
                        "total_events": 0,
                        "categories": {},
                        "last_activity": None
                    }
                
                user_activity[event.user_id]["total_events"] += 1
                user_activity[event.user_id]["categories"][category] = \
                    user_activity[event.user_id]["categories"].get(category, 0) + 1
                
                if (user_activity[event.user_id]["last_activity"] is None or 
                    event.timestamp > user_activity[event.user_id]["last_activity"]):
                    user_activity[event.user_id]["last_activity"] = event.timestamp
        
        # Calculate compliance metrics
        compliance_metrics = self._calculate_compliance_metrics(period_events)
        
        # Security analysis
        security_analysis = self._analyze_security_events(period_events)
        
        return {
            "report_period": f"{start_date} to {end_date}",
            "total_events": len(period_events),
            "category_breakdown": category_counts,
            "level_breakdown": level_counts,
            "event_type_breakdown": event_type_counts,
            "user_activity": user_activity,
            "compliance_metrics": compliance_metrics,
            "security_analysis": security_analysis,
            "alerts_generated": len([
                alert for alert in self.monitoring_alerts
                if start_date <= alert["timestamp"] <= end_date
            ]),
            "correlation_events": len(self.correlation_events),
            "compliance_status": "compliant" if compliance_metrics["overall_score"] >= 0.8 else "attention_required"
        }
    
    def _calculate_compliance_metrics(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Calculate compliance metrics"""
        
        metrics = {
            "data_access_logged": 0,
            "security_events_logged": 0,
            "user_activity_tracked": 0,
            "error_events_logged": 0,
            "overall_score": 0.0
        }
        
        for event in events:
            if event.category == AuditCategory.DATA_ACCESS:
                metrics["data_access_logged"] += 1
            elif event.category == AuditCategory.SECURITY:
                metrics["security_events_logged"] += 1
            elif event.category == AuditCategory.USER_ACTIVITY:
                metrics["user_activity_tracked"] += 1
            elif event.level in [AuditLevel.ERROR, AuditLevel.CRITICAL]:
                metrics["error_events_logged"] += 1
        
        # Calculate overall compliance score
        total_events = len(events)
        if total_events > 0:
            metrics["overall_score"] = (
                (metrics["data_access_logged"] / total_events) * 0.3 +
                (metrics["security_events_logged"] / total_events) * 0.3 +
                (metrics["user_activity_tracked"] / total_events) * 0.2 +
                (metrics["error_events_logged"] / total_events) * 0.2
            )
        
        return metrics
    
    def _analyze_security_events(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Analyze security-related events"""
        
        security_events = [e for e in events if e.category == AuditCategory.SECURITY]
        
        analysis = {
            "total_security_events": len(security_events),
            "authentication_events": 0,
            "authorization_events": 0,
            "data_access_events": 0,
            "suspicious_activities": 0,
            "threat_level": "LOW"
        }
        
        for event in security_events:
            if "auth" in event.event_type.lower():
                analysis["authentication_events"] += 1
            elif "access" in event.event_type.lower():
                analysis["data_access_events"] += 1
            elif "suspicious" in event.event_type.lower():
                analysis["suspicious_activities"] += 1
        
        # Determine threat level
        if analysis["suspicious_activities"] > 10:
            analysis["threat_level"] = "HIGH"
        elif analysis["suspicious_activities"] > 5:
            analysis["threat_level"] = "MEDIUM"
        
        return analysis
    
    def export_audit_logs(self, start_date: datetime, end_date: datetime, 
                         format: str = "json") -> str:
        """Export audit logs in specified format"""
        
        period_events = [
            event for event in self.audit_events
            if start_date <= event.timestamp <= end_date
        ]
        
        if format.lower() == "json":
            # Convert events to dictionaries
            export_data = []
            for event in period_events:
                event_dict = {
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "level": event.level.value,
                    "category": event.category.value,
                    "event_type": event.event_type,
                    "user_id": event.user_id,
                    "session_id": event.session_id,
                    "ip_address": event.ip_address,
                    "user_agent": event.user_agent,
                    "action": event.action,
                    "resource": event.resource,
                    "details": event.details,
                    "metadata": event.metadata,
                    "correlation_id": event.correlation_id,
                    "parent_event_id": event.parent_event_id
                }
                export_data.append(event_dict)
            
            return json.dumps(export_data, indent=2)
        
        elif format.lower() == "csv":
            # Generate CSV format
            csv_lines = [
                "event_id,timestamp,level,category,event_type,user_id,action,resource,ip_address"
            ]
            
            for event in period_events:
                csv_line = f"{event.event_id},{event.timestamp.isoformat()},{event.level.value},{event.category.value},{event.event_type},{event.user_id or ''},{event.action},{event.resource},{event.ip_address}"
                csv_lines.append(csv_line)
            
            return "\n".join(csv_lines)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")

def simulate_audit_scenarios():
    """Simulate various audit scenarios"""
    
    print("Audit System Demo")
    print("=" * 60)
    
    # Initialize audit system
    audit = VoiceAuditSystem()
    
    # Scenario 1: User Authentication Events
    print("\n1. User Authentication Events")
    print("-" * 30)
    
    user_id = "user_001"
    session_id = "session_123"
    correlation_id = "corr_001"
    
    # Successful login
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.SECURITY,
        "authentication_success",
        user_id,
        "login",
        "authentication_service",
        {
            "method": "password",
            "ip_address": "192.168.1.100",
            "user_agent": "VoiceAI/1.0"
        },
        session_id,
        correlation_id
    )
    
    # Failed login attempts
    for i in range(3):
        audit.log_audit_event(
            AuditLevel.WARN,
            AuditCategory.SECURITY,
            "authentication_failed",
            user_id,
            "login_attempt",
            "authentication_service",
            {
                "method": "password",
                "reason": "invalid_credentials",
                "attempt_number": i + 1
            },
            session_id,
            correlation_id
        )
    
    print(f"Logged authentication events for user {user_id}")
    
    # Scenario 2: Data Access Events
    print("\n2. Data Access Events")
    print("-" * 30)
    
    # Voice data access
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.DATA_ACCESS,
        "voice_data_accessed",
        user_id,
        "read",
        "voice_recording_001",
        {
            "data_type": "voice_recording",
            "duration": 120,
            "purpose": "customer_service"
        },
        session_id,
        correlation_id
    )
    
    # Sensitive data access
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.DATA_ACCESS,
        "personal_data_accessed",
        user_id,
        "read",
        "user_profile",
        {
            "data_type": "personal_information",
            "fields_accessed": ["name", "email", "phone"],
            "purpose": "account_verification"
        },
        session_id,
        correlation_id
    )
    
    print(f"Logged data access events for user {user_id}")
    
    # Scenario 3: Compliance Events
    print("\n3. Compliance Events")
    print("-" * 30)
    
    # GDPR consent
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.COMPLIANCE,
        "gdpr_consent_recorded",
        user_id,
        "consent_given",
        "gdpr_consent",
        {
            "consent_type": "voice_recording",
            "consent_given": True,
            "timestamp": datetime.now().isoformat()
        },
        session_id,
        correlation_id
    )
    
    # HIPAA PHI access
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.COMPLIANCE,
        "hipaa_phi_accessed",
        user_id,
        "read",
        "patient_record_001",
        {
            "patient_id": "patient_001",
            "data_type": "medical_condition",
            "purpose": "treatment",
            "authorized": True
        },
        session_id,
        correlation_id
    )
    
    print(f"Logged compliance events for user {user_id}")
    
    # Scenario 4: Performance Events
    print("\n4. Performance Events")
    print("-" * 30)
    
    # Voice processing performance
    audit.log_audit_event(
        AuditLevel.INFO,
        AuditCategory.PERFORMANCE,
        "voice_processing_completed",
        user_id,
        "process",
        "voice_processor",
        {
            "processing_time_ms": 1250,
            "audio_length_seconds": 30,
            "quality_score": 0.95
        },
        session_id,
        correlation_id
    )
    
    # Error event
    audit.log_audit_event(
        AuditLevel.ERROR,
        AuditCategory.PERFORMANCE,
        "voice_processing_failed",
        user_id,
        "process",
        "voice_processor",
        {
            "error_code": "AUDIO_FORMAT_ERROR",
            "error_message": "Unsupported audio format",
            "audio_format": "wav"
        },
        session_id,
        correlation_id
    )
    
    print(f"Logged performance events for user {user_id}")
    
    # Scenario 5: Audit Report Generation
    print("\n5. Audit Report Generation")
    print("-" * 30)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=1)
    
    audit_report = audit.generate_audit_report(start_date, end_date)
    
    print(f"Total events: {audit_report['total_events']}")
    print(f"Compliance status: {audit_report['compliance_status']}")
    print(f"Alerts generated: {audit_report['alerts_generated']}")
    
    print("\nCategory Breakdown:")
    for category, count in audit_report['category_breakdown'].items():
        print(f"  {category}: {count}")
    
    print("\nLevel Breakdown:")
    for level, count in audit_report['level_breakdown'].items():
        print(f"  {level}: {count}")
    
    print(f"\nSecurity Analysis:")
    security = audit_report['security_analysis']
    print(f"  Threat level: {security['threat_level']}")
    print(f"  Security events: {security['total_security_events']}")
    print(f"  Suspicious activities: {security['suspicious_activities']}")
    
    # Scenario 6: Audit Log Search
    print("\n6. Audit Log Search")
    print("-" * 30)
    
    # Search for security events
    security_events = audit.search_audit_logs({
        "category": AuditCategory.SECURITY
    })
    print(f"Found {len(security_events)} security events")
    
    # Search for user-specific events
    user_events = audit.search_audit_logs({
        "user_id": user_id
    })
    print(f"Found {len(user_events)} events for user {user_id}")
    
    # Search for error events
    error_events = audit.search_audit_logs({
        "level": [AuditLevel.ERROR, AuditLevel.CRITICAL]
    })
    print(f"Found {len(error_events)} error events")
    
    # Scenario 7: Correlation Analysis
    print("\n7. Correlation Analysis")
    print("-" * 30)
    
    correlation_events = audit.get_correlation_events(correlation_id)
    print(f"Found {len(correlation_events)} events for correlation ID {correlation_id}")
    
    for event in correlation_events:
        print(f"  {event.timestamp}: {event.event_type} ({event.category.value})")
    
    # Scenario 8: Export Audit Logs
    print("\n8. Export Audit Logs")
    print("-" * 30)
    
    # Export as JSON
    json_export = audit.export_audit_logs(start_date, end_date, "json")
    print(f"JSON export length: {len(json_export)} characters")
    
    # Export as CSV
    csv_export = audit.export_audit_logs(start_date, end_date, "csv")
    print(f"CSV export lines: {len(csv_export.split(chr(10)))}")
    
    print("\n" + "=" * 60)
    print("Audit System Demo Complete")
    print("=" * 60)
    
    return audit

if __name__ == "__main__":
    audit_system = simulate_audit_scenarios()
