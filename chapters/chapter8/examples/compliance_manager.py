#!/usr/bin/env python3
"""
Compliance Manager Demo
Demonstrates comprehensive compliance management for voice AI systems including
GDPR, HIPAA, and PCI compliance requirements.
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

class ComplianceType(Enum):
    """Types of compliance frameworks"""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI = "pci"
    CCPA = "ccpa"

@dataclass
class ComplianceEvent:
    """Compliance event data structure"""
    event_id: str
    timestamp: datetime
    compliance_type: ComplianceType
    event_type: str
    user_id: Optional[str]
    data_type: str
    action: str
    details: Dict[str, Any]
    status: str

class ComplianceManager:
    """Comprehensive compliance management for voice AI systems"""
    
    def __init__(self):
        self.compliance_events = []
        self.consent_records = {}
        self.data_retention_policies = {
            ComplianceType.GDPR: {
                "voice_recordings": 30,  # days
                "transcripts": 90,
                "user_profiles": 365,
                "analytics_data": 730
            },
            ComplianceType.HIPAA: {
                "phi_data": 2555,  # 7 years
                "access_logs": 2555,
                "audit_trails": 2555
            },
            ComplianceType.PCI: {
                "payment_data": 0,  # No retention allowed
                "transaction_logs": 2555,
                "security_logs": 2555
            }
        }
        
        self.data_subjects = {}
        self.phi_records = {}  # Protected Health Information
        self.payment_records = {}
        
        # Compliance requirements
        self.compliance_requirements = {
            ComplianceType.GDPR: [
                "data_minimization",
                "purpose_limitation",
                "storage_limitation",
                "accuracy",
                "integrity_confidentiality",
                "accountability"
            ],
            ComplianceType.HIPAA: [
                "privacy_rule",
                "security_rule",
                "breach_notification",
                "minimum_necessary",
                "patient_rights"
            ],
            ComplianceType.PCI: [
                "data_encryption",
                "access_controls",
                "audit_logging",
                "vulnerability_management",
                "incident_response"
            ]
        }
    
    def record_consent(self, user_id: str, consent_type: str, 
                      consent_given: bool, compliance_type: ComplianceType) -> str:
        """Record user consent for data processing"""
        
        consent_id = f"consent_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        consent_record = {
            "consent_id": consent_id,
            "user_id": user_id,
            "consent_type": consent_type,
            "consent_given": consent_given,
            "compliance_type": compliance_type.value,
            "timestamp": datetime.now(),
            "ip_address": "192.168.1.1",
            "user_agent": "VoiceAI/1.0",
            "language": "en-US"
        }
        
        self.consent_records[consent_id] = consent_record
        
        # Log compliance event
        self.log_compliance_event(
            compliance_type,
            "consent_recorded",
            user_id,
            "consent",
            "record",
            {
                "consent_id": consent_id,
                "consent_given": consent_given,
                "consent_type": consent_type
            }
        )
        
        return consent_id
    
    def check_consent(self, user_id: str, consent_type: str, 
                     compliance_type: ComplianceType) -> bool:
        """Check if user has given consent for specific processing"""
        
        # Find most recent consent for this user, type, and compliance framework
        latest_consent = None
        latest_timestamp = None
        
        for consent_id, consent_data in self.consent_records.items():
            if (consent_data["user_id"] == user_id and 
                consent_data["consent_type"] == consent_type and
                consent_data["compliance_type"] == compliance_type.value):
                
                if latest_timestamp is None or consent_data["timestamp"] > latest_timestamp:
                    latest_consent = consent_data
                    latest_timestamp = consent_data["timestamp"]
        
        if latest_consent is None:
            return False
        
        return latest_consent["consent_given"]
    
    def process_gdpr_request(self, user_id: str, request_type: str) -> Dict[str, Any]:
        """Process GDPR data subject requests"""
        
        if request_type == "access":
            return self._handle_gdpr_access_request(user_id)
        elif request_type == "deletion":
            return self._handle_gdpr_deletion_request(user_id)
        elif request_type == "portability":
            return self._handle_gdpr_portability_request(user_id)
        elif request_type == "rectification":
            return self._handle_gdpr_rectification_request(user_id)
        else:
            return {"error": "Unknown GDPR request type"}
    
    def _handle_gdpr_access_request(self, user_id: str) -> Dict[str, Any]:
        """Handle GDPR right of access request"""
        
        user_data = {
            "personal_data": self._get_user_personal_data(user_id),
            "processing_activities": self._get_processing_activities(user_id),
            "consent_records": self._get_user_consent_records(user_id, ComplianceType.GDPR)
        }
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.GDPR,
            "access_request_processed",
            user_id,
            "personal_data",
            "access",
            {"data_types": list(user_data.keys())}
        )
        
        return {
            "request_type": "access",
            "user_id": user_id,
            "data": user_data,
            "timestamp": datetime.now(),
            "compliance_status": "compliant"
        }
    
    def _handle_gdpr_deletion_request(self, user_id: str) -> Dict[str, Any]:
        """Handle GDPR right to be forgotten request"""
        
        # Mark user data for deletion
        self.data_subjects[user_id] = {
            "deletion_requested": True,
            "deletion_date": datetime.now(),
            "retention_period": 30,  # days to retain for legal purposes
            "compliance_type": ComplianceType.GDPR.value
        }
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.GDPR,
            "deletion_request_processed",
            user_id,
            "personal_data",
            "deletion",
            {"retention_period": 30}
        )
        
        return {
            "request_type": "deletion",
            "user_id": user_id,
            "status": "deletion_scheduled",
            "completion_date": datetime.now() + timedelta(days=30),
            "compliance_status": "compliant"
        }
    
    def _handle_gdpr_portability_request(self, user_id: str) -> Dict[str, Any]:
        """Handle GDPR data portability request"""
        
        portable_data = {
            "personal_data": self._get_user_personal_data(user_id),
            "voice_recordings": self._get_user_voice_data(user_id),
            "interaction_history": self._get_user_interactions(user_id)
        }
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.GDPR,
            "portability_request_processed",
            user_id,
            "personal_data",
            "export",
            {"data_types": list(portable_data.keys())}
        )
        
        return {
            "request_type": "portability",
            "user_id": user_id,
            "data": portable_data,
            "format": "JSON",
            "timestamp": datetime.now(),
            "compliance_status": "compliant"
        }
    
    def _handle_gdpr_rectification_request(self, user_id: str) -> Dict[str, Any]:
        """Handle GDPR data rectification request"""
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.GDPR,
            "rectification_request_processed",
            user_id,
            "personal_data",
            "rectification",
            {"status": "pending_user_input"}
        )
        
        return {
            "request_type": "rectification",
            "user_id": user_id,
            "status": "pending",
            "message": "Please provide the corrected information",
            "timestamp": datetime.now(),
            "compliance_status": "compliant"
        }
    
    def handle_hipaa_data(self, patient_id: str, data_type: str, 
                         data_content: str, user_id: str, purpose: str) -> Dict[str, Any]:
        """Handle Protected Health Information with HIPAA compliance"""
        
        # Validate purpose
        valid_purposes = ["treatment", "payment", "operations"]
        if purpose not in valid_purposes:
            return {
                "status": "error",
                "error": f"Invalid purpose. Must be one of: {valid_purposes}"
            }
        
        # Log access
        access_id = self._log_hipaa_access(patient_id, user_id, data_type, purpose)
        
        # Encrypt PHI data
        encrypted_data = self._encrypt_phi_data(data_content)
        
        # Store with audit trail
        self.phi_records[access_id] = {
            "patient_id": patient_id,
            "data_type": data_type,
            "encrypted_data": encrypted_data,
            "user_id": user_id,
            "timestamp": datetime.now(),
            "purpose": purpose,
            "compliance_type": ComplianceType.HIPAA.value
        }
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.HIPAA,
            "phi_data_handled",
            user_id,
            data_type,
            "access",
            {
                "patient_id": patient_id,
                "purpose": purpose,
                "access_id": access_id
            }
        )
        
        return {
            "access_id": access_id,
            "status": "phi_handled",
            "compliance_verified": True,
            "purpose": purpose
        }
    
    def _log_hipaa_access(self, patient_id: str, user_id: str, data_type: str, purpose: str) -> str:
        """Log access to PHI"""
        
        access_id = f"hipaa_access_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        # In practice, store in database
        access_log = {
            "access_id": access_id,
            "patient_id": patient_id,
            "user_id": user_id,
            "data_type": data_type,
            "timestamp": datetime.now(),
            "purpose": purpose,
            "ip_address": "192.168.1.1",
            "action": "access"
        }
        
        return access_id
    
    def _encrypt_phi_data(self, data: str) -> str:
        """Encrypt PHI data"""
        # In practice, use strong encryption
        return f"encrypted_{hash(data)}"
    
    def handle_pci_data(self, transaction_id: str, payment_data: Dict[str, Any], 
                       user_id: str) -> Dict[str, Any]:
        """Handle payment data with PCI compliance"""
        
        # Validate payment data
        required_fields = ["card_number", "expiry_date", "cvv", "amount"]
        for field in required_fields:
            if field not in payment_data:
                return {
                    "status": "error",
                    "error": f"Missing required field: {field}"
                }
        
        # Tokenize sensitive payment data
        tokenized_data = self._tokenize_payment_data(payment_data)
        
        # Store transaction record (no sensitive data)
        self.payment_records[transaction_id] = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": payment_data["amount"],
            "currency": payment_data.get("currency", "USD"),
            "timestamp": datetime.now(),
            "token": tokenized_data["token"],
            "compliance_type": ComplianceType.PCI.value
        }
        
        # Log compliance event
        self.log_compliance_event(
            ComplianceType.PCI,
            "payment_data_processed",
            user_id,
            "payment",
            "process",
            {
                "transaction_id": transaction_id,
                "amount": payment_data["amount"],
                "tokenized": True
            }
        )
        
        return {
            "transaction_id": transaction_id,
            "status": "payment_processed",
            "token": tokenized_data["token"],
            "compliance_verified": True
        }
    
    def _tokenize_payment_data(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tokenize sensitive payment data"""
        
        # Generate token for card number
        card_token = f"tok_{secrets.token_hex(16)}"
        
        return {
            "token": card_token,
            "masked_card": f"****-****-****-{payment_data['card_number'][-4:]}",
            "expiry": payment_data["expiry_date"],
            "amount": payment_data["amount"]
        }
    
    def log_compliance_event(self, compliance_type: ComplianceType, event_type: str,
                           user_id: Optional[str], data_type: str, action: str,
                           details: Dict[str, Any]) -> str:
        """Log compliance event with comprehensive details"""
        
        event_id = f"comp_{compliance_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        compliance_event = ComplianceEvent(
            event_id=event_id,
            timestamp=datetime.now(),
            compliance_type=compliance_type,
            event_type=event_type,
            user_id=user_id,
            data_type=data_type,
            action=action,
            details=details,
            status="completed"
        )
        
        self.compliance_events.append(compliance_event)
        
        return event_id
    
    def generate_compliance_report(self, compliance_type: ComplianceType, 
                                 start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate compliance report for specific framework"""
        
        period_events = [
            event for event in self.compliance_events
            if event.compliance_type == compliance_type and
            start_date <= event.timestamp <= end_date
        ]
        
        # Analyze events by type
        event_counts = {}
        action_counts = {}
        
        for event in period_events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
            action_counts[event.action] = action_counts.get(event.action, 0) + 1
        
        # Calculate compliance metrics
        total_events = len(period_events)
        unique_users = len(set(event.user_id for event in period_events if event.user_id))
        
        # Check compliance requirements
        requirements = self.compliance_requirements[compliance_type]
        compliance_status = self._check_compliance_requirements(compliance_type, period_events)
        
        return {
            "compliance_type": compliance_type.value,
            "report_period": f"{start_date} to {end_date}",
            "total_events": total_events,
            "unique_users": unique_users,
            "event_type_breakdown": event_counts,
            "action_breakdown": action_counts,
            "requirements": requirements,
            "compliance_status": compliance_status,
            "recommendations": self._get_compliance_recommendations(compliance_type, period_events)
        }
    
    def _check_compliance_requirements(self, compliance_type: ComplianceType, 
                                     events: List[ComplianceEvent]) -> Dict[str, bool]:
        """Check compliance requirements"""
        
        status = {}
        
        if compliance_type == ComplianceType.GDPR:
            status["consent_management"] = any(e.event_type == "consent_recorded" for e in events)
            status["data_access"] = any(e.event_type == "access_request_processed" for e in events)
            status["data_deletion"] = any(e.event_type == "deletion_request_processed" for e in events)
            status["data_portability"] = any(e.event_type == "portability_request_processed" for e in events)
        
        elif compliance_type == ComplianceType.HIPAA:
            status["phi_handling"] = any(e.event_type == "phi_data_handled" for e in events)
            status["access_logging"] = any(e.event_type == "hipaa_access_logged" for e in events)
            status["breach_notification"] = True  # Assume no breaches in demo
        
        elif compliance_type == ComplianceType.PCI:
            status["payment_processing"] = any(e.event_type == "payment_data_processed" for e in events)
            status["data_encryption"] = True  # Assume encryption is implemented
            status["access_controls"] = True  # Assume access controls are in place
        
        return status
    
    def _get_compliance_recommendations(self, compliance_type: ComplianceType,
                                      events: List[ComplianceEvent]) -> List[str]:
        """Get compliance recommendations"""
        
        recommendations = []
        
        if compliance_type == ComplianceType.GDPR:
            consent_events = [e for e in events if e.event_type == "consent_recorded"]
            if len(consent_events) < 10:
                recommendations.append("Increase consent collection and management")
            
            access_events = [e for e in events if e.event_type == "access_request_processed"]
            if len(access_events) == 0:
                recommendations.append("Implement data subject access request handling")
        
        elif compliance_type == ComplianceType.HIPAA:
            phi_events = [e for e in events if e.event_type == "phi_data_handled"]
            if len(phi_events) < 5:
                recommendations.append("Review PHI data handling procedures")
            
            recommendations.append("Conduct regular HIPAA compliance audits")
        
        elif compliance_type == ComplianceType.PCI:
            payment_events = [e for e in events if e.event_type == "payment_data_processed"]
            if len(payment_events) < 3:
                recommendations.append("Review payment data processing procedures")
            
            recommendations.append("Conduct regular PCI DSS assessments")
        
        if not recommendations:
            recommendations.append("Compliance appears to be in good standing")
        
        return recommendations
    
    def _get_user_personal_data(self, user_id: str) -> Dict[str, Any]:
        """Get user's personal data"""
        return {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "voice_profile": "voice_profile_hash",
            "preferences": {
                "language": "en-US",
                "timezone": "UTC-5"
            }
        }
    
    def _get_processing_activities(self, user_id: str) -> List[Dict[str, Any]]:
        """Get data processing activities for user"""
        return [
            {
                "activity": "voice_recording",
                "purpose": "customer_service",
                "timestamp": datetime.now() - timedelta(days=1),
                "legal_basis": "consent"
            },
            {
                "activity": "transcript_analysis",
                "purpose": "service_improvement",
                "timestamp": datetime.now() - timedelta(days=2),
                "legal_basis": "legitimate_interest"
            }
        ]
    
    def _get_user_consent_records(self, user_id: str, compliance_type: ComplianceType) -> List[Dict[str, Any]]:
        """Get user's consent records"""
        return [
            consent_data for consent_data in self.consent_records.values()
            if consent_data["user_id"] == user_id and 
            consent_data["compliance_type"] == compliance_type.value
        ]
    
    def _get_user_voice_data(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's voice data"""
        return [
            {
                "recording_id": f"rec_{user_id}_001",
                "timestamp": datetime.now() - timedelta(days=1),
                "duration": 120,
                "purpose": "customer_service"
            }
        ]
    
    def _get_user_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's interaction history"""
        return [
            {
                "interaction_id": f"int_{user_id}_001",
                "timestamp": datetime.now() - timedelta(days=1),
                "type": "voice_call",
                "duration": 300,
                "outcome": "resolved"
            }
        ]

def simulate_compliance_scenarios():
    """Simulate various compliance scenarios"""
    
    print("Compliance Manager Demo")
    print("=" * 60)
    
    # Initialize compliance manager
    compliance = ComplianceManager()
    
    # Scenario 1: GDPR Consent Management
    print("\n1. GDPR Consent Management")
    print("-" * 30)
    
    user_id = "customer_001"
    
    # Record consent
    consent_id = compliance.record_consent(
        user_id, 
        "voice_recording", 
        True, 
        ComplianceType.GDPR
    )
    print(f"Consent recorded: {consent_id}")
    
    # Check consent
    has_consent = compliance.check_consent(user_id, "voice_recording", ComplianceType.GDPR)
    print(f"User has consent: {has_consent}")
    
    # Scenario 2: GDPR Data Subject Requests
    print("\n2. GDPR Data Subject Requests")
    print("-" * 30)
    
    # Access request
    access_result = compliance.process_gdpr_request(user_id, "access")
    print(f"Access request status: {access_result['compliance_status']}")
    
    # Portability request
    portability_result = compliance.process_gdpr_request(user_id, "portability")
    print(f"Portability request status: {portability_result['compliance_status']}")
    
    # Scenario 3: HIPAA PHI Handling
    print("\n3. HIPAA PHI Handling")
    print("-" * 30)
    
    patient_id = "patient_001"
    phi_data = "Patient has diabetes and requires insulin"
    
    hipaa_result = compliance.handle_hipaa_data(
        patient_id,
        "medical_condition",
        phi_data,
        "doctor_001",
        "treatment"
    )
    print(f"HIPAA data handling status: {hipaa_result['status']}")
    print(f"Compliance verified: {hipaa_result['compliance_verified']}")
    
    # Scenario 4: PCI Payment Processing
    print("\n4. PCI Payment Processing")
    print("-" * 30)
    
    transaction_id = "txn_001"
    payment_data = {
        "card_number": "4111111111111111",
        "expiry_date": "12/25",
        "cvv": "123",
        "amount": 99.99,
        "currency": "USD"
    }
    
    pci_result = compliance.handle_pci_data(transaction_id, payment_data, user_id)
    print(f"PCI payment processing status: {pci_result['status']}")
    print(f"Token generated: {pci_result['token'][:20]}...")
    
    # Scenario 5: Compliance Reports
    print("\n5. Compliance Reports")
    print("-" * 30)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=1)
    
    # GDPR Report
    gdpr_report = compliance.generate_compliance_report(ComplianceType.GDPR, start_date, end_date)
    print(f"GDPR Compliance Status:")
    for req, status in gdpr_report['compliance_status'].items():
        print(f"  {req}: {'✓' if status else '✗'}")
    
    # HIPAA Report
    hipaa_report = compliance.generate_compliance_report(ComplianceType.HIPAA, start_date, end_date)
    print(f"\nHIPAA Compliance Status:")
    for req, status in hipaa_report['compliance_status'].items():
        print(f"  {req}: {'✓' if status else '✗'}")
    
    # PCI Report
    pci_report = compliance.generate_compliance_report(ComplianceType.PCI, start_date, end_date)
    print(f"\nPCI Compliance Status:")
    for req, status in pci_report['compliance_status'].items():
        print(f"  {req}: {'✓' if status else '✗'}")
    
    # Scenario 6: Multi-Compliance Workflow
    print("\n6. Multi-Compliance Workflow")
    print("-" * 35)
    
    # Simulate a healthcare payment scenario
    patient_user_id = "patient_002"
    
    # Step 1: Record consent for both HIPAA and payment processing
    hipaa_consent = compliance.record_consent(patient_user_id, "medical_data", True, ComplianceType.HIPAA)
    payment_consent = compliance.record_consent(patient_user_id, "payment_processing", True, ComplianceType.PCI)
    
    print(f"HIPAA consent: {hipaa_consent}")
    print(f"Payment consent: {payment_consent}")
    
    # Step 2: Handle medical data
    medical_result = compliance.handle_hipaa_data(
        "patient_002",
        "appointment_booking",
        "Patient scheduled for diabetes consultation",
        "nurse_001",
        "treatment"
    )
    
    # Step 3: Process payment
    payment_result = compliance.handle_pci_data(
        "txn_002",
        {
            "card_number": "5555555555554444",
            "expiry_date": "06/26",
            "cvv": "456",
            "amount": 150.00,
            "currency": "USD"
        },
        patient_user_id
    )
    
    print(f"Medical data handling: {medical_result['status']}")
    print(f"Payment processing: {payment_result['status']}")
    
    print("\n" + "=" * 60)
    print("Compliance Manager Demo Complete")
    print("=" * 60)
    
    return compliance

if __name__ == "__main__":
    compliance_manager = simulate_compliance_scenarios()
