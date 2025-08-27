# Chapter 5: Modern IVR Script Examples

## 5.1 Introduction

Modern call centers are moving beyond rigid menu-based IVRs toward **AI-powered, dynamic conversational flows**. This chapter provides **real-world examples** of IVR scripts that combine **TTS + NLP + Telephony**, ready for developers and integrators.

The examples in this chapter demonstrate:
- **Natural Language Processing** for intent recognition
- **Text-to-Speech** with SSML for natural responses
- **Telephony Integration** with major platforms
- **Business Logic** integration with backend systems
- **Error Handling** and graceful fallbacks

---

## 5.2 Example 1 – E-commerce Order Tracking

**Scenario:** Customer wants to check their order status.

**Flow:**  
1. Greeting → "Welcome to ShopEasy. How can I assist you today?"  
2. Customer → "I want to track my order."  
3. NLP identifies intent `CheckOrderStatus`.  
4. AI asks for the order number → "Please provide your order number."  
5. Customer → "55421."  
6. Backend query retrieves order info.  
7. TTS response → "Order 55421 was shipped yesterday and will arrive tomorrow."  
8. Closing → "Is there anything else I can help you with?"

**Key Features:**
- Natural language understanding
- Order number validation
- Real-time backend integration
- Confirmation and closing

**Twilio + Python Example:**

```python
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Welcome to ShopEasy. How can I assist you today?", voice="Polly.Joanna")
    # Here you would integrate NLP and backend logic
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(port=5000)
```

---

## 5.3 Example 2 – Appointment Booking (Healthcare)

**Scenario:** Patient wants to schedule an appointment.

**Flow:**  
1. Greeting → "Hello, this is CityCare. How can I help you today?"  
2. Customer → "I want to book an appointment with Dr. Smith."  
3. NLP intent → `BookAppointment`, entity → `DoctorName=Smith`.  
4. AI checks schedule → "Dr. Smith is available Thursday at 10 AM. Does that work?"  
5. Customer confirms → TTS → "Your appointment with Dr. Smith is confirmed for Thursday at 10 AM."

**Key Points:**  
- Short prompts  
- Confirmation of critical info (doctor, date, time)  
- Escalation if schedule unavailable → human operator
- HIPAA compliance considerations

**Features:**
- Doctor name recognition
- Schedule availability checking
- Appointment confirmation
- Calendar integration

---

## 5.4 Example 3 – Payment Collection

**Scenario:** Customer calls to pay an outstanding invoice.

**Flow:**  
1. Greeting → "Welcome to FinBank automated service."  
2. Customer → "I want to pay my bill."  
3. NLP intent → `MakePayment`  
4. AI → "Please provide your account number."  
5. Customer provides info → Backend verifies balance  
6. TTS → "Your payment of $120 has been successfully processed."  
7. Closing → "Thank you for using FinBank. Have a great day!"

**Notes:**  
- Always confirm amounts and account info  
- Use SSML for natural pauses in TTS  
- Include fallback for payment errors
- PCI compliance for payment processing

**Security Features:**
- Account number validation
- Payment amount confirmation
- Transaction logging
- Fraud detection integration

---

## 5.5 Example 4 – Technical Support

**Scenario:** Customer needs help with a technical issue.

**Flow:**
1. Greeting → "Welcome to TechSupport. How can I help you today?"
2. Customer → "My internet is not working."
3. NLP intent → `TechnicalSupport`, entity → `IssueType=Internet`
4. AI → "I understand you're having internet issues. Let me help you troubleshoot."
5. AI guides through diagnostic steps
6. If resolved → "Great! Your internet should be working now."
7. If not resolved → "Let me connect you with a technician."

**Features:**
- Issue classification
- Step-by-step troubleshooting
- Escalation to human agents
- Knowledge base integration

---

## 5.6 Example 5 – Banking Balance Inquiry

**Scenario:** Customer wants to check account balance.

**Flow:**
1. Greeting → "Welcome to SecureBank. How can I help you today?"
2. Customer → "I want to check my balance."
3. NLP intent → `CheckBalance`
4. AI → "For security, I'll need to verify your identity. What's your account number?"
5. Customer provides account number
6. AI → "Did you say account number 1-2-3-4-5-6-7-8?"
7. Customer confirms
8. AI → "Your current balance is $2,456.78."
9. Closing → "Is there anything else I can help you with?"

**Security Features:**
- Multi-factor authentication
- Account number confirmation
- Session management
- Fraud detection

---

## 5.7 Best Practices Illustrated in Scripts

### 1. Use Natural Language
❌ "Press 1 for billing, press 2 for support..."  
✅ "How can I help you today?"

### 2. Confirm Key Data
- Order numbers, appointment times, payment amounts
- Account numbers, personal information
- Critical business data

### 3. Short & Clear Prompts
- Keep responses under 10 seconds
- Use simple, direct language
- Avoid overwhelming with options

### 4. Error Handling
- Reprompt for unclear input
- Provide helpful examples
- Escalate to human agents when needed

### 5. Personalization
- Use customer name when available
- Reference previous interactions
- Adapt tone based on context

### 6. Multilingual Support
- Detect customer language preference
- Provide TTS in multiple languages
- Support regional accents and dialects

---

## 5.8 Technical Implementation Patterns

### A. Intent Recognition Pattern
```python
def classify_intent(utterance: str) -> Dict:
    """Classify customer intent from utterance"""
    utterance_lower = utterance.lower()
    
    if any(word in utterance_lower for word in ["track", "order", "status"]):
        return {"intent": "CheckOrderStatus", "confidence": 0.95}
    elif any(word in utterance_lower for word in ["book", "appointment", "schedule"]):
        return {"intent": "BookAppointment", "confidence": 0.92}
    elif any(word in utterance_lower for word in ["pay", "payment", "bill"]):
        return {"intent": "MakePayment", "confidence": 0.89}
    else:
        return {"intent": "Unknown", "confidence": 0.45}
```

### B. Entity Extraction Pattern
```python
def extract_entities(utterance: str) -> Dict:
    """Extract entities from customer utterance"""
    entities = {}
    
    # Extract order numbers
    order_pattern = r'\b(\d{5,})\b'
    orders = re.findall(order_pattern, utterance)
    if orders:
        entities["order_number"] = orders[0]
    
    # Extract doctor names
    doctor_pattern = r'Dr\.\s+(\w+)'
    doctors = re.findall(doctor_pattern, utterance)
    if doctors:
        entities["doctor_name"] = doctors[0]
    
    # Extract amounts
    amount_pattern = r'\$(\d+(?:\.\d{2})?)'
    amounts = re.findall(amount_pattern, utterance)
    if amounts:
        entities["amount"] = float(amounts[0])
    
    return entities
```

### C. SSML Response Pattern
```python
def generate_ssml_response(text: str, add_pauses: bool = True) -> str:
    """Generate SSML with natural pacing"""
    ssml = text
    
    if add_pauses:
        # Add pauses for natural pacing
        ssml = re.sub(r'([.!?])\s+', r'\1 <break time="300ms"/> ', ssml)
        
        # Add pauses before important information
        ssml = re.sub(r'(\$[\d,]+\.?\d*)', r'<break time="400ms"/> \1', ssml)
    
    return f'<speak>{ssml}</speak>'
```

---

## 5.9 Platform-Specific Implementations

### A. Twilio Implementation
```python
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def handle_call():
    resp = VoiceResponse()
    
    # Get customer input
    speech_result = request.values.get('SpeechResult', '')
    
    # Process with NLP
    intent = classify_intent(speech_result)
    
    if intent["intent"] == "CheckOrderStatus":
        resp.say("Please provide your order number.", voice="Polly.Joanna")
        resp.gather(input="speech", action="/process_order", method="POST")
    else:
        resp.say("I didn't understand. Please try again.", voice="Polly.Joanna")
        resp.gather(input="speech", action="/webhook", method="POST")
    
    return str(resp)
```

### B. Amazon Connect Implementation
```json
{
  "Type": "GetCustomerInput",
  "Parameters": {
    "Text": "Welcome to our service. How can I help you today?",
    "TimeoutSeconds": 10,
    "MaxDigits": 0,
    "TextToSpeechParameters": {
      "VoiceId": "Joanna",
      "Engine": "neural"
    }
  },
  "NextAction": "ProcessIntent"
}
```

### C. Asterisk Implementation
```asterisk
[main-menu]
exten => s,1,Answer()
exten => s,n,Wait(1)
exten => s,n,Playback(welcome)
exten => s,n,Read(customer_input,beep,3)
exten => s,n,Set(intent=${SHELL(python3 /path/to/nlp.py ${customer_input})})
exten => s,n,GotoIf($[${intent}="order"]?order-tracking:main-menu)
exten => s,n,Hangup()

[order-tracking]
exten => s,1,Playback(please-provide-order)
exten => s,n,Read(order_number,beep,5)
exten => s,n,Set(order_info=${SHELL(python3 /path/to/order_lookup.py ${order_number})})
exten => s,n,Playback(order-info)
exten => s,n,Hangup()
```

---

## 5.10 Error Handling and Fallbacks

### A. Low Confidence Handling
```python
def handle_low_confidence(intent: Dict, utterance: str) -> str:
    """Handle cases where intent confidence is low"""
    if intent["confidence"] < 0.7:
        return f"I think you said '{utterance}', but I'm not completely sure. " \
               f"Could you please clarify what you need help with?"
    return None
```

### B. Escalation Pattern
```python
def escalate_to_human(reason: str) -> str:
    """Escalate call to human agent"""
    return f"I understand this is important. Let me connect you with a " \
           f"specialist who can better assist you. Please hold."
```

### C. Retry Pattern
```python
def retry_prompt(attempt: int, max_attempts: int = 3) -> str:
    """Generate retry prompt with increasing clarity"""
    if attempt == 1:
        return "I didn't catch that. Could you please repeat?"
    elif attempt == 2:
        return "I'm still having trouble understanding. You can say things like " \
               "'check my order', 'make a payment', or 'speak to an agent'."
    else:
        return "Let me connect you with a human agent who can help."
```

---

## 5.11 Performance Optimization

### A. Response Time Optimization
- Cache frequently used responses
- Pre-generate common SSML
- Use async processing for backend calls
- Optimize NLP model inference

### B. Accuracy Improvement
- Train on domain-specific data
- Use context from previous turns
- Implement confidence thresholds
- Regular model retraining

### C. Scalability Considerations
- Load balancing across instances
- Database connection pooling
- CDN for static assets
- Monitoring and alerting

---

## 5.12 Testing and Quality Assurance

### A. Unit Testing
```python
def test_intent_classification():
    """Test intent classification accuracy"""
    test_cases = [
        ("I want to track my order", "CheckOrderStatus"),
        ("I need to pay my bill", "MakePayment"),
        ("Book an appointment", "BookAppointment")
    ]
    
    for utterance, expected_intent in test_cases:
        result = classify_intent(utterance)
        assert result["intent"] == expected_intent
```

### B. Integration Testing
- End-to-end call flow testing
- Backend system integration
- Performance under load
- Error scenario testing

### C. User Acceptance Testing
- Real user feedback collection
- A/B testing of different flows
- Satisfaction score monitoring
- Call completion rate tracking

---

## 5.13 Summary

- Modern IVRs leverage **AI + TTS + NLP** for natural conversations.  
- Scripts must combine **clarity, confirmation, and fallback mechanisms**.  
- Real-world examples demonstrate flexibility across industries: e-commerce, healthcare, finance.  
- Developers can implement these flows using **Twilio, Asterisk, Amazon Connect, or Genesys**.
- **Error handling** and **escalation** are critical for user satisfaction.
- **Performance optimization** and **testing** ensure reliable operation.

---

## 🛠️ Practical Examples

- [E-commerce Order Tracking](./examples/ecommerce_order_tracking.py) - Complete order tracking implementation
- [Healthcare Appointment Booking](./examples/healthcare_appointment.py) - Medical appointment scheduling
- [Payment Collection System](./examples/payment_collection.py) - Secure payment processing
- [Technical Support Flow](./examples/technical_support.py) - IT support automation
- [Banking Balance Inquiry](./examples/banking_balance.py) - Financial services integration

## 📚 Next Steps

✅ This closes Chapter 5.

Chapter 6 will cover advanced voice AI features including emotion detection, speaker identification, and multilingual support for global call centers.
