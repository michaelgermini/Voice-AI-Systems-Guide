#!/usr/bin/env python3
"""
Voice Security Framework Demo
Demonstrates comprehensive security measures for voice AI systems including
encryption, authentication, threat detection, and secure transmission.
"""

import hashlib
import secrets
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from cryptography.fernet import Fernet
import json

@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_id: str
    timestamp: datetime
    event_type: str
    severity: str
    user_id: Optional[str]
    ip_address: str
    details: Dict[str, Any]
    threat_level: str

class VoiceSecurityFramework:
    """Comprehensive security framework for voice AI systems"""
    
    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Security monitoring
        self.security_events = []
        self.failed_attempts = {}
        self.blocked_ips = set()
        self.user_sessions = {}
        
        # Threat detection patterns
        self.threat_patterns = {
            "voice_spoofing": [
                r"artificial.*voice",
                r"synthetic.*speech",
                r"voice.*clone",
                r"deepfake.*audio"
            ],
            "fraud_attempts": [
                r"password.*reset",
                r"account.*recovery",
                r"credit.*card.*number",
                r"social.*security.*number"
            ],
            "brute_force": [
                r"multiple.*failed.*attempts",
                r"rapid.*login.*attempts",
                r"dictionary.*attack"
            ]
        }
        
        # Security thresholds
        self.security_thresholds = {
            "max_failed_attempts": 5,
            "lockout_duration": 30,  # minutes
            "session_timeout": 3600,  # 1 hour
            "suspicious_activity_threshold": 0.8
        }
    
    def encrypt_voice_data(self, audio_data: bytes) -> Dict[str, Any]:
        """Encrypt voice audio data with metadata"""
        
        # Generate encryption metadata
        encryption_metadata = {
            "algorithm": "AES-256-GCM",
            "key_id": self.encryption_key[:16].hex(),
            "timestamp": datetime.now().isoformat(),
            "data_size": len(audio_data)
        }
        
        # Encrypt the audio data
        encrypted_data = self.cipher_suite.encrypt(audio_data)
        
        return {
            "encrypted_data": encrypted_data,
            "metadata": encryption_metadata,
            "checksum": hashlib.sha256(encrypted_data).hexdigest()
        }
    
    def decrypt_voice_data(self, encrypted_package: Dict[str, Any]) -> bytes:
        """Decrypt voice audio data"""
        
        try:
            encrypted_data = encrypted_package["encrypted_data"]
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            # Verify checksum
            expected_checksum = encrypted_package["checksum"]
            actual_checksum = hashlib.sha256(encrypted_data).hexdigest()
            
            if expected_checksum != actual_checksum:
                raise ValueError("Data integrity check failed")
            
            return decrypted_data
            
        except Exception as e:
            self.log_security_event(
                "decryption_failure",
                "ERROR",
                None,
                "192.168.1.1",
                {"error": str(e), "package_id": id(encrypted_package)}
            )
            raise
    
    def mask_sensitive_data(self, text: str) -> str:
        """Mask sensitive information in voice transcripts"""
        
        # Credit card numbers
        text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[CARD_NUMBER]', text)
        
        # SSN
        text = re.sub(r'\b\d{3}[\s-]?\d{2}[\s-]?\d{4}\b', '[SSN]', text)
        
        # Phone numbers
        text = re.sub(r'\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b', '[PHONE]', text)
        
        # Email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Account numbers
        text = re.sub(r'\baccount.*?\d{6,}\b', '[ACCOUNT_NUMBER]', text, flags=re.IGNORECASE)
        
        return text
    
    def authenticate_user(self, username: str, password: str, ip_address: str) -> Dict[str, Any]:
        """Authenticate user with security monitoring"""
        
        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            self.log_security_event(
                "blocked_ip_attempt",
                "WARN",
                username,
                ip_address,
                {"reason": "IP address is blocked"}
            )
            return {"authenticated": False, "error": "Access denied"}
        
        # Check failed attempts
        if ip_address in self.failed_attempts:
            failed_count = self.failed_attempts[ip_address]["count"]
            last_attempt = self.failed_attempts[ip_address]["timestamp"]
            
            # Check if lockout period has expired
            if time.time() - last_attempt < self.security_thresholds["lockout_duration"] * 60:
                if failed_count >= self.security_thresholds["max_failed_attempts"]:
                    self.log_security_event(
                        "account_locked",
                        "WARN",
                        username,
                        ip_address,
                        {"failed_attempts": failed_count}
                    )
                    return {"authenticated": False, "error": "Account temporarily locked"}
        
        # Simulate authentication (in practice, verify against database)
        if username == "admin" and password == "secure_password":
            # Successful authentication
            session_token = secrets.token_hex(32)
            self.user_sessions[session_token] = {
                "username": username,
                "ip_address": ip_address,
                "created_at": time.time(),
                "last_activity": time.time()
            }
            
            # Clear failed attempts
            if ip_address in self.failed_attempts:
                del self.failed_attempts[ip_address]
            
            self.log_security_event(
                "successful_login",
                "INFO",
                username,
                ip_address,
                {"session_token": session_token[:16] + "..."}
            )
            
            return {
                "authenticated": True,
                "session_token": session_token,
                "user_id": f"user_{hash(username)}"
            }
        else:
            # Failed authentication
            if ip_address not in self.failed_attempts:
                self.failed_attempts[ip_address] = {"count": 0, "timestamp": time.time()}
            
            self.failed_attempts[ip_address]["count"] += 1
            self.failed_attempts[ip_address]["timestamp"] = time.time()
            
            # Block IP if too many failed attempts
            if self.failed_attempts[ip_address]["count"] >= self.security_thresholds["max_failed_attempts"]:
                self.blocked_ips.add(ip_address)
                self.log_security_event(
                    "ip_blocked",
                    "CRITICAL",
                    username,
                    ip_address,
                    {"failed_attempts": self.failed_attempts[ip_address]["count"]}
                )
            
            self.log_security_event(
                "failed_login",
                "WARN",
                username,
                ip_address,
                {"failed_attempts": self.failed_attempts[ip_address]["count"]}
            )
            
            return {"authenticated": False, "error": "Invalid credentials"}
    
    def detect_threats(self, voice_transcript: str, user_id: str, ip_address: str) -> Dict[str, Any]:
        """Detect potential security threats in voice interactions"""
        
        threats_detected = []
        threat_score = 0.0
        
        # Check for threat patterns
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if re.search(pattern, voice_transcript, re.IGNORECASE):
                    threats_detected.append({
                        "type": threat_type,
                        "pattern": pattern,
                        "confidence": 0.8
                    })
                    threat_score += 0.2
        
        # Check for suspicious activity patterns
        suspicious_indicators = [
            "multiple account numbers mentioned",
            "rapid speech patterns",
            "background noise suggesting recording",
            "unusual call timing"
        ]
        
        # Simulate suspicious activity detection
        if len(voice_transcript.split()) > 100:  # Long transcript
            threat_score += 0.1
        
        if "urgent" in voice_transcript.lower() or "emergency" in voice_transcript.lower():
            threat_score += 0.15
        
        # Determine threat level
        if threat_score >= self.security_thresholds["suspicious_activity_threshold"]:
            threat_level = "HIGH"
        elif threat_score >= 0.5:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        # Log threat detection
        if threats_detected or threat_score > 0.3:
            self.log_security_event(
                "threat_detected",
                "WARN" if threat_level == "MEDIUM" else "CRITICAL",
                user_id,
                ip_address,
                {
                    "threats": threats_detected,
                    "threat_score": threat_score,
                    "transcript_preview": voice_transcript[:100] + "..."
                }
            )
        
        return {
            "threats_detected": threats_detected,
            "threat_score": threat_score,
            "threat_level": threat_level,
            "recommendations": self._get_threat_recommendations(threat_level)
        }
    
    def _get_threat_recommendations(self, threat_level: str) -> List[str]:
        """Get security recommendations based on threat level"""
        
        recommendations = {
            "LOW": [
                "Continue monitoring",
                "Log interaction for analysis"
            ],
            "MEDIUM": [
                "Increase monitoring frequency",
                "Request additional verification",
                "Flag for manual review"
            ],
            "HIGH": [
                "Immediate escalation to security team",
                "Block user access temporarily",
                "Initiate fraud investigation",
                "Contact law enforcement if necessary"
            ]
        }
        
        return recommendations.get(threat_level, ["Unknown threat level"])
    
    def log_security_event(self, event_type: str, severity: str, user_id: Optional[str], 
                          ip_address: str, details: Dict[str, Any]) -> str:
        """Log security event with comprehensive details"""
        
        event_id = f"sec_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        security_event = SecurityEvent(
            event_id=event_id,
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            ip_address=ip_address,
            details=details,
            threat_level=self._calculate_threat_level(severity, details)
        )
        
        self.security_events.append(security_event)
        
        return event_id
    
    def _calculate_threat_level(self, severity: str, details: Dict[str, Any]) -> str:
        """Calculate threat level based on severity and details"""
        
        severity_weights = {
            "INFO": 0.1,
            "WARN": 0.5,
            "ERROR": 0.7,
            "CRITICAL": 1.0
        }
        
        base_score = severity_weights.get(severity, 0.1)
        
        # Adjust based on details
        if "failed_attempts" in details:
            base_score += min(details["failed_attempts"] * 0.1, 0.5)
        
        if "threat_score" in details:
            base_score += details["threat_score"] * 0.3
        
        if base_score >= 0.8:
            return "HIGH"
        elif base_score >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_security_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        
        period_events = [
            event for event in self.security_events
            if start_date <= event.timestamp <= end_date
        ]
        
        # Analyze events by type
        event_counts = {}
        severity_counts = {}
        threat_level_counts = {}
        
        for event in period_events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
            severity_counts[event.severity] = severity_counts.get(event.severity, 0) + 1
            threat_level_counts[event.threat_level] = threat_level_counts.get(event.threat_level, 0) + 1
        
        # Calculate security metrics
        total_events = len(period_events)
        critical_events = len([e for e in period_events if e.severity == "CRITICAL"])
        high_threat_events = len([e for e in period_events if e.threat_level == "HIGH"])
        
        return {
            "report_period": f"{start_date} to {end_date}",
            "total_security_events": total_events,
            "critical_events": critical_events,
            "high_threat_events": high_threat_events,
            "event_type_breakdown": event_counts,
            "severity_breakdown": severity_counts,
            "threat_level_breakdown": threat_level_counts,
            "blocked_ips_count": len(self.blocked_ips),
            "active_sessions_count": len(self.user_sessions),
            "security_status": "SECURE" if critical_events == 0 else "ATTENTION_REQUIRED",
            "recommendations": self._get_security_recommendations(period_events)
        }
    
    def _get_security_recommendations(self, events: List[SecurityEvent]) -> List[str]:
        """Get security recommendations based on events"""
        
        recommendations = []
        
        critical_count = len([e for e in events if e.severity == "CRITICAL"])
        failed_logins = len([e for e in events if e.event_type == "failed_login"])
        
        if critical_count > 0:
            recommendations.append("Review critical security events immediately")
        
        if failed_logins > 10:
            recommendations.append("Consider implementing additional authentication measures")
        
        if len(self.blocked_ips) > 5:
            recommendations.append("Review IP blocking policies and whitelist legitimate users")
        
        if not recommendations:
            recommendations.append("Security posture appears healthy - continue monitoring")
        
        return recommendations

def simulate_voice_security_scenarios():
    """Simulate various voice security scenarios"""
    
    print("Voice Security Framework Demo")
    print("=" * 60)
    
    # Initialize security framework
    security = VoiceSecurityFramework()
    
    # Scenario 1: Normal voice interaction
    print("\n1. Normal Voice Interaction")
    print("-" * 30)
    
    normal_audio = b"Hello, I need help with my account balance"
    encrypted_package = security.encrypt_voice_data(normal_audio)
    decrypted_audio = security.decrypt_voice_data(encrypted_package)
    
    print(f"Original audio length: {len(normal_audio)} bytes")
    print(f"Encrypted package size: {len(encrypted_package['encrypted_data'])} bytes")
    print(f"Decrypted audio matches: {normal_audio == decrypted_audio}")
    
    # Scenario 2: Sensitive data masking
    print("\n2. Sensitive Data Masking")
    print("-" * 30)
    
    sensitive_text = "My credit card is 1234-5678-9012-3456 and SSN is 123-45-6789"
    masked_text = security.mask_sensitive_data(sensitive_text)
    
    print(f"Original: {sensitive_text}")
    print(f"Masked:   {masked_text}")
    
    # Scenario 3: Authentication with security monitoring
    print("\n3. Authentication Security")
    print("-" * 30)
    
    # Successful login
    auth_result = security.authenticate_user("admin", "secure_password", "192.168.1.100")
    print(f"Successful login: {auth_result['authenticated']}")
    
    # Failed login attempts
    for i in range(6):
        auth_result = security.authenticate_user("admin", "wrong_password", "192.168.1.200")
        print(f"Failed attempt {i+1}: {auth_result['error']}")
    
    # Scenario 4: Threat detection
    print("\n4. Threat Detection")
    print("-" * 30)
    
    # Normal transcript
    normal_transcript = "Hello, I need help with my account"
    threat_result = security.detect_threats(normal_transcript, "user123", "192.168.1.100")
    print(f"Normal transcript threat level: {threat_result['threat_level']}")
    
    # Suspicious transcript
    suspicious_transcript = "I need to reset my password immediately and my credit card number is 1234-5678-9012-3456"
    threat_result = security.detect_threats(suspicious_transcript, "user456", "192.168.1.200")
    print(f"Suspicious transcript threat level: {threat_result['threat_level']}")
    print(f"Threats detected: {len(threat_result['threats_detected'])}")
    
    # Scenario 5: Security report
    print("\n5. Security Report")
    print("-" * 30)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=1)
    
    security_report = security.generate_security_report(start_date, end_date)
    
    print(f"Total security events: {security_report['total_security_events']}")
    print(f"Critical events: {security_report['critical_events']}")
    print(f"High threat events: {security_report['high_threat_events']}")
    print(f"Blocked IPs: {security_report['blocked_ips_count']}")
    print(f"Security status: {security_report['security_status']}")
    
    print("\nEvent Type Breakdown:")
    for event_type, count in security_report['event_type_breakdown'].items():
        print(f"  {event_type}: {count}")
    
    print("\nRecommendations:")
    for rec in security_report['recommendations']:
        print(f"  • {rec}")
    
    # Scenario 6: Voice data security workflow
    print("\n6. Complete Voice Security Workflow")
    print("-" * 40)
    
    # Simulate a complete voice interaction with security
    voice_input = "My account number is 123456789 and I need to reset my password"
    user_id = "customer_001"
    ip_address = "203.0.113.45"
    
    print(f"Voice input: {voice_input}")
    
    # Step 1: Mask sensitive data
    masked_input = security.mask_sensitive_data(voice_input)
    print(f"Masked input: {masked_input}")
    
    # Step 2: Detect threats
    threat_analysis = security.detect_threats(voice_input, user_id, ip_address)
    print(f"Threat level: {threat_analysis['threat_level']}")
    print(f"Threat score: {threat_analysis['threat_score']:.2f}")
    
    # Step 3: Encrypt for processing
    audio_data = voice_input.encode('utf-8')
    encrypted_package = security.encrypt_voice_data(audio_data)
    print(f"Audio encrypted: {len(encrypted_package['encrypted_data'])} bytes")
    
    # Step 4: Process securely
    decrypted_data = security.decrypt_voice_data(encrypted_package)
    processed_text = decrypted_data.decode('utf-8')
    print(f"Processed text: {processed_text}")
    
    print("\n" + "=" * 60)
    print("Voice Security Framework Demo Complete")
    print("=" * 60)
    
    return security

if __name__ == "__main__":
    security_framework = simulate_voice_security_scenarios()
