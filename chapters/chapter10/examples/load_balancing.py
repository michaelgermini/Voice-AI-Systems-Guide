#!/usr/bin/env python3
"""
Chapter 9 - Scalability and Cloud-Native Voice Architectures
Example: Load Balancing

This example demonstrates load balancing strategies for voice AI services,
including global load balancing, session persistence, and failover mechanisms.
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
class Region:
    region_id: str
    name: str
    location: str
    latency_ms: float
    capacity: int
    current_load: int
    health_status: str  # "healthy", "degraded", "unhealthy"
    last_health_check: datetime

@dataclass
class Instance:
    instance_id: str
    region_id: str
    ip_address: str
    port: int
    health_status: str
    current_connections: int
    max_connections: int
    cpu_utilization: float
    memory_utilization: float
    last_health_check: datetime

@dataclass
class CallRequest:
    call_id: str
    user_id: str
    user_location: str
    audio_data: bytes
    session_id: Optional[str] = None
    timestamp: datetime = None

@dataclass
class LoadBalancerMetrics:
    total_requests: int
    requests_per_region: Dict[str, int]
    average_latency_ms: float
    error_rate: float
    active_sessions: int
    timestamp: datetime

class HealthChecker:
    """Monitors health of regions and instances"""
    
    def __init__(self):
        self.health_check_interval = 30  # seconds
        self.last_health_checks = {}
    
    async def check_region_health(self, region: Region) -> bool:
        """Simulate health check for a region"""
        # Simulate network latency and health check
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Simulate health status based on current load and random factors
        health_score = 1.0
        
        # Reduce health if overloaded
        if region.current_load > region.capacity * 0.9:
            health_score -= 0.3
        
        # Add some randomness
        health_score += random.uniform(-0.1, 0.1)
        
        # Update region health
        if health_score > 0.8:
            region.health_status = "healthy"
        elif health_score > 0.5:
            region.health_status = "degraded"
        else:
            region.health_status = "unhealthy"
        
        region.last_health_check = datetime.utcnow()
        return region.health_status != "unhealthy"
    
    async def check_instance_health(self, instance: Instance) -> bool:
        """Simulate health check for an instance"""
        await asyncio.sleep(random.uniform(0.05, 0.2))
        
        # Simulate health based on resource utilization
        health_score = 1.0
        
        if instance.cpu_utilization > 90:
            health_score -= 0.4
        elif instance.cpu_utilization > 80:
            health_score -= 0.2
        
        if instance.memory_utilization > 90:
            health_score -= 0.3
        elif instance.memory_utilization > 80:
            health_score -= 0.1
        
        # Add randomness
        health_score += random.uniform(-0.05, 0.05)
        
        # Update instance health
        if health_score > 0.8:
            instance.health_status = "healthy"
        elif health_score > 0.5:
            instance.health_status = "degraded"
        else:
            instance.health_status = "unhealthy"
        
        instance.last_health_check = datetime.utcnow()
        return instance.health_status != "unhealthy"

class SessionManager:
    """Manages session persistence across load balancers"""
    
    def __init__(self):
        self.sessions = {}
        self.session_timeout = 3600  # 1 hour
        self.sticky_session_enabled = True
    
    def create_session(self, call_id: str, user_id: str, instance_id: str) -> str:
        """Create a new session and bind it to an instance"""
        session_id = f"session-{uuid.uuid4().hex[:8]}"
        
        session = {
            "session_id": session_id,
            "call_id": call_id,
            "user_id": user_id,
            "instance_id": instance_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "context": {},
            "conversation_history": []
        }
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        session = self.sessions.get(session_id)
        if session and datetime.utcnow() - session["last_activity"] < timedelta(seconds=self.session_timeout):
            session["last_activity"] = datetime.utcnow()
            return session
        return None
    
    def get_instance_for_session(self, session_id: str) -> Optional[str]:
        """Get the instance ID for a given session"""
        session = self.get_session(session_id)
        return session["instance_id"] if session else None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.sessions[session_id]["last_activity"] = datetime.utcnow()
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.utcnow()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session["last_activity"] > timedelta(seconds=self.session_timeout)
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        self.cleanup_expired_sessions()
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len([s for s in self.sessions.values() 
                                  if datetime.utcnow() - s["last_activity"] < timedelta(minutes=5)])
        }

class GlobalLoadBalancer:
    """Global load balancer for voice AI services"""
    
    def __init__(self):
        self.regions = {}
        self.instances = {}
        self.health_checker = HealthChecker()
        self.session_manager = SessionManager()
        self.metrics = LoadBalancerMetrics(
            total_requests=0,
            requests_per_region={},
            average_latency_ms=0.0,
            error_rate=0.0,
            active_sessions=0,
            timestamp=datetime.utcnow()
        )
        
        # Load balancing strategies
        self.strategies = {
            "round_robin": self._round_robin,
            "least_connections": self._least_connections,
            "weighted_round_robin": self._weighted_round_robin,
            "geographic": self._geographic,
            "session_aware": self._session_aware
        }
        
        self.current_strategy = "session_aware"
        self.round_robin_index = 0
    
    def add_region(self, region: Region):
        """Add a region to the load balancer"""
        self.regions[region.region_id] = region
        self.metrics.requests_per_region[region.region_id] = 0
    
    def add_instance(self, instance: Instance):
        """Add an instance to the load balancer"""
        self.instances[instance.instance_id] = instance
    
    def _round_robin(self, available_instances: List[Instance]) -> Optional[Instance]:
        """Round-robin load balancing"""
        if not available_instances:
            return None
        
        instance = available_instances[self.round_robin_index % len(available_instances)]
        self.round_robin_index += 1
        return instance
    
    def _least_connections(self, available_instances: List[Instance]) -> Optional[Instance]:
        """Least connections load balancing"""
        if not available_instances:
            return None
        
        return min(available_instances, key=lambda x: x.current_connections)
    
    def _weighted_round_robin(self, available_instances: List[Instance]) -> Optional[Instance]:
        """Weighted round-robin based on capacity"""
        if not available_instances:
            return None
        
        # Calculate total weight
        total_weight = sum(instance.max_connections for instance in available_instances)
        if total_weight == 0:
            return available_instances[0]
        
        # Select based on weight
        random_value = random.uniform(0, total_weight)
        current_weight = 0
        
        for instance in available_instances:
            current_weight += instance.max_connections
            if random_value <= current_weight:
                return instance
        
        return available_instances[-1]
    
    def _geographic(self, available_instances: List[Instance], user_location: str) -> Optional[Instance]:
        """Geographic load balancing based on user location"""
        if not available_instances:
            return None
        
        # Simulate geographic proximity calculation
        # In real implementation, this would use actual geographic data
        location_scores = {}
        
        for instance in available_instances:
            region = self.regions.get(instance.region_id)
            if region:
                # Simulate distance calculation
                distance_score = random.uniform(0.1, 1.0)  # Lower is better
                latency_score = region.latency_ms / 1000.0  # Normalize latency
                
                # Combine distance and latency
                total_score = (distance_score + latency_score) / 2
                location_scores[instance] = total_score
        
        if location_scores:
            return min(location_scores.keys(), key=lambda x: location_scores[x])
        
        return available_instances[0]
    
    def _session_aware(self, available_instances: List[Instance], session_id: Optional[str] = None) -> Optional[Instance]:
        """Session-aware load balancing"""
        if not available_instances:
            return None
        
        # If session exists, try to route to the same instance
        if session_id:
            instance_id = self.session_manager.get_instance_for_session(session_id)
            if instance_id and instance_id in self.instances:
                instance = self.instances[instance_id]
                if instance in available_instances and instance.health_status == "healthy":
                    return instance
        
        # Fall back to least connections for new sessions
        return self._least_connections(available_instances)
    
    def get_available_instances(self) -> List[Instance]:
        """Get all healthy instances"""
        return [
            instance for instance in self.instances.values()
            if instance.health_status in ["healthy", "degraded"]
        ]
    
    async def route_call(self, call_request: CallRequest) -> Dict[str, Any]:
        """Route a call to the best available instance"""
        start_time = time.time()
        
        try:
            # Get available instances
            available_instances = self.get_available_instances()
            
            if not available_instances:
                raise Exception("No healthy instances available")
            
            # Select instance based on strategy
            strategy_func = self.strategies.get(self.current_strategy, self._session_aware)
            
            if self.current_strategy == "geographic":
                selected_instance = strategy_func(available_instances, call_request.user_location)
            elif self.current_strategy == "session_aware":
                selected_instance = strategy_func(available_instances, call_request.session_id)
            else:
                selected_instance = strategy_func(available_instances)
            
            if not selected_instance:
                raise Exception("No suitable instance found")
            
            # Create or retrieve session
            session_id = call_request.session_id
            if not session_id:
                session_id = self.session_manager.create_session(
                    call_request.call_id,
                    call_request.user_id,
                    selected_instance.instance_id
                )
            
            # Update instance metrics
            selected_instance.current_connections += 1
            
            # Update global metrics
            self.metrics.total_requests += 1
            region = self.regions.get(selected_instance.region_id)
            if region:
                self.metrics.requests_per_region[region.region_id] += 1
            
            # Simulate call processing
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Calculate latency
            processing_time = (time.time() - start_time) * 1000
            self.metrics.average_latency_ms = (
                (self.metrics.average_latency_ms + processing_time) / 2
            )
            
            # Update session
            self.session_manager.update_session(session_id, {
                "conversation_history": [
                    {"role": "user", "text": "Hello", "timestamp": datetime.utcnow().isoformat()},
                    {"role": "assistant", "text": "How can I help you?", "timestamp": datetime.utcnow().isoformat()}
                ]
            })
            
            # Release connection
            selected_instance.current_connections = max(0, selected_instance.current_connections - 1)
            
            return {
                "success": True,
                "instance_id": selected_instance.instance_id,
                "region_id": selected_instance.region_id,
                "session_id": session_id,
                "latency_ms": processing_time,
                "strategy_used": self.current_strategy
            }
            
        except Exception as e:
            self.metrics.error_rate = min(1.0, self.metrics.error_rate + 0.01)
            return {
                "success": False,
                "error": str(e),
                "latency_ms": (time.time() - start_time) * 1000
            }
    
    async def perform_health_checks(self):
        """Perform health checks on all regions and instances"""
        print("   Performing health checks...")
        
        # Check regions
        for region in self.regions.values():
            is_healthy = await self.health_checker.check_region_health(region)
            if not is_healthy:
                print(f"     Region {region.name} is unhealthy")
        
        # Check instances
        for instance in self.instances.values():
            is_healthy = await self.health_checker.check_instance_health(instance)
            if not is_healthy:
                print(f"     Instance {instance.instance_id} is unhealthy")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get load balancer metrics"""
        session_stats = self.session_manager.get_session_stats()
        
        return {
            "total_requests": self.metrics.total_requests,
            "requests_per_region": self.metrics.requests_per_region,
            "average_latency_ms": round(self.metrics.average_latency_ms, 2),
            "error_rate": round(self.metrics.error_rate, 3),
            "active_sessions": session_stats["active_sessions"],
            "total_sessions": session_stats["total_sessions"],
            "current_strategy": self.current_strategy,
            "healthy_instances": len([i for i in self.instances.values() if i.health_status == "healthy"]),
            "total_instances": len(self.instances)
        }

async def simulate_load_balancing_demo():
    """Demonstrate load balancing capabilities"""
    print("=" * 60)
    print("Chapter 9: Scalability and Cloud-Native Voice Architectures")
    print("Example: Load Balancing")
    print("=" * 60)
    
    # Initialize global load balancer
    load_balancer = GlobalLoadBalancer()
    
    # Add regions
    regions = [
        Region("us-east-1", "US East (N. Virginia)", "Virginia, USA", 50, 1000, 0, "healthy", datetime.utcnow()),
        Region("us-west-2", "US West (Oregon)", "Oregon, USA", 80, 800, 0, "healthy", datetime.utcnow()),
        Region("eu-west-1", "Europe (Ireland)", "Dublin, Ireland", 120, 600, 0, "healthy", datetime.utcnow()),
        Region("ap-southeast-1", "Asia Pacific (Singapore)", "Singapore", 150, 500, 0, "healthy", datetime.utcnow())
    ]
    
    for region in regions:
        load_balancer.add_region(region)
    
    # Add instances to each region
    for region in regions:
        for i in range(3):  # 3 instances per region
            instance = Instance(
                instance_id=f"{region.region_id}-instance-{i+1}",
                region_id=region.region_id,
                ip_address=f"10.0.{i+1}.{i+1}",
                port=8080,
                health_status="healthy",
                current_connections=0,
                max_connections=100,
                cpu_utilization=random.uniform(20, 60),
                memory_utilization=random.uniform(30, 70),
                last_health_check=datetime.utcnow()
            )
            load_balancer.add_instance(instance)
    
    print(f"\n1. Load Balancer Configuration:")
    print(f"   Regions: {len(regions)}")
    print(f"   Total Instances: {len(load_balancer.instances)}")
    print(f"   Current Strategy: {load_balancer.current_strategy}")
    
    print(f"\n2. Regions and Instances:")
    for region in regions:
        region_instances = [i for i in load_balancer.instances.values() if i.region_id == region.region_id]
        print(f"   {region.name} ({region.region_id}):")
        print(f"     - Latency: {region.latency_ms}ms")
        print(f"     - Capacity: {region.capacity}")
        print(f"     - Instances: {len(region_instances)}")
    
    print(f"\n3. Load Balancing Simulation:")
    print(f"   Simulating 50 calls with different strategies...")
    
    # Test different strategies
    strategies = ["round_robin", "least_connections", "geographic", "session_aware"]
    
    for strategy in strategies:
        print(f"\n   Testing Strategy: {strategy}")
        load_balancer.current_strategy = strategy
        
        # Simulate calls
        for i in range(10):
            call_request = CallRequest(
                call_id=f"call-{strategy}-{i+1}",
                user_id=f"user-{i+1}",
                user_location="New York, USA",
                audio_data=b"sample_audio",
                session_id=f"session-{i+1}" if strategy == "session_aware" else None
            )
            
            result = await load_balancer.route_call(call_request)
            
            if result["success"]:
                print(f"     Call {i+1}: Instance {result['instance_id']} (Region: {result['region_id']}) - {result['latency_ms']:.1f}ms")
            else:
                print(f"     Call {i+1}: Failed - {result['error']}")
    
    print(f"\n4. Health Check Simulation:")
    await load_balancer.perform_health_checks()
    
    print(f"\n5. Load Balancer Metrics:")
    metrics = load_balancer.get_metrics()
    print(f"   Total Requests: {metrics['total_requests']}")
    print(f"   Average Latency: {metrics['average_latency_ms']}ms")
    print(f"   Error Rate: {metrics['error_rate']:.3f}")
    print(f"   Active Sessions: {metrics['active_sessions']}")
    print(f"   Healthy Instances: {metrics['healthy_instances']}/{metrics['total_instances']}")
    
    print(f"\n   Requests per Region:")
    for region_id, count in metrics['requests_per_region'].items():
        region_name = next(r.name for r in regions if r.region_id == region_id)
        print(f"     {region_name}: {count}")
    
    print(f"\n6. Load Balancing Benefits:")
    print(f"   ✓ Geographic distribution for low latency")
    print(f"   ✓ Session persistence for conversation continuity")
    print(f"   ✓ Automatic failover for high availability")
    print(f"   ✓ Multiple routing strategies for different needs")
    print(f"   ✓ Health monitoring and automatic recovery")
    print(f"   ✓ Load distribution for optimal resource utilization")
    
    return load_balancer

if __name__ == "__main__":
    asyncio.run(simulate_load_balancing_demo())
