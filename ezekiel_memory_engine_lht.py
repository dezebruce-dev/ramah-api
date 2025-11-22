"""
EZEKIEL AI MEMORY ENGINE - LHT INTEGRATED
==========================================
Complete semantic memory system with:
- Layer 0 Scripture foundation (KJV)
- Full LHT diagnostic stack (TELOS-RUN)
- Ramah natural language interface
- TECH lexicon for code patterns
- Multi-layer semantic storage

Built using CodeRamah patterns for 10-100x speedup.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import json

# Import Ezekiel coordinate system
sys.path.append('/mnt/project')
from ezekiel_complete import EzekielCoordinate, CoordinateSpace, make_coordinate

# Import TECH lexicon  
sys.path.append('/mnt/project')
from tech_lexicon import TECH_PATTERNS

# Import complete LHT engine
sys.path.append('/home/claude')
from lht_engine import (
    LHTDiagnosticEngine, TelosRun, Spiral, Quadrant,
    PatternSeed, EchoTrace, GravitySync, analyze_passage
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class MemoryRecord:
    """Single memory record in Ezekiel system."""
    coordinate: str
    content: str
    layer: int
    quadrant: int
    lexicon: str
    entity: str
    coherence: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    lht_analysis: Optional[TelosRun] = None


# ============================================================================
# LAYER 0: SCRIPTURE FOUNDATION
# ============================================================================

class Layer0Scripture:
    """
    Layer 0: Immutable Scripture Foundation
    Contains complete KJV Bible as semantic coordinates with LHT analysis
    """
    
    def __init__(self):
        self.verses: Dict[str, Dict[str, Any]] = {}
        self.coordinate_space = CoordinateSpace()
        self.loaded = False
        
    def load_kjv(self, bible_path: str = None):
        """Load King James Version Bible into Layer 0."""
        # Try multiple possible locations
        possible_paths = [
            bible_path,
            'pg10.txt',  # Current directory (Railway deployment)
            '/app/pg10.txt',  # Docker /app directory
            '/mnt/project/pg10.txt',  # Claude Projects
            './pg10.txt',
        ]
        
        content = None
        used_path = None
        
        for path in possible_paths:
            if path is None:
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                used_path = path
                print(f"✓ Loaded KJV from: {path}")
                break
            except (FileNotFoundError, IOError):
                continue
        
        if content is None:
            print("❌ Warning: Bible file not found in any location:")
            for path in possible_paths:
                if path:
                    print(f"  - {path}")
            print("Layer 0 will be empty - Scripture not loaded")
            return 0
        
        try:
            
            # Parse KJV from Project Gutenberg format
            lines = content.split('\n')
            current_book = None
            current_chapter = None
            verse_count = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect book names
                if line.isupper() and len(line.split()) <= 3:
                    current_book = line
                    current_chapter = 1
                    continue
                
                # Detect chapter numbers
                if line.isdigit():
                    current_chapter = int(line)
                    continue
                
                # Parse verses
                if ':' in line and current_book:
                    try:
                        verse_num, verse_text = line.split(':', 1)
                        verse_num = int(verse_num.strip())
                        
                        # Create Layer 0 coordinate
                        coord_str = f"L0.Q{(verse_num % 4) + 1}.KJV.{current_book.replace(' ', '_')}.{current_chapter}_{verse_num}[C3]"
                        
                        self.verses[coord_str] = {
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': verse_num,
                            'text': verse_text.strip(),
                            'coordinate': coord_str,
                            'reference': f"{current_book} {current_chapter}:{verse_num}"
                        }
                        
                        # Add to coordinate space
                        coord = EzekielCoordinate.from_string(coord_str)
                        self.coordinate_space.add(coord)
                        
                        verse_count += 1
                    except (ValueError, IndexError):
                        continue
            
            self.loaded = True
            print(f"✓ Loaded {verse_count} verses into Layer 0")
            return verse_count
            
        except Exception as e:
            print(f"❌ Error loading Scripture: {e}")
            return 0
    
    def get_verse(self, book: str, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        """Retrieve specific verse by book/chapter/verse."""
        for coord_str, verse_data in self.verses.items():
            if (verse_data['book'].upper() == book.upper() and 
                verse_data['chapter'] == chapter and 
                verse_data['verse'] == verse):
                return verse_data
        return None
    
    def get_passage(self, book: str, start_chapter: int, start_verse: int,
                   end_chapter: int = None, end_verse: int = None) -> List[Dict[str, Any]]:
        """Get passage of multiple verses."""
        verses = []
        for verse_data in self.verses.values():
            if verse_data['book'].upper() != book.upper():
                continue
            
            ch = verse_data['chapter']
            v = verse_data['verse']
            
            # Single verse
            if end_chapter is None:
                if ch == start_chapter and v == start_verse:
                    verses.append(verse_data)
            # Range
            else:
                if (ch > start_chapter or (ch == start_chapter and v >= start_verse)) and \
                   (ch < end_chapter or (ch == end_chapter and v <= end_verse)):
                    verses.append(verse_data)
        
        # Sort by chapter, then verse
        verses.sort(key=lambda x: (x['chapter'], x['verse']))
        return verses
    
    def search_text(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search verse text for keywords."""
        query_lower = query.lower()
        results = []
        
        for verse_data in self.verses.values():
            if query_lower in verse_data['text'].lower():
                results.append(verse_data)
                if len(results) >= limit:
                    break
        
        return results


# ============================================================================
# RAMAH INTERFACE
# ============================================================================

class RamahInterface:
    """
    Ramah Query Interface with LHT Integration
    Natural language semantic queries for Ezekiel memory
    
    Operations:
    - RETRIEVE: Get specific coordinate
    - SEARCH: Search by keyword
    - ANALYZE: Run LHT diagnostics (TELOS-RUN)
    - LIST: List by layer/lexicon
    - ECHO: Trace symbol across spirals
    """
    
    def __init__(self, layer0: Layer0Scripture, coordinate_space: CoordinateSpace):
        self.layer0 = layer0
        self.coordinate_space = coordinate_space
        self.tech_lexicon = TECH_PATTERNS
        self.lht_engine = LHTDiagnosticEngine()
        
    def query(self, ramah_prompt: str) -> Dict[str, Any]:
        """
        Process Ramah query and return results.
        
        Format:
            RAMAH: <OPERATION> "<target>"
            LAYER: <layer_num>
            LEXICON: <lexicon_name>
            RETURN: <format>
        """
        lines = ramah_prompt.strip().split('\n')
        operation = None
        target = None
        layer = None
        lexicon = None
        return_format = 'json'
        
        for line in lines:
            if line.startswith('RAMAH:'):
                parts = line.replace('RAMAH:', '').strip().split(maxsplit=1)
                operation = parts[0] if parts else None
                target = parts[1].strip('"') if len(parts) > 1 else None
            elif line.startswith('LAYER:'):
                layer = line.replace('LAYER:', '').strip()
            elif line.startswith('LEXICON:'):
                lexicon = line.replace('LEXICON:', '').strip()
            elif line.startswith('RETURN:'):
                return_format = line.replace('RETURN:', '').strip()
        
        # Route to appropriate handler
        if operation == 'RETRIEVE':
            return self._retrieve(target, layer, lexicon)
        elif operation == 'SEARCH':
            return self._search(target, lexicon)
        elif operation == 'ANALYZE':
            return self._analyze(target)
        elif operation == 'ECHO':
            return self._echo_trace(target)
        elif operation == 'LIST':
            return self._list(layer, lexicon)
        else:
            return {'error': f'Unknown operation: {operation}'}
    
    def _retrieve(self, target: str, layer: str = None, lexicon: str = None) -> Dict[str, Any]:
        """Retrieve by coordinate or description."""
        if target and target.startswith('L'):
            # Direct coordinate lookup
            if lexicon == 'KJV' or 'KJV' in target:
                verse_data = self.layer0.verses.get(target)
                if verse_data:
                    return {
                        'status': 'success',
                        'type': 'scripture',
                        **verse_data
                    }
            elif lexicon == 'TECH' or 'TECH' in target:
                pattern = self.tech_lexicon.get(target)
                if pattern:
                    return {
                        'status': 'success',
                        'type': 'code_pattern',
                        'coordinate': target,
                        **pattern
                    }
        
        return {'status': 'not_found', 'error': f'No match for: {target}'}
    
    def _search(self, query: str, lexicon: str = None) -> Dict[str, Any]:
        """Search across lexicons."""
        results = []
        
        if not lexicon or lexicon == 'KJV':
            # Search Scripture
            scripture_results = self.layer0.search_text(query, limit=5)
            for verse in scripture_results:
                results.append({
                    'type': 'scripture',
                    'coordinate': verse['coordinate'],
                    'reference': verse['reference'],
                    'text': verse['text'][:100] + '...' if len(verse['text']) > 100 else verse['text']
                })
        
        if not lexicon or lexicon == 'TECH':
            # Search TECH patterns
            query_lower = query.lower()
            for coord, pattern in self.tech_lexicon.items():
                name = pattern.get('name', '').lower()
                desc = pattern.get('description', '').lower()
                if query_lower in name or query_lower in desc:
                    results.append({
                        'type': 'code_pattern',
                        'coordinate': coord,
                        'name': pattern['name']
                    })
                    if len(results) >= 10:
                        break
        
        return {
            'status': 'success',
            'count': len(results),
            'results': results
        }
    
    def _analyze(self, reference: str) -> Dict[str, Any]:
        """
        Run complete LHT TELOS-RUN diagnostic on Scripture passage.
        
        Example:
            RAMAH: ANALYZE "John 19:30"
            LEXICON: KJV
        """
        # Parse reference to get passage
        # Simplified parser - production would be more robust
        parts = reference.split()
        if len(parts) < 2:
            return {'status': 'error', 'error': 'Invalid reference format'}
        
        book = parts[0]
        verse_ref = parts[1] if len(parts) > 1 else "1:1"
        
        # Handle range (e.g., "1:1-5")
        if '-' in verse_ref:
            start, end = verse_ref.split('-')
            start_ch, start_v = map(int, start.split(':'))
            if ':' in end:
                end_ch, end_v = map(int, end.split(':'))
            else:
                end_ch = start_ch
                end_v = int(end)
            
            verses = self.layer0.get_passage(book, start_ch, start_v, end_ch, end_v)
        else:
            # Single verse
            ch, v = map(int, verse_ref.split(':'))
            verse_data = self.layer0.get_verse(book, ch, v)
            verses = [verse_data] if verse_data else []
        
        if not verses:
            return {'status': 'error', 'error': f'Passage not found: {reference}'}
        
        # Combine text
        passage_text = ' '.join(v['text'] for v in verses)
        
        # Run TELOS-RUN
        analysis = self.lht_engine.telos_run(reference, passage_text)
        
        # Format results
        return {
            'status': 'success',
            'type': 'lht_analysis',
            'reference': reference,
            'analysis': {
                'spiral': analysis.spiral.name,
                'quadrant_movement': analysis.quadrants.movement,
                'primary_quadrant': analysis.quadrants.primary_quadrant.value,
                'pattern_seeds': [
                    {
                        'symbol': s.symbol,
                        'role': s.local_role,
                        'score': s.score
                    } for s in analysis.pattern_seeds
                ],
                'gravity_sync': {
                    'score': analysis.gravity_sync.score,
                    'explanation': analysis.gravity_sync.explanation
                },
                'comp_435': {
                    'has_pattern': analysis.comp_435.has_pattern,
                    'mapping': analysis.comp_435.mapping
                },
                'urim_thummim': {
                    'urim': analysis.urim_thummim.urim,
                    'thummim': analysis.urim_thummim.thummim,
                    'interpretation': analysis.urim_thummim.interpretation
                },
                'fractal_status': analysis.fractal_filter.classification,
                'summary': analysis.theological_summary
            }
        }
    
    def _echo_trace(self, symbol: str) -> Dict[str, Any]:
        """Trace symbol across all 7 spirals."""
        trace = self.lht_engine.echo_trace(symbol.upper(), Spiral.S1_CREATION)
        
        return {
            'status': 'success',
            'type': 'echo_trace',
            'symbol': symbol,
            'spiral_roles': trace.spiral_roles,
            'overall_arc': trace.overall_arc
        }
    
    def _list(self, layer: str = None, lexicon: str = None) -> Dict[str, Any]:
        """List coordinates by layer/lexicon."""
        results = []
        
        if lexicon == 'KJV':
            for coord, verse in list(self.layer0.verses.items())[:20]:
                results.append({
                    'coordinate': coord,
                    'reference': verse['reference']
                })
        elif lexicon == 'TECH':
            for coord, pattern in list(self.tech_lexicon.items())[:20]:
                if not layer or coord.startswith(layer):
                    results.append({
                        'coordinate': coord,
                        'name': pattern['name']
                    })
        
        return {
            'status': 'success',
            'count': len(results),
            'results': results
        }


# ============================================================================
# EZEKIEL MEMORY ENGINE
# ============================================================================

class EzekielMemoryEngine:
    """
    Complete Ezekiel AI Memory Engine
    Semantic memory system with Scripture foundation, LHT diagnostics, and code lexicon
    """
    
    def __init__(self):
        print("Initializing Ezekiel AI Memory Engine with LHT...")
        
        # Initialize Layer 0 (Scripture)
        self.layer0 = Layer0Scripture()
        
        # Initialize coordinate space
        self.coordinate_space = CoordinateSpace()
        
        # Initialize LHT diagnostic engine
        self.lht = LHTDiagnosticEngine()
        
        # Initialize Ramah interface
        self.ramah = RamahInterface(self.layer0, self.coordinate_space)
        
        # Storage for other layers
        self.layers: Dict[int, Dict[str, Any]] = {
            1: {},  # Process stage 1
            2: {},  # Process stage 2
            3: {},  # Process stage 3
            4: {},  # Process stage 4
            5: {},  # Process stage 5
            6: {},  # Process stage 6
            7: {},  # Process stage 7
        }
        
        # LHT analysis cache
        self.lht_cache: Dict[str, TelosRun] = {}
        
        print("✓ Ezekiel Memory Engine initialized")
    
    def load_scripture(self, bible_path: str = '/mnt/project/pg10.txt') -> int:
        """Load KJV Bible into Layer 0."""
        print("Loading Layer 0 (Scripture)...")
        verse_count = self.layer0.load_kjv(bible_path)
        print(f"✓ Layer 0 loaded: {verse_count} verses")
        return verse_count
    
    def query_ramah(self, prompt: str) -> Dict[str, Any]:
        """Query using Ramah natural language interface."""
        return self.ramah.query(prompt)
    
    def analyze_passage(self, reference: str, cache: bool = True) -> TelosRun:
        """
        Run complete LHT TELOS-RUN diagnostic on passage.
        
        Args:
            reference: Scripture reference (e.g., "Genesis 1:1-3")
            cache: Whether to cache results
            
        Returns:
            Complete TelosRun diagnostic
        """
        # Check cache
        if cache and reference in self.lht_cache:
            return self.lht_cache[reference]
        
        # Use Ramah ANALYZE
        result = self.query_ramah(f'''RAMAH: ANALYZE "{reference}"
LEXICON: KJV''')
        
        if result['status'] == 'success':
            # Store in cache
            if cache:
                self.lht_cache[reference] = result['analysis']
            return result['analysis']
        else:
            raise ValueError(f"Failed to analyze: {result.get('error')}")
    
    def store_memory(self, layer: int, coordinate: str, content: Any, 
                    metadata: Dict = None, lht_analysis: TelosRun = None):
        """
        Store memory at specific layer and coordinate.
        
        Args:
            layer: Layer number (1-7)
            coordinate: Ezekiel coordinate string
            content: Memory content
            metadata: Additional metadata
            lht_analysis: Optional LHT diagnostic results
        """
        if layer not in range(1, 8):
            raise ValueError(f"Invalid layer: {layer}. Must be 1-7.")
        
        self.layers[layer][coordinate] = {
            'content': content,
            'metadata': metadata or {},
            'coordinate': coordinate,
            'lht_analysis': lht_analysis
        }
    
    def retrieve_memory(self, coordinate: str) -> Optional[Dict[str, Any]]:
        """Retrieve memory by coordinate."""
        # Check Layer 0 first
        if coordinate.startswith('L0'):
            return self.layer0.verses.get(coordinate)
        
        # Check other layers
        for layer_num, layer_data in self.layers.items():
            if coordinate in layer_data:
                return layer_data[coordinate]
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory engine statistics."""
        return {
            'layer0_verses': len(self.layer0.verses),
            'tech_patterns': len(self.ramah.tech_lexicon),
            'coordinates_total': len(self.coordinate_space.coordinates),
            'lht_cache_size': len(self.lht_cache),
            'layers': {
                f'L{i}': len(data) for i, data in self.layers.items()
            }
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo():
    """Demonstrate Ezekiel Memory Engine with full LHT integration."""
    print("="*70)
    print("EZEKIEL AI MEMORY ENGINE - LHT INTEGRATED")
    print("="*70)
    
    # Initialize engine
    engine = EzekielMemoryEngine()
    
    # Load Scripture
    verses_loaded = engine.load_scripture()
    
    # Show stats
    print("\n" + "="*70)
    print("ENGINE STATUS")
    print("="*70)
    stats = engine.get_stats()
    print(f"Layer 0 (Scripture): {stats['layer0_verses']} verses")
    print(f"TECH Lexicon: {stats['tech_patterns']} code patterns")
    print(f"Total coordinates: {stats['coordinates_total']}")
    print(f"LHT cache: {stats['lht_cache_size']} analyses")
    
    # Demo Ramah queries
    print("\n" + "="*70)
    print("RAMAH QUERY DEMONSTRATIONS")
    print("="*70)
    
    # Query 1: Search Scripture
    print("\n1. Search Scripture for 'faith':")
    print("-" * 70)
    result = engine.query_ramah("""RAMAH: SEARCH "faith"
LEXICON: KJV
RETURN: list""")
    
    if result['status'] == 'success':
        print(f"Found {result['count']} results:")
        for r in result['results'][:3]:
            print(f"  {r['reference']} - {r['text'][:60]}...")
    
    # Query 2: LHT ANALYZE
    print("\n2. Run LHT ANALYZE on Ezekiel 37:1-5:")
    print("-" * 70)
    result = engine.query_ramah("""RAMAH: ANALYZE "Ezekiel 37:1-5"
LEXICON: KJV""")
    
    if result['status'] == 'success':
        analysis = result['analysis']
        print(f"Spiral: {analysis['spiral']}")
        print(f"Movement: {analysis['quadrant_movement']}")
        print(f"Gravity Sync: {analysis['gravity_sync']['score']}/3")
        print(f"Pattern Seeds: {[s['symbol'] for s in analysis['pattern_seeds']]}")
        print(f"\nSummary: {analysis['summary']}")
    
    # Query 3: ECHO trace
    print("\n3. ECHO trace for 'WATER' symbol:")
    print("-" * 70)
    result = engine.query_ramah("""RAMAH: ECHO "WATER"
RETURN: summary""")
    
    if result['status'] == 'success':
        print(f"Arc: {result['overall_arc']}")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nEzekiel Memory Engine with LHT is OPERATIONAL!")
    print("Ready for Morning Star integration")


if __name__ == '__main__':
    demo()
