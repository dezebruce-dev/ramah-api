"""
EZEKIEL UNIVERSAL INFORMATION GRID - COMPLETE COORDINATE SYSTEM
================================================================

This is a self-contained implementation of the Ezekiel coordinate system.
Everything you need to get started is in this single file.

Usage:
    python ezekiel_complete.py          # Run demo
    
Or import in your code:
    from ezekiel_complete import EzekielCoordinate, make_coordinate

Author: Built November 19, 2025
Version: 1.0.0 - Foundation Complete
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Tuple
import math
import re


# ============================================================================
# CORE ENUMS
# ============================================================================

class Layer(Enum):
    """Seven layers representing process stages from foundation to completion."""
    L1 = 1  # Foundation/Physical
    L2 = 2  # Structure/Organization
    L3 = 3  # Pattern/Application
    L4 = 4  # Execution/Service
    L5 = 5  # Integration/Coordination
    L6 = 6  # Ecosystem/Network
    L7 = 7  # Completion/Innovation


class Quadrant(Enum):
    """Four quadrants representing state phases."""
    Q1 = 1  # Initiation/Beginning
    Q2 = 2  # Fracture/Separation
    Q3 = 3  # Pattern/Clarity
    Q4 = 4  # Resolution/Restoration


# ============================================================================
# MAIN COORDINATE CLASS
# ============================================================================

@dataclass
class EzekielCoordinate:
    """
    A coordinate in Ezekiel's semantic space.
    
    Attributes:
        layer: Process stage (L1-L7)
        quadrant: State phase (Q1-Q4)
        lexicon: Domain of knowledge (TECH, BIO, etc.)
        entity: Specific concept within domain
        coherence: Validation score (0-3)
    """
    
    layer: Layer
    quadrant: Quadrant
    lexicon: str
    entity: str
    coherence: int
    
    def __post_init__(self):
        """Validate coherence score"""
        if not 0 <= self.coherence <= 3:
            raise ValueError(f"Coherence must be 0-3, got {self.coherence}")
    
    def to_string(self) -> str:
        """Generate standard coordinate string: L4.Q3.TECH.NETWORK[C2]"""
        return (f"{self.layer.name}."
                f"{self.quadrant.name}."
                f"{self.lexicon}."
                f"{self.entity}"
                f"[C{self.coherence}]")
    
    @classmethod
    def from_string(cls, coord_str: str) -> 'EzekielCoordinate':
        """Parse coordinate string back to object."""
        pattern = r'L(\d)\.Q(\d)\.([A-Z_]+)\.([A-Z_\.]+)\[C(\d)\]'
        match = re.match(pattern, coord_str)
        
        if not match:
            raise ValueError(f"Invalid coordinate string: {coord_str}")
        
        layer_num, quad_num, lexicon, entity, coherence = match.groups()
        
        return cls(
            layer=Layer[f"L{layer_num}"],
            quadrant=Quadrant[f"Q{quad_num}"],
            lexicon=lexicon,
            entity=entity,
            coherence=int(coherence)
        )
    
    def distance_to(self, other: 'EzekielCoordinate') -> float:
        """Calculate semantic distance between two coordinates."""
        # Layer distance (0-6, normalized to 0-1)
        layer_dist = abs(self.layer.value - other.layer.value) / 6.0
        
        # Quadrant distance (circular, 0-2, normalized to 0-1)
        quad_diff = abs(self.quadrant.value - other.quadrant.value)
        quad_dist = min(quad_diff, 4 - quad_diff) / 2.0
        
        # Lexicon match (0 if same, 1 if different)
        lexicon_dist = 0.0 if self.lexicon == other.lexicon else 1.0
        
        # Entity similarity
        entity_dist = self._entity_distance(other.entity)
        
        # Weighted combination
        distance = (
            layer_dist * 0.3 +
            quad_dist * 0.3 +
            lexicon_dist * 0.2 +
            entity_dist * 0.2
        )
        
        return distance
    
    def _entity_distance(self, other_entity: str) -> float:
        """Calculate entity similarity using normalized Levenshtein distance."""
        if self.entity == other_entity:
            return 0.0
        
        if self.entity in other_entity or other_entity in self.entity:
            return 0.3
        
        # Levenshtein distance
        s1, s2 = self.entity, other_entity
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        
        distances = range(len(s2) + 1)
        for i1, c1 in enumerate(s1):
            new_distances = [i1 + 1]
            for i2, c2 in enumerate(s2):
                if c1 == c2:
                    new_distances.append(distances[i2])
                else:
                    new_distances.append(1 + min(distances[i2],
                                                  distances[i2 + 1],
                                                  new_distances[-1]))
            distances = new_distances
        
        return distances[-1] / max(len(s1), len(s2))
    
    def neighbors(self, radius: float = 1.0) -> List['EzekielCoordinate']:
        """Generate nearby coordinates within semantic radius."""
        neighbors = []
        
        for layer_offset in [-2, -1, 0, 1, 2]:
            new_layer_val = self.layer.value + layer_offset
            if not 1 <= new_layer_val <= 7:
                continue
            new_layer = Layer(new_layer_val)
            
            for quad in Quadrant:
                neighbor = EzekielCoordinate(
                    layer=new_layer,
                    quadrant=quad,
                    lexicon=self.lexicon,
                    entity=self.entity,
                    coherence=self.coherence
                )
                
                dist = self.distance_to(neighbor)
                if dist <= radius and dist > 0:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def vector_representation(self) -> Tuple[float, float, float, float]:
        """Convert coordinate to 4D vector for geometric operations."""
        layer_vec = float(self.layer.value)
        
        angle = (self.quadrant.value - 1) * (math.pi / 2)
        quad_x = math.cos(angle)
        quad_y = math.sin(angle)
        
        coherence_vec = float(self.coherence)
        
        return (layer_vec, quad_x, quad_y, coherence_vec)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"EzekielCoordinate({self.to_string()})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, EzekielCoordinate):
            return False
        return self.to_string() == other.to_string()
    
    def __hash__(self) -> int:
        return hash(self.to_string())


# ============================================================================
# COORDINATE SPACE
# ============================================================================

class CoordinateSpace:
    """Represents the entire Ezekiel coordinate space with operations."""
    
    def __init__(self):
        self.coordinates: List[EzekielCoordinate] = []
    
    def add(self, coord: EzekielCoordinate):
        """Add coordinate to space"""
        self.coordinates.append(coord)
    
    def find_nearest(self, target: EzekielCoordinate, 
                    k: int = 5) -> List[Tuple[EzekielCoordinate, float]]:
        """Find k nearest coordinates to target."""
        distances = [
            (coord, target.distance_to(coord))
            for coord in self.coordinates
            if coord != target
        ]
        
        distances.sort(key=lambda x: x[1])
        return distances[:k]
    
    def cluster_by_layer(self) -> dict:
        """Group coordinates by layer"""
        clusters = {layer: [] for layer in Layer}
        for coord in self.coordinates:
            clusters[coord.layer].append(coord)
        return clusters
    
    def cluster_by_lexicon(self) -> dict:
        """Group coordinates by lexicon"""
        clusters = {}
        for coord in self.coordinates:
            if coord.lexicon not in clusters:
                clusters[coord.lexicon] = []
            clusters[coord.lexicon].append(coord)
        return clusters
    
    def density_at(self, coord: EzekielCoordinate, radius: float = 1.0) -> int:
        """Calculate semantic density around a coordinate."""
        count = 0
        for other in self.coordinates:
            if coord.distance_to(other) <= radius:
                count += 1
        return count


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def make_coordinate(layer: int, quadrant: int, lexicon: str, 
                   entity: str, coherence: int = 2) -> EzekielCoordinate:
    """Quick coordinate creation."""
    return EzekielCoordinate(
        layer=Layer[f"L{layer}"],
        quadrant=Quadrant[f"Q{quadrant}"],
        lexicon=lexicon,
        entity=entity,
        coherence=coherence
    )


def parse_coordinate(coord_str: str) -> EzekielCoordinate:
    """Alias for EzekielCoordinate.from_string"""
    return EzekielCoordinate.from_string(coord_str)


# ============================================================================
# DEMO / MAIN
# ============================================================================

def run_demo():
    """Run comprehensive demonstration of Ezekiel coordinate system."""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          EZEKIEL COORDINATE SYSTEM DEMO                  ║
║                                                          ║
║          Storage by Meaning, Not Location                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Demo 1: Create coordinates
    print("\n" + "="*60)
    print("  1. Creating Coordinates")
    print("="*60)
    
    coord1 = make_coordinate(4, 3, "TECH", "NETWORK.TCP", 2)
    print(f"\nCreated: {coord1}")
    print(f"  Layer: {coord1.layer.name} (Execution/Service)")
    print(f"  Quadrant: {coord1.quadrant.name} (Pattern/Clarity)")
    print(f"  Lexicon: {coord1.lexicon}")
    print(f"  Entity: {coord1.entity}")
    print(f"  Coherence: C{coord1.coherence} (Strong)")
    
    # Demo 2: Distances
    print("\n" + "="*60)
    print("  2. Semantic Distance")
    print("="*60)
    
    coord2 = make_coordinate(4, 3, "TECH", "NETWORK.UDP", 2)
    coord3 = make_coordinate(5, 4, "BIO", "CELL.MITOSIS", 3)
    
    print(f"\nReference: {coord1}")
    print(f"\nSimilar concept (UDP):")
    print(f"  Target: {coord2}")
    print(f"  Distance: {coord1.distance_to(coord2):.3f}")
    
    print(f"\nDifferent domain (Biology):")
    print(f"  Target: {coord3}")
    print(f"  Distance: {coord1.distance_to(coord3):.3f}")
    
    # Demo 3: Neighbors
    print("\n" + "="*60)
    print("  3. Finding Neighbors")
    print("="*60)
    
    center = make_coordinate(4, 2, "TECH", "NETWORK.SECURITY", 2)
    print(f"\nCenter: {center}")
    
    neighbors = center.neighbors(radius=0.5)
    print(f"\nFound {len(neighbors)} neighbors within radius 0.5")
    for neighbor in neighbors[:3]:
        print(f"  {neighbor} (distance: {center.distance_to(neighbor):.3f})")
    
    # Demo 4: Coordinate Space
    print("\n" + "="*60)
    print("  4. AI Memory Example")
    print("="*60)
    
    space = CoordinateSpace()
    
    knowledge = [
        ("TCP is reliable", make_coordinate(4, 3, "TECH", "NETWORK.TCP", 2)),
        ("UDP is fast", make_coordinate(4, 3, "TECH", "NETWORK.UDP", 2)),
        ("DNS resolves names", make_coordinate(4, 3, "TECH", "NETWORK.DNS", 2)),
    ]
    
    print("\nStoring knowledge:")
    for content, coord in knowledge:
        space.add(coord)
        print(f"  '{content}' → {coord}")
    
    print("\n\nQuery: 'What about network protocols?'")
    search_center = make_coordinate(4, 3, "TECH", "NETWORK", 2)
    results = space.find_nearest(search_center, k=3)
    
    print("\nRetrieved:")
    for coord, distance in results:
        relevance = 1 - distance
        print(f"  {coord} (relevance: {relevance:.2f})")
    
    # Summary
    print("\n" + "="*60)
    print("  Summary")
    print("="*60)
    print("""
The Ezekiel coordinate system provides:

✓ Semantic addressing (meaning is the location)
✓ Geometric distance calculations
✓ Neighbor discovery in meaning-space
✓ Multi-dimensional organization
✓ Cross-domain pattern recognition

Next steps:
- Add semantic encoder (text → coordinates)
- Build storage layer with echo redundancy
- Create REST API
- Develop domain lexicons
    """)


if __name__ == "__main__":
    run_demo()
