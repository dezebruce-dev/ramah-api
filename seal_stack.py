"""
SEAL STACK - Semantic Code Retrieval System
7-layer meaning-based architecture for code pattern assembly

Based on LHT framework:
- Each seal represents a meaning layer
- Patterns retrieved by semantic depth, not category
- Automatic coherence validation across seals
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import sys
sys.path.append('/mnt/project')

from tech_lexicon import TECH_PATTERNS


class SealLayer(Enum):
    """7 Seals mapping to LHT spirals"""
    IDENTITY = 1      # What IS this? (Essence)
    STRUCTURE = 2     # What's its SHAPE? (Form)
    FUNCTION = 3      # What does it DO? (Behavior)
    AUTHORITY = 4     # Who can ACCESS it? (Gate)
    COMMUNITY = 5     # How does it RELATE? (Network)
    WISDOM = 6        # How does it EVOLVE? (Adaptation)
    FULFILLMENT = 7   # What's COMPLETE form? (Telos)


@dataclass
class SemanticQuery:
    """Parsed semantic query"""
    concept: str           # e.g., "Users", "Authentication"
    domain: str           # e.g., "API", "Database"
    context: List[str]    # Additional context
    required_seals: List[SealLayer]  # Which seals to traverse


@dataclass
class SealPattern:
    """Pattern at a specific seal layer"""
    seal: SealLayer
    coordinate: str
    pattern: Dict[str, Any]
    coherence_score: int
    semantic_tags: List[str]


class SemanticRouter:
    """Routes queries through 7-layer seal stack"""
    
    # Semantic mapping: concept -> seal layers
    CONCEPT_SEAL_MAP = {
        "user": {
            SealLayer.IDENTITY: ["ENTITY", "PERSONHOOD", "IDENTITY"],
            SealLayer.STRUCTURE: ["MODEL", "SCHEMA", "DATACLASS"],
            SealLayer.FUNCTION: ["CRUD", "REST", "API"],
            SealLayer.AUTHORITY: ["AUTH", "JWT", "PERMISSION"],
            SealLayer.COMMUNITY: ["RELATIONSHIP", "FOREIGN_KEY"],
            SealLayer.WISDOM: ["MIGRATION", "VERSION"],
            SealLayer.FULFILLMENT: ["TEST", "VALIDATION"]
        },
        "api": {
            SealLayer.IDENTITY: ["SERVICE", "ENDPOINT"],
            SealLayer.STRUCTURE: ["ROUTER", "BLUEPRINT"],
            SealLayer.FUNCTION: ["HTTP", "REST", "HANDLER"],
            SealLayer.AUTHORITY: ["AUTH", "MIDDLEWARE"],
            SealLayer.COMMUNITY: ["CLIENT", "INTEGRATION"],
            SealLayer.WISDOM: ["VERSION", "DEPRECATION"],
            SealLayer.FULFILLMENT: ["DEPLOY", "MONITOR"]
        },
        "database": {
            SealLayer.IDENTITY: ["DATA", "PERSISTENCE"],
            SealLayer.STRUCTURE: ["SCHEMA", "TABLE", "MODEL"],
            SealLayer.FUNCTION: ["QUERY", "TRANSACTION"],
            SealLayer.AUTHORITY: ["ACCESS", "ROLE"],
            SealLayer.COMMUNITY: ["RELATION", "JOIN"],
            SealLayer.WISDOM: ["MIGRATION", "INDEX"],
            SealLayer.FULFILLMENT: ["BACKUP", "OPTIMIZATION"]
        }
    }
    
    def __init__(self):
        self.patterns = TECH_PATTERNS
    
    def parse_query(self, query: str) -> SemanticQuery:
        """Parse natural language query into semantic structure"""
        query_lower = query.lower()
        
        # Detect concept
        concept = None
        if "user" in query_lower:
            concept = "user"
        elif "api" in query_lower or "endpoint" in query_lower:
            concept = "api"
        elif "database" in query_lower or "db" in query_lower:
            concept = "database"
        else:
            concept = "general"
        
        # Detect domain
        domain = "web"
        if "database" in query_lower or "sql" in query_lower:
            domain = "database"
        elif "auth" in query_lower:
            domain = "auth"
        
        # Determine required seals
        required_seals = list(SealLayer)  # Default: all 7
        
        # Could narrow based on query specificity
        if "basic" in query_lower or "simple" in query_lower:
            required_seals = required_seals[:3]  # Just first 3 seals
        
        return SemanticQuery(
            concept=concept,
            domain=domain,
            context=query.split(),
            required_seals=required_seals
        )
    
    def route_through_seals(self, query: SemanticQuery) -> List[SealPattern]:
        """Route query through seal stack, retrieving patterns at each layer"""
        seal_patterns = []
        
        concept_map = self.CONCEPT_SEAL_MAP.get(query.concept, {})
        
        for seal in query.required_seals:
            # Get semantic tags for this seal
            tags = concept_map.get(seal, [])
            
            # Find matching patterns
            pattern = self._find_pattern_for_seal(seal, tags, query.domain)
            
            if pattern:
                seal_patterns.append(pattern)
        
        return seal_patterns
    
    def _find_pattern_for_seal(
        self, 
        seal: SealLayer, 
        tags: List[str],
        domain: str
    ) -> Optional[SealPattern]:
        """Find best matching pattern for seal layer"""
        
        # Map seal to layer number
        layer_num = seal.value
        
        # Search patterns at this layer
        candidates = []
        
        for coord, pattern_data in self.patterns.items():
            # Check if pattern is at correct layer
            if not coord.startswith(f"L{layer_num}"):
                continue
            
            # Check if pattern matches semantic tags
            coord_upper = coord.upper()
            match_score = sum(1 for tag in tags if tag in coord_upper)
            
            if match_score > 0:
                candidates.append({
                    'coord': coord,
                    'data': pattern_data,
                    'score': match_score
                })
        
        if not candidates:
            return None
        
        # Return highest scoring pattern
        best = max(candidates, key=lambda x: x['score'])
        
        return SealPattern(
            seal=seal,
            coordinate=best['coord'],
            pattern=best['data'],
            coherence_score=best['data'].get('coherence', 0),
            semantic_tags=tags
        )


class SealStackAssembler:
    """Assembles complete modules from seal-routed patterns"""
    
    def __init__(self):
        self.router = SemanticRouter()
    
    def build_module(self, query: str) -> Dict[str, Any]:
        """Build complete module by traversing seal stack"""
        
        # Parse query
        semantic_query = self.router.parse_query(query)
        
        # Route through seals
        seal_patterns = self.router.route_through_seals(semantic_query)
        
        # Assemble module
        module = {
            'query': query,
            'concept': semantic_query.concept,
            'seals': [],
            'code': {},
            'coherence': 0,
            'completeness': 0
        }
        
        for seal_pattern in seal_patterns:
            seal_data = {
                'seal': seal_pattern.seal.name,
                'layer': seal_pattern.seal.value,
                'coordinate': seal_pattern.coordinate,
                'pattern_name': seal_pattern.pattern.get('name', 'Unknown'),
                'coherence': seal_pattern.coherence_score,
                'semantic_tags': seal_pattern.semantic_tags
            }
            
            module['seals'].append(seal_data)
            
            # Add code from pattern
            seal_name = seal_pattern.seal.name.lower()
            module['code'][seal_name] = {
                'code': seal_pattern.pattern.get('code', ''),
                'tests': seal_pattern.pattern.get('tests', ''),
                'dependencies': seal_pattern.pattern.get('dependencies', [])
            }
        
        # Calculate overall coherence
        if seal_patterns:
            module['coherence'] = sum(
                sp.coherence_score for sp in seal_patterns
            ) / len(seal_patterns)
        
        # Calculate completeness (how many seals filled)
        module['completeness'] = (
            len(seal_patterns) / len(semantic_query.required_seals)
        ) * 100
        
        return module
    
    def generate_unified_code(self, module: Dict[str, Any]) -> str:
        """Generate unified code from seal-assembled patterns"""
        
        code_parts = []
        dependencies = set()
        
        code_parts.append(f'"""\n{module["concept"].upper()} MODULE')
        code_parts.append(f'Generated via Seal Stack semantic routing')
        code_parts.append(f'Coherence: {module["coherence"]:.1f}/3.0')
        code_parts.append(f'Completeness: {module["completeness"]:.0f}%')
        code_parts.append('"""')
        code_parts.append('')
        
        # Collect dependencies
        for seal_data in module['code'].values():
            dependencies.update(seal_data.get('dependencies', []))
        
        # Add imports
        if dependencies:
            code_parts.append('# Dependencies')
            for dep in sorted(dependencies):
                code_parts.append(f'import {dep}')
            code_parts.append('')
        
        # Add code by seal layer
        for seal in module['seals']:
            seal_name = seal['seal'].lower()
            seal_code_data = module['code'].get(seal_name, {})
            
            code_parts.append(f'# ===== SEAL {seal["layer"]}: {seal["seal"]} =====')
            code_parts.append(f'# Pattern: {seal["pattern_name"]}')
            code_parts.append(f'# Coordinate: {seal["coordinate"]}')
            code_parts.append('')
            
            code = seal_code_data.get('code', '')
            if code:
                code_parts.append(code)
                code_parts.append('')
        
        return '\n'.join(code_parts)


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo_seal_stack():
    """Demonstrate seal stack semantic routing"""
    
    print("="*70)
    print("SEAL STACK SEMANTIC ROUTER - DEMONSTRATION")
    print("="*70)
    print()
    
    assembler = SealStackAssembler()
    
    # Example 1: Users Module
    print("EXAMPLE 1: Building Users Module")
    print("-" * 70)
    
    module = assembler.build_module("Create a users module with authentication")
    
    print(f"Concept: {module['concept']}")
    print(f"Coherence: {module['coherence']:.1f}/3.0")
    print(f"Completeness: {module['completeness']:.0f}%")
    print()
    print("Seal Stack Traversal:")
    
    for seal in module['seals']:
        print(f"  {seal['layer']}. {seal['seal']:15} → {seal['coordinate']}")
        print(f"     Pattern: {seal['pattern_name']}")
        print(f"     Tags: {', '.join(seal['semantic_tags'])}")
        print()
    
    # Show generated code
    print("\nGenerated Unified Code:")
    print("-" * 70)
    unified_code = assembler.generate_unified_code(module)
    print(unified_code[:500] + "..." if len(unified_code) > 500 else unified_code)
    print()
    
    # Example 2: API Module
    print("\n" + "="*70)
    print("EXAMPLE 2: Building API Module")
    print("-" * 70)
    
    module = assembler.build_module("Build a REST API endpoint")
    
    print(f"Concept: {module['concept']}")
    print(f"Seals traversed: {len(module['seals'])}")
    print()
    
    for seal in module['seals']:
        print(f"  {seal['layer']}. {seal['seal']:15} → {seal['pattern_name']}")
    
    print()
    print("="*70)
    print("SEAL STACK VS FLAT RETRIEVAL")
    print("="*70)
    print()
    print("Traditional approach:")
    print("  - Search by keyword")
    print("  - Return matching patterns")
    print("  - No semantic depth")
    print()
    print("Seal Stack approach:")
    print("  - Parse query semantically")
    print("  - Route through 7 meaning layers")
    print("  - Retrieve patterns by WHAT THEY MEAN")
    print("  - Assemble with coherence validation")
    print("  - Result: semantically unified module")
    print()


if __name__ == "__main__":
    demo_seal_stack()
