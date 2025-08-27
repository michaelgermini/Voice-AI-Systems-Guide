#!/usr/bin/env python3
"""
Chapter 2 - Natural Language Processing in Call Centers
Entity Extraction Demo
"""

import re
import time
from dataclasses import dataclass
from typing import List

@dataclass
class Entity:
    entity_type: str
    value: str
    confidence: float
    start_pos: int
    end_pos: int

class EntityExtractor:
    """Extract entities from customer input"""
    
    def __init__(self):
        self.entity_patterns = {
            "order_number": r"\b\d{5,10}\b",
            "phone_number": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "amount": r"\$\d+(?:\.\d{2})?",
            "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            "account_number": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "zip_code": r"\b\d{5}(?:-\d{4})?\b"
        }
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from text"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                entity = Entity(
                    entity_type=entity_type,
                    value=match.group(),
                    confidence=0.9,
                    start_pos=match.start(),
                    end_pos=match.end()
                )
                entities.append(entity)
        
        return entities

def demo_entity_extraction():
    """Demonstrate entity extraction capabilities"""
    
    print("=" * 60)
    print("ENTITY EXTRACTION DEMO")
    print("=" * 60)
    
    # Initialize entity extractor
    entity_extractor = EntityExtractor()
    
    # Test cases with various entity types
    test_cases = [
        "My order number is 12345 and I need to track it",
        "Please call me at 555-123-4567 or email john@example.com",
        "I want to pay $150.00 for my account ending in 1234-5678-9012-3456",
        "My appointment is on 12/15/2024 and my zip code is 90210",
        "The amount is $99.99 and my phone is 555.123.4567",
        "No entities in this plain text message",
        "Multiple amounts: $50, $100, and $200 with dates 01/01/2024 and 02/15/2024"
    ]
    
    print("\nTesting Entity Extraction:")
    print("-" * 40)
    
    total_entities = 0
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        
        # Simulate processing time
        time.sleep(0.3)
        
        # Extract entities
        entities = entity_extractor.extract_entities(test_input)
        
        if entities:
            print(f"  Found {len(entities)} entities:")
            for entity in entities:
                print(f"    - {entity.entity_type}: '{entity.value}' (confidence: {entity.confidence:.2f})")
            total_entities += len(entities)
            print("  Status: [SUCCESS] Entities Found")
        else:
            print("  Status: [FAILED] No Entities Found")
    
    print("\n" + "=" * 60)
    print("DEMO SUMMARY")
    print("=" * 60)
    
    print(f"Total Test Cases: {len(test_cases)}")
    print(f"Total Entities Extracted: {total_entities}")
    print(f"Average Entities per Test: {total_entities/len(test_cases):.1f}")
    
    print("\nSupported Entity Types:")
    for entity_type in entity_extractor.entity_patterns.keys():
        print(f"  - {entity_type}")
    
    print("\nEntity Patterns:")
    for entity_type, pattern in entity_extractor.entity_patterns.items():
        print(f"  - {entity_type}: {pattern}")
    
    print("\nDemo completed successfully! [SUCCESS]")

if __name__ == "__main__":
    demo_entity_extraction()
