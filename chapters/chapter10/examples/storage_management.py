#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Example: Storage Management

This example demonstrates storage management strategies for voice AI services,
including hot/warm/cold storage tiers and session state management.
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
class CallData:
    call_id: str
    user_id: str
    session_id: str
    audio_data: bytes
    transcript: str
    intent: str
    response: str
    metadata: Dict[str, Any]
    created_at: datetime
    accessed_at: datetime
    size_bytes: int

@dataclass
class StorageTier:
    name: str
    type: str  # "hot", "warm", "cold"
    latency_ms: float
    cost_per_gb_month: float
    retention_days: int
    max_size_gb: float
    current_usage_gb: float

@dataclass
class StorageMetrics:
    total_calls_stored: int
    total_size_gb: float
    calls_per_tier: Dict[str, int]
    size_per_tier: Dict[str, float]
    average_latency_ms: float
    cost_per_month: float
    timestamp: datetime

class HotStorage:
    """Redis-like in-memory storage for active sessions and recent calls"""
    
    def __init__(self, max_size_gb: float = 10.0):
        self.max_size_gb = max_size_gb
        self.current_usage_gb = 0.0
        self.data = {}
        self.access_times = {}
        self.max_retention_hours = 24
        
    async def store(self, key: str, data: CallData) -> bool:
        """Store data in hot storage"""
        data_size_gb = data.size_bytes / (1024**3)
        
        # Check if we have space
        if self.current_usage_gb + data_size_gb > self.max_size_gb:
            # Evict least recently used data
            await self._evict_lru_data(data_size_gb)
        
        if self.current_usage_gb + data_size_gb <= self.max_size_gb:
            self.data[key] = data
            self.access_times[key] = datetime.utcnow()
            self.current_usage_gb += data_size_gb
            return True
        return False
    
    async def retrieve(self, key: str) -> Optional[CallData]:
        """Retrieve data from hot storage"""
        if key in self.data:
            data = self.data[key]
            self.access_times[key] = datetime.utcnow()
            data.accessed_at = datetime.utcnow()
            return data
        return None
    
    async def _evict_lru_data(self, required_space_gb: float):
        """Evict least recently used data"""
        # Sort by access time (oldest first)
        sorted_keys = sorted(self.access_times.keys(), 
                           key=lambda k: self.access_times[k])
        
        freed_space = 0.0
        for key in sorted_keys:
            if freed_space >= required_space_gb:
                break
            
            data = self.data[key]
            data_size_gb = data.size_bytes / (1024**3)
            
            del self.data[key]
            del self.access_times[key]
            self.current_usage_gb -= data_size_gb
            freed_space += data_size_gb
    
    def cleanup_expired_data(self):
        """Remove data older than retention period"""
        cutoff_time = datetime.utcnow() - timedelta(hours=self.max_retention_hours)
        expired_keys = [
            key for key, access_time in self.access_times.items()
            if access_time < cutoff_time
        ]
        
        for key in expired_keys:
            data = self.data[key]
            data_size_gb = data.size_bytes / (1024**3)
            del self.data[key]
            del self.access_times[key]
            self.current_usage_gb -= data_size_gb
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get storage metrics"""
        self.cleanup_expired_data()
        return {
            "type": "hot",
            "current_usage_gb": round(self.current_usage_gb, 2),
            "max_size_gb": self.max_size_gb,
            "utilization_percent": round((self.current_usage_gb / self.max_size_gb) * 100, 1),
            "items_count": len(self.data),
            "latency_ms": 1.0
        }

class WarmStorage:
    """PostgreSQL-like storage for recent calls and analytics"""
    
    def __init__(self, max_size_gb: float = 100.0):
        self.max_size_gb = max_size_gb
        self.current_usage_gb = 0.0
        self.data = {}
        self.indexes = {}
        self.max_retention_days = 30
        
    async def store(self, key: str, data: CallData) -> bool:
        """Store data in warm storage"""
        data_size_gb = data.size_bytes / (1024**3)
        
        if self.current_usage_gb + data_size_gb <= self.max_size_gb:
            self.data[key] = data
            
            # Create indexes for common queries
            if data.user_id not in self.indexes:
                self.indexes[data.user_id] = []
            self.indexes[data.user_id].append(key)
            
            if data.intent not in self.indexes:
                self.indexes[data.intent] = []
            self.indexes[data.intent].append(key)
            
            self.current_usage_gb += data_size_gb
            return True
        return False
    
    async def retrieve(self, key: str) -> Optional[CallData]:
        """Retrieve data from warm storage"""
        if key in self.data:
            data = self.data[key]
            data.accessed_at = datetime.utcnow()
            return data
        return None
    
    async def query_by_user(self, user_id: str) -> List[CallData]:
        """Query calls by user ID"""
        if user_id in self.indexes:
            return [self.data[key] for key in self.indexes[user_id] if key in self.data]
        return []
    
    async def query_by_intent(self, intent: str) -> List[CallData]:
        """Query calls by intent"""
        if intent in self.indexes:
            return [self.data[key] for key in self.indexes[intent] if key in self.data]
        return []
    
    def cleanup_expired_data(self):
        """Remove data older than retention period"""
        cutoff_time = datetime.utcnow() - timedelta(days=self.max_retention_days)
        expired_keys = [
            key for key, data in self.data.items()
            if data.created_at < cutoff_time
        ]
        
        for key in expired_keys:
            data = self.data[key]
            data_size_gb = data.size_bytes / (1024**3)
            del self.data[key]
            self.current_usage_gb -= data_size_gb
            
            # Clean up indexes
            for index_list in self.indexes.values():
                if key in index_list:
                    index_list.remove(key)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get storage metrics"""
        self.cleanup_expired_data()
        return {
            "type": "warm",
            "current_usage_gb": round(self.current_usage_gb, 2),
            "max_size_gb": self.max_size_gb,
            "utilization_percent": round((self.current_usage_gb / self.max_size_gb) * 100, 1),
            "items_count": len(self.data),
            "latency_ms": 10.0
        }

class ColdStorage:
    """S3-like storage for long-term retention and compliance"""
    
    def __init__(self, max_size_gb: float = 1000.0):
        self.max_size_gb = max_size_gb
        self.current_usage_gb = 0.0
        self.data = {}
        self.metadata_index = {}
        self.max_retention_days = 365 * 7  # 7 years
        
    async def store(self, key: str, data: CallData) -> bool:
        """Store data in cold storage"""
        data_size_gb = data.size_bytes / (1024**3)
        
        if self.current_usage_gb + data_size_gb <= self.max_size_gb:
            # Compress data for cold storage
            compressed_data = self._compress_data(data)
            self.data[key] = compressed_data
            
            # Store metadata for search
            self.metadata_index[key] = {
                "call_id": data.call_id,
                "user_id": data.user_id,
                "intent": data.intent,
                "created_at": data.created_at.isoformat(),
                "size_bytes": data.size_bytes,
                "compressed_size_bytes": len(compressed_data)
            }
            
            self.current_usage_gb += data_size_gb
            return True
        return False
    
    async def retrieve(self, key: str) -> Optional[CallData]:
        """Retrieve data from cold storage"""
        if key in self.data:
            compressed_data = self.data[key]
            # Simulate decompression delay
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Decompress data
            data = self._decompress_data(compressed_data)
            data.accessed_at = datetime.utcnow()
            return data
        return None
    
    def _compress_data(self, data: CallData) -> bytes:
        """Simulate data compression"""
        # In real implementation, this would use actual compression
        data_dict = asdict(data)
        data_dict["compressed"] = True
        return json.dumps(data_dict).encode()
    
    def _decompress_data(self, compressed_data: bytes) -> CallData:
        """Simulate data decompression"""
        # In real implementation, this would use actual decompression
        data_dict = json.loads(compressed_data.decode())
        data_dict.pop("compressed", None)
        
        # Reconstruct CallData object
        data_dict["created_at"] = datetime.fromisoformat(data_dict["created_at"])
        data_dict["accessed_at"] = datetime.fromisoformat(data_dict["accessed_at"])
        
        return CallData(**data_dict)
    
    async def search_metadata(self, filters: Dict[str, Any]) -> List[str]:
        """Search metadata for matching keys"""
        matching_keys = []
        
        for key, metadata in self.metadata_index.items():
            matches = True
            
            for filter_key, filter_value in filters.items():
                if filter_key in metadata:
                    if isinstance(filter_value, str):
                        if filter_value.lower() not in str(metadata[filter_key]).lower():
                            matches = False
                            break
                    elif metadata[filter_key] != filter_value:
                        matches = False
                        break
                else:
                    matches = False
                    break
            
            if matches:
                matching_keys.append(key)
        
        return matching_keys
    
    def cleanup_expired_data(self):
        """Remove data older than retention period"""
        cutoff_time = datetime.utcnow() - timedelta(days=self.max_retention_days)
        expired_keys = [
            key for key, metadata in self.metadata_index.items()
            if datetime.fromisoformat(metadata["created_at"]) < cutoff_time
        ]
        
        for key in expired_keys:
            metadata = self.metadata_index[key]
            data_size_gb = metadata["size_bytes"] / (1024**3)
            del self.data[key]
            del self.metadata_index[key]
            self.current_usage_gb -= data_size_gb
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get storage metrics"""
        self.cleanup_expired_data()
        return {
            "type": "cold",
            "current_usage_gb": round(self.current_usage_gb, 2),
            "max_size_gb": self.max_size_gb,
            "utilization_percent": round((self.current_usage_gb / self.max_size_gb) * 100, 1),
            "items_count": len(self.data),
            "latency_ms": 500.0
        }

class DistributedSessionManager:
    """Manages session state across multiple storage tiers"""
    
    def __init__(self):
        self.hot_storage = HotStorage()
        self.warm_storage = WarmStorage()
        self.cold_storage = ColdStorage()
        self.session_cache = {}
        self.session_timeout = 3600  # 1 hour
        
    async def store_call_data(self, call_data: CallData, tier: str = "auto") -> bool:
        """Store call data in appropriate tier"""
        if tier == "auto":
            tier = self._determine_storage_tier(call_data)
        
        success = False
        
        if tier == "hot":
            success = await self.hot_storage.store(call_data.call_id, call_data)
        elif tier == "warm":
            success = await self.warm_storage.store(call_data.call_id, call_data)
        elif tier == "cold":
            success = await self.cold_storage.store(call_data.call_id, call_data)
        
        return success
    
    async def retrieve_call_data(self, call_id: str) -> Optional[CallData]:
        """Retrieve call data from appropriate tier"""
        # Try hot storage first
        data = await self.hot_storage.retrieve(call_id)
        if data:
            return data
        
        # Try warm storage
        data = await self.warm_storage.retrieve(call_id)
        if data:
            # Move to hot storage for faster future access
            await self.hot_storage.store(call_id, data)
            return data
        
        # Try cold storage
        data = await self.cold_storage.retrieve(call_id)
        if data:
            # Move to warm storage
            await self.warm_storage.store(call_id, data)
            return data
        
        return None
    
    def _determine_storage_tier(self, call_data: CallData) -> str:
        """Determine appropriate storage tier based on data characteristics"""
        age_hours = (datetime.utcnow() - call_data.created_at).total_seconds() / 3600
        
        if age_hours < 24:
            return "hot"
        elif age_hours < 30 * 24:  # 30 days
            return "warm"
        else:
            return "cold"
    
    async def create_session(self, session_id: str, user_id: str) -> Dict[str, Any]:
        """Create a new session"""
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "context": {},
            "conversation_history": []
        }
        
        self.session_cache[session_id] = session
        return session
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session = self.session_cache.get(session_id)
        if session and datetime.utcnow() - session["last_activity"] < timedelta(seconds=self.session_timeout):
            session["last_activity"] = datetime.utcnow()
            return session
        return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        if session_id in self.session_cache:
            self.session_cache[session_id].update(updates)
            self.session_cache[session_id]["last_activity"] = datetime.utcnow()
    
    def get_storage_metrics(self) -> StorageMetrics:
        """Get comprehensive storage metrics"""
        hot_metrics = self.hot_storage.get_metrics()
        warm_metrics = self.warm_storage.get_metrics()
        cold_metrics = self.cold_storage.get_metrics()
        
        total_calls = hot_metrics["items_count"] + warm_metrics["items_count"] + cold_metrics["items_count"]
        total_size = hot_metrics["current_usage_gb"] + warm_metrics["current_usage_gb"] + cold_metrics["current_usage_gb"]
        
        # Calculate average latency
        total_latency = (hot_metrics["latency_ms"] * hot_metrics["items_count"] +
                        warm_metrics["latency_ms"] * warm_metrics["items_count"] +
                        cold_metrics["latency_ms"] * cold_metrics["items_count"])
        
        avg_latency = total_latency / total_calls if total_calls > 0 else 0
        
        # Calculate monthly cost
        monthly_cost = (hot_metrics["current_usage_gb"] * 0.50 +  # $0.50/GB/month for hot
                       warm_metrics["current_usage_gb"] * 0.10 +  # $0.10/GB/month for warm
                       cold_metrics["current_usage_gb"] * 0.02)   # $0.02/GB/month for cold
        
        return StorageMetrics(
            total_calls_stored=total_calls,
            total_size_gb=total_size,
            calls_per_tier={
                "hot": hot_metrics["items_count"],
                "warm": warm_metrics["items_count"],
                "cold": cold_metrics["items_count"]
            },
            size_per_tier={
                "hot": hot_metrics["current_usage_gb"],
                "warm": warm_metrics["current_usage_gb"],
                "cold": cold_metrics["current_usage_gb"]
            },
            average_latency_ms=avg_latency,
            cost_per_month=monthly_cost,
            timestamp=datetime.utcnow()
        )

async def simulate_storage_management_demo():
    """Demonstrate storage management capabilities"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Example: Storage Management")
    print("=" * 60)
    
    # Initialize storage manager
    storage_manager = DistributedSessionManager()
    
    print("\n1. Storage Tiers Configuration:")
    print("   Hot Storage (Redis-like):")
    print("     - Latency: ~1ms")
    print("     - Cost: $0.50/GB/month")
    print("     - Retention: 24 hours")
    print("     - Use case: Active sessions, recent calls")
    
    print("\n   Warm Storage (PostgreSQL-like):")
    print("     - Latency: ~10ms")
    print("     - Cost: $0.10/GB/month")
    print("     - Retention: 30 days")
    print("     - Use case: Analytics, recent history")
    
    print("\n   Cold Storage (S3-like):")
    print("     - Latency: ~500ms")
    print("     - Cost: $0.02/GB/month")
    print("     - Retention: 7 years")
    print("     - Use case: Compliance, long-term retention")
    
    print("\n2. Storage Simulation:")
    print("   Storing 100 call records across different tiers...")
    
    # Generate sample call data
    call_data_list = []
    for i in range(100):
        # Vary the age of calls
        if i < 20:
            # Recent calls (hot storage)
            age_hours = random.uniform(0, 24)
        elif i < 60:
            # Recent history (warm storage)
            age_hours = random.uniform(24, 30 * 24)
        else:
            # Old calls (cold storage)
            age_hours = random.uniform(30 * 24, 365 * 24)
        
        created_at = datetime.utcnow() - timedelta(hours=age_hours)
        
        call_data = CallData(
            call_id=f"call-{uuid.uuid4().hex[:8]}",
            user_id=f"user-{random.randint(1, 50)}",
            session_id=f"session-{uuid.uuid4().hex[:8]}",
            audio_data=b"simulated_audio_data" * random.randint(10, 100),
            transcript=f"User said something about {random.choice(['order', 'billing', 'support', 'account'])}",
            intent=random.choice(['order_support', 'billing_question', 'technical_support', 'account_inquiry']),
            response=f"AI responded with helpful information about {random.choice(['order', 'billing', 'support', 'account'])}",
            metadata={
                "duration_seconds": random.uniform(30, 300),
                "language": "en-US",
                "confidence": random.uniform(0.8, 0.98)
            },
            created_at=created_at,
            accessed_at=created_at,
            size_bytes=random.randint(1024, 10240)  # 1KB to 10KB
        )
        
        call_data_list.append(call_data)
    
    # Store call data
    storage_results = []
    for call_data in call_data_list:
        tier = storage_manager._determine_storage_tier(call_data)
        success = await storage_manager.store_call_data(call_data, tier)
        storage_results.append((call_data.call_id, tier, success))
    
    print(f"   Stored {len([r for r in storage_results if r[2]])} calls successfully")
    
    print("\n3. Retrieval Performance Test:")
    print("   Testing retrieval from different tiers...")
    
    # Test retrieval performance
    retrieval_times = []
    for call_data in call_data_list[:10]:  # Test first 10 calls
        start_time = time.time()
        retrieved_data = await storage_manager.retrieve_call_data(call_data.call_id)
        retrieval_time = (time.time() - start_time) * 1000
        retrieval_times.append(retrieval_time)
        
        if retrieved_data:
            print(f"     Retrieved {call_data.call_id}: {retrieval_time:.1f}ms")
        else:
            print(f"     Failed to retrieve {call_data.call_id}")
    
    avg_retrieval_time = sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0
    
    print("\n4. Storage Metrics:")
    metrics = storage_manager.get_storage_metrics()
    
    print(f"   Total Calls Stored: {metrics.total_calls_stored}")
    print(f"   Total Size: {metrics.total_size_gb:.2f} GB")
    print(f"   Average Retrieval Latency: {metrics.average_latency_ms:.1f}ms")
    print(f"   Monthly Storage Cost: ${metrics.cost_per_month:.2f}")
    
    print("\n   Calls per Tier:")
    for tier, count in metrics.calls_per_tier.items():
        print(f"     {tier.capitalize()}: {count} calls")
    
    print("\n   Size per Tier:")
    for tier, size in metrics.size_per_tier.items():
        print(f"     {tier.capitalize()}: {size:.2f} GB")
    
    print("\n5. Session Management Test:")
    print("   Testing session persistence...")
    
    # Create and manage sessions
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    session = await storage_manager.create_session(session_id, "user-123")
    print(f"   Created session: {session_id}")
    
    # Update session
    await storage_manager.update_session(session_id, {
        "conversation_history": [
            {"role": "user", "text": "Hello", "timestamp": datetime.utcnow().isoformat()},
            {"role": "assistant", "text": "How can I help you?", "timestamp": datetime.utcnow().isoformat()}
        ]
    })
    
    # Retrieve session
    retrieved_session = await storage_manager.get_session(session_id)
    if retrieved_session:
        print(f"   Retrieved session with {len(retrieved_session['conversation_history'])} messages")
    
    print("\n6. Storage Management Benefits:")
    print("   ✓ Cost optimization through tiered storage")
    print("   ✓ Performance optimization for active data")
    print("   ✓ Compliance with long-term retention requirements")
    print("   ✓ Automatic data lifecycle management")
    print("   ✓ Session persistence across storage tiers")
    print("   ✓ Scalable storage architecture")
    
    return storage_manager

if __name__ == "__main__":
    asyncio.run(simulate_storage_management_demo())
