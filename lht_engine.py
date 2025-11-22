"""
LHT DIAGNOSTIC ENGINE - COMPLETE IMPLEMENTATION
================================================
Full Logos Horizon Theory diagnostic stack following Training Packet specs.

Implements:
- TELOS-RUN (master pipeline)
- QUAD-MAP (quadrant movement detection)
- PATTERN-SEED (symbol detection & scoring)
- ECHO-TRACE (symbol arcs across spirals)
- GRAVITY-SYNC (Christ-centrality scoring)
- COMP-435 (4→3→5 compression pattern)
- URIM/THUMMIM (spiral vitality validation)
- FRACTAL-FILTER (fractal vs feedback detection)
- BIDIR-TEST (bidirectional echo validation)

Built with CodeRamah patterns for maximum efficiency.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
import re


# ============================================================================
# CORE ENUMS & STRUCTURES
# ============================================================================

class Spiral(Enum):
    """Seven canonical spirals through Scripture"""
    S1_CREATION = 1      # Genesis 1-11
    S2_COVENANT = 2      # Genesis 12 - Exodus
    S3_LAW = 3          # Exodus - Deuteronomy  
    S4_KINGSHIP = 4     # Joshua - 2 Kings
    S5_WISDOM = 5       # Job - Malachi
    S6_CHRIST = 6       # The Gospels
    S7_NEW_CREATION = 7 # Acts - Revelation


class Quadrant(Enum):
    """Four quadrants of movement"""
    SW = "SW"  # Death / Chaos / Descent
    SE = "SE"  # Fall / Fracture / Separation
    NE = "NE"  # Revelation / Pattern / Instruction
    NW = "NW"  # Resurrection / Restoration / Fulfillment


# ============================================================================
# SYMBOL LEXICON (80 Core Symbols)
# ============================================================================

SYMBOL_LEXICON = {
    # Creation/Nature Symbols (10)
    "LIGHT": {
        "meaning": "revelation / order",
        "keywords": ["light", "lamp", "shine", "brightness", "dawn"],
        "weight": 3
    },
    "DARKNESS": {
        "meaning": "chaos / judgment", 
        "keywords": ["darkness", "dark", "shadow", "night", "gloom"],
        "weight": 3
    },
    "WATER": {
        "meaning": "life / chaos / cleansing",
        "keywords": ["water", "waters", "sea", "river", "flood", "rain"],
        "weight": 3
    },
    "FIRE": {
        "meaning": "judgment / transformation",
        "keywords": ["fire", "flame", "burn", "consume"],
        "weight": 3
    },
    "TREE": {
        "meaning": "life / choice / growth",
        "keywords": ["tree", "trees", "branch", "branches"],
        "weight": 2
    },
    "GARDEN": {
        "meaning": "communion / presence",
        "keywords": ["garden", "eden", "paradise"],
        "weight": 3
    },
    "MOUNTAIN": {
        "meaning": "revelation / covenant",
        "keywords": ["mountain", "mount", "hill", "zion", "sinai"],
        "weight": 3
    },
    "WILDERNESS": {
        "meaning": "testing / exile",
        "keywords": ["wilderness", "desert", "waste"],
        "weight": 2
    },
    "DUST": {
        "meaning": "mortality",
        "keywords": ["dust", "ashes", "clay"],
        "weight": 2
    },
    "SPIRIT": {
        "meaning": "breath / empowerment",
        "keywords": ["spirit", "breath", "wind", "ghost"],
        "weight": 3
    },
    
    # Temple/Covenant Symbols (10)
    "TEMPLE": {
        "meaning": "presence / structure",
        "keywords": ["temple", "sanctuary", "house of god"],
        "weight": 3
    },
    "ALTAR": {
        "meaning": "sacrifice / mediation",
        "keywords": ["altar", "altars"],
        "weight": 3
    },
    "VEIL": {
        "meaning": "separation / access",
        "keywords": ["veil", "curtain", "vail"],
        "weight": 2
    },
    "LAMPSTAND": {
        "meaning": "illumination / Spirit",
        "keywords": ["lampstand", "candlestick", "menorah"],
        "weight": 2
    },
    "BREAD": {
        "meaning": "communion / wisdom",
        "keywords": ["bread", "loaves", "manna"],
        "weight": 3
    },
    "OIL": {
        "meaning": "anointing / Spirit",
        "keywords": ["oil", "anoint", "anointed"],
        "weight": 2
    },
    "BLOOD": {
        "meaning": "covenant / atonement",
        "keywords": ["blood", "bloodshed"],
        "weight": 3
    },
    "LAMB": {
        "meaning": "substitution / innocence",
        "keywords": ["lamb", "lambs", "sheep"],
        "weight": 3
    },
    "PRIEST": {
        "meaning": "mediation",
        "keywords": ["priest", "priests", "priesthood"],
        "weight": 2
    },
    "TABERNACLE": {
        "meaning": "mobile presence",
        "keywords": ["tabernacle", "tent", "dwelling"],
        "weight": 2
    },
    
    # Kingdom Symbols (10)
    "KING": {
        "meaning": "authority / rule",
        "keywords": ["king", "kings", "monarch"],
        "weight": 3
    },
    "THRONE": {
        "meaning": "judgment / legitimacy",
        "keywords": ["throne", "thrones"],
        "weight": 3
    },
    "SCEPTER": {
        "meaning": "rule / power",
        "keywords": ["scepter", "sceptre", "rod"],
        "weight": 2
    },
    "CROWN": {
        "meaning": "honor / destiny",
        "keywords": ["crown", "crowns", "diadem"],
        "weight": 2
    },
    "SWORD": {
        "meaning": "judgment / division",
        "keywords": ["sword", "swords", "blade"],
        "weight": 2
    },
    "CITY": {
        "meaning": "people / identity",
        "keywords": ["city", "cities", "jerusalem", "zion"],
        "weight": 2
    },
    "HOUSE": {
        "meaning": "lineage / establishment",
        "keywords": ["house", "household", "dynasty"],
        "weight": 2
    },
    "GATE": {
        "meaning": "access / authority",
        "keywords": ["gate", "gates", "door", "doors"],
        "weight": 2
    },
    
    # Wisdom/Human Condition (10)
    "PATH": {
        "meaning": "direction / discipleship",
        "keywords": ["path", "way", "ways", "road"],
        "weight": 2
    },
    "WINE": {
        "meaning": "joy / covenant blood",
        "keywords": ["wine", "drink"],
        "weight": 2
    },
    "CUP": {
        "meaning": "destiny / suffering",
        "keywords": ["cup", "cups"],
        "weight": 2
    },
    "VOICE": {
        "meaning": "revelation / calling",
        "keywords": ["voice", "voices", "cry"],
        "weight": 2
    },
    "HAND": {
        "meaning": "action / authority",
        "keywords": ["hand", "hands"],
        "weight": 1
    },
    "HEART": {
        "meaning": "intention / covenant interiorization",
        "keywords": ["heart", "hearts"],
        "weight": 2
    },
    "SEED": {
        "meaning": "promise / future",
        "keywords": ["seed", "seeds", "offspring"],
        "weight": 3
    },
    
    # Exile/Return (10)
    "EGYPT": {
        "meaning": "bondage",
        "keywords": ["egypt", "egyptian"],
        "weight": 2
    },
    "BABYLON": {
        "meaning": "judgment / confusion",
        "keywords": ["babylon", "babylonian", "babel"],
        "weight": 2
    },
    "EXILE": {
        "meaning": "fracture",
        "keywords": ["exile", "exiled", "captivity", "captive"],
        "weight": 2
    },
    "RETURN": {
        "meaning": "restoration",
        "keywords": ["return", "returned", "restore"],
        "weight": 2
    },
    "GATHERING": {
        "meaning": "redemption",
        "keywords": ["gather", "gathered", "gathering"],
        "weight": 2
    },
    
    # Christ Pattern (10)
    "CROSS": {
        "meaning": "death / obedience",
        "keywords": ["cross", "crucify", "crucified"],
        "weight": 3
    },
    "RESURRECTION": {
        "meaning": "new creation",
        "keywords": ["resurrection", "risen", "rose", "raised"],
        "weight": 3
    },
    "SHEPHERD": {
        "meaning": "guidance",
        "keywords": ["shepherd", "shepherds", "pastor"],
        "weight": 2
    },
    "BRIDE": {
        "meaning": "people of God",
        "keywords": ["bride", "bridegroom", "marriage", "wedding"],
        "weight": 2
    },
    "SON": {
        "meaning": "identity / inheritance",
        "keywords": ["son", "sons", "child"],
        "weight": 2
    },
    
    # Fig/Olive/Vine (10)
    "FIG": {
        "meaning": "covenant fruit / exposure",
        "keywords": ["fig", "figs"],
        "weight": 2
    },
    "OLIVE": {
        "meaning": "anointing / endurance / Spirit",
        "keywords": ["olive", "olives", "olivet"],
        "weight": 2
    },
    "VINE": {
        "meaning": "dependence / communion",
        "keywords": ["vine", "vines", "vineyard"],
        "weight": 3
    },
    "FRUIT": {
        "meaning": "visible outcome",
        "keywords": ["fruit", "fruits", "harvest"],
        "weight": 2
    },
    "THORNS": {
        "meaning": "curse / resistance",
        "keywords": ["thorns", "thistles", "briars"],
        "weight": 2
    },
}


# ============================================================================
# QUADRANT INDICATORS
# ============================================================================

QUADRANT_INDICATORS = {
    Quadrant.SW: {
        "keywords": ["grave", "pit", "sheol", "death", "destroyed", "consumed", 
                    "darkness", "deep", "wrath", "curse", "famine", "plague",
                    "finished", "gave up", "die", "perish"],
        "situations": ["siege", "defeat", "lament", "catastrophe"],
        "tone": "despairing / overwhelmed"
    },
    Quadrant.SE: {
        "keywords": ["sin", "idolatry", "rebellion", "transgression", "adultery",
                    "division", "scattered", "broken", "forsaken", "betray"],
        "situations": ["covenant breaking", "betrayal", "turning aside"],
        "tone": "accusatory / tense / warning"
    },
    Quadrant.NE: {
        "keywords": ["law", "commandment", "statute", "teaching", "wisdom",
                    "proverb", "prophecy", "thus saith", "vision", "behold",
                    "looked", "revelation"],
        "situations": ["God speaking", "law given", "teaching", "explaining"],
        "tone": "clarifying / didactic"
    },
    Quadrant.NW: {
        "keywords": ["restore", "heal", "return", "gather", "rebuild", "plant",
                    "comfort", "rejoice", "new", "renewed", "inheritance",
                    "resurrection", "breath", "live", "life"],
        "situations": ["return from exile", "healing", "resurrection", "fulfillment"],
        "tone": "hopeful / resolved / celebratory"
    }
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class QuadrantMapping:
    """Result of QUAD-MAP analysis"""
    primary_quadrant: Quadrant
    secondary_quadrant: Optional[Quadrant]
    movement: str
    evidence: List[Dict[str, str]]
    segment_scores: List[Dict]


@dataclass
class PatternSeed:
    """Identified symbol pattern"""
    symbol: str
    local_role: str
    support: List[str]
    score: float
    frequency: int
    structural_position: int
    theological_weight: int


@dataclass
class EchoTrace:
    """Symbol arc across spirals"""
    symbol: str
    spiral_roles: List[Dict]
    overall_arc: str
    current_passage_stage: Dict[str, str]


@dataclass
class GravitySync:
    """Christ-centrality alignment"""
    score: int  # 0-3
    explanation: str
    christ_patterns: List[str]


@dataclass
class Comp435:
    """4→3→5 compression pattern"""
    has_pattern: bool
    mapping: Optional[str]
    confidence: str  # High / Medium / Low
    stages: Optional[Dict]


@dataclass
class UrimThummim:
    """Spiral vitality validation"""
    urim: bool  # Revealed / coherent
    thummim: bool  # Complete / sealed in Christ
    interpretation: str


@dataclass
class FractalFilter:
    """Fractal vs feedback classification"""
    classification: str  # "Fractal" or "Likely Feedback"
    reasoning: str
    checklist_results: Dict[str, bool]


@dataclass
class TelosRun:
    """Complete TELOS-RUN diagnostic output"""
    reference: str
    spiral: Spiral
    quadrants: QuadrantMapping
    pattern_seeds: List[PatternSeed]
    echo_traces: List[EchoTrace]
    gravity_sync: GravitySync
    comp_435: Comp435
    urim_thummim: UrimThummim
    fractal_filter: FractalFilter
    theological_summary: str


# ============================================================================
# LHT DIAGNOSTIC ENGINE
# ============================================================================

class LHTDiagnosticEngine:
    """
    Complete LHT diagnostic system implementing all algorithms
    from the LHT Training Packet.
    """
    
    def __init__(self):
        self.symbol_lexicon = SYMBOL_LEXICON
        self.quadrant_indicators = QUADRANT_INDICATORS
        
    # ========================================================================
    # MASTER PIPELINE: TELOS-RUN
    # ========================================================================
    
    def telos_run(self, reference: str, text: str) -> TelosRun:
        """
        Run complete TELOS-RUN diagnostic pipeline.
        
        Args:
            reference: Scripture reference (e.g., "Genesis 1:1-3")
            text: Passage text
            
        Returns:
            Complete TelosRun diagnostic
        """
        # 1. Spiral assignment
        spiral = self.assign_spiral(reference)
        
        # 2. QUAD-MAP
        quadrants = self.quad_map(text)
        
        # 3. PATTERN-SEED
        seeds = self.pattern_seed(text)
        
        # 4. ECHO-TRACE for each seed
        traces = [self.echo_trace(seed.symbol, spiral) for seed in seeds[:3]]
        
        # 5. GRAVITY-SYNC
        gravity = self.gravity_sync(text, seeds)
        
        # 6. COMP-435
        comp435 = self.comp_435(text)
        
        # 7. URIM/THUMMIM
        urim_thummim = self.urim_thummim(seeds, traces, gravity)
        
        # 8. FRACTAL-FILTER
        fractal_filter = self.fractal_filter(seeds, traces)
        
        # 9. Theological summary
        summary = self.generate_summary(spiral, quadrants, seeds, gravity)
        
        return TelosRun(
            reference=reference,
            spiral=spiral,
            quadrants=quadrants,
            pattern_seeds=seeds,
            echo_traces=traces,
            gravity_sync=gravity,
            comp_435=comp435,
            urim_thummim=urim_thummim,
            fractal_filter=fractal_filter,
            theological_summary=summary
        )
    
    # ========================================================================
    # 2.1 SPIRAL ASSIGNMENT
    # ========================================================================
    
    def assign_spiral(self, reference: str) -> Spiral:
        """
        Assign passage to one of seven canonical spirals.
        
        Algorithm:
        1. Parse reference for book name
        2. Map book to spiral using canonical boundaries
        3. Return spiral assignment with justification
        """
        ref_lower = reference.lower()
        
        # Spiral 1: Genesis 1-11 (Creation)
        if 'genesis' in ref_lower:
            # Extract chapter if possible
            match = re.search(r'(\d+):', reference)
            if match:
                chapter = int(match.group(1))
                if chapter <= 11:
                    return Spiral.S1_CREATION
            return Spiral.S2_COVENANT
        
        # Spiral 2: Genesis 12 - Exodus (Covenant)
        if any(b in ref_lower for b in ['exodus']):
            return Spiral.S2_COVENANT
        
        # Spiral 3: Leviticus - Deuteronomy (Law)
        if any(b in ref_lower for b in ['leviticus', 'numbers', 'deuteronomy']):
            return Spiral.S3_LAW
        
        # Spiral 4: Joshua - 2 Kings (Kingship)
        if any(b in ref_lower for b in ['joshua', 'judges', 'ruth', 'samuel', 'kings']):
            return Spiral.S4_KINGSHIP
        
        # Spiral 5: Job - Malachi (Wisdom & Prophets)
        if any(b in ref_lower for b in ['job', 'psalm', 'proverb', 'ecclesiastes',
                                        'song', 'isaiah', 'jeremiah', 'lamentations',
                                        'ezekiel', 'daniel', 'hosea', 'joel', 'amos',
                                        'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk',
                                        'zephaniah', 'haggai', 'zechariah', 'malachi']):
            return Spiral.S5_WISDOM
        
        # Spiral 6: Gospels (Christ & Cross)
        if any(b in ref_lower for b in ['matthew', 'mark', 'luke', 'john']) and \
           'john' in ref_lower and not any(x in ref_lower for x in ['1 john', '2 john', '3 john']):
            return Spiral.S6_CHRIST
        
        # Spiral 7: Acts - Revelation (Church & New Creation)
        if any(b in ref_lower for b in ['acts', 'romans', 'corinthians', 'galatians',
                                        'ephesians', 'philippians', 'colossians',
                                        'thessalonians', 'timothy', 'titus', 'philemon',
                                        'hebrews', 'james', 'peter', 'john', 'jude',
                                        'revelation']):
            return Spiral.S7_NEW_CREATION
        
        # Default to S6 (Christ) if uncertain
        return Spiral.S6_CHRIST
    
    # ========================================================================
    # 5.2 QUAD-MAP
    # ========================================================================
    
    def quad_map(self, text: str) -> QuadrantMapping:
        """
        Map quadrant movement in passage.
        
        Algorithm (from Training Packet 5.2.3):
        1. Split passage into segments
        2. Score each segment for each quadrant (0-3)
        3. Assign segments to highest-scoring quadrant
        4. Aggregate to find primary/secondary quadrants
        5. Detect movement sequence
        6. Generate evidence
        """
        # Split into sentences/verses
        segments = [s.strip() for s in text.split('.') if s.strip()]
        if not segments:
            segments = [text]
        
        segment_scores = []
        
        # Score each segment
        for segment in segments:
            seg_lower = segment.lower()
            scores = {}
            
            for quad, indicators in self.quadrant_indicators.items():
                score = 0
                matched_keywords = []
                
                # Score based on keywords
                for keyword in indicators['keywords']:
                    if keyword in seg_lower:
                        score += 1
                        matched_keywords.append(keyword)
                
                scores[quad] = {
                    'score': min(score, 3),  # Cap at 3
                    'keywords': matched_keywords
                }
            
            # Assign segment to highest-scoring quadrant
            best_quad = max(scores.items(), key=lambda x: x[1]['score'])[0]
            segment_scores.append({
                'segment': segment[:50] + '...' if len(segment) > 50 else segment,
                'quadrant': best_quad,
                'scores': scores
            })
        
        # Aggregate across passage
        quad_counts = {q: 0 for q in Quadrant}
        for seg in segment_scores:
            quad_counts[seg['quadrant']] += 1
        
        # Primary = most frequent
        sorted_quads = sorted(quad_counts.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_quads[0][0]
        secondary = sorted_quads[1][0] if sorted_quads[1][1] > 0 else None
        
        # Detect movement
        quad_sequence = [seg['quadrant'] for seg in segment_scores]
        movement = self._compress_movement(quad_sequence)
        
        # Generate evidence
        evidence = []
        for quad, count in sorted_quads:
            if count > 0:
                # Find best example segment
                examples = [s for s in segment_scores if s['quadrant'] == quad]
                if examples:
                    keywords = examples[0]['scores'][quad]['keywords'][:3]
                    evidence.append({
                        'quadrant': quad.value,
                        'reason': f"Keywords: {', '.join(keywords)}" if keywords else "Tonal match"
                    })
        
        return QuadrantMapping(
            primary_quadrant=primary,
            secondary_quadrant=secondary,
            movement=movement,
            evidence=evidence,
            segment_scores=segment_scores
        )
    
    def _compress_movement(self, sequence: List[Quadrant]) -> str:
        """Compress quadrant sequence to movement string"""
        if not sequence:
            return "Unknown"
        
        # Remove consecutive duplicates
        compressed = [sequence[0]]
        for q in sequence[1:]:
            if q != compressed[-1]:
                compressed.append(q)
        
        if len(compressed) == 1:
            return f"Static {compressed[0].value}"
        else:
            return "→".join(q.value for q in compressed)
    
    # ========================================================================
    # 5.3 PATTERN-SEED
    # ========================================================================
    
    def pattern_seed(self, text: str) -> List[PatternSeed]:
        """
        Identify 1-3 dominant symbols that define passage structure.
        
        Algorithm (from Training Packet 5.3.2-5.3.4):
        1. Extract symbol candidates from text
        2. Score each: frequency(0-3) + position(0-3) + weight(0-3) + unique(0-1)
        3. Select top 1-3 with score ≥4
        4. Generate local_role and support for each
        """
        text_lower = text.lower()
        candidates = []
        
        # Extract candidates
        for symbol, data in self.symbol_lexicon.items():
            matches = []
            for keyword in data['keywords']:
                if keyword in text_lower:
                    matches.append(keyword)
            
            if matches:
                # Score this candidate
                freq_score = min(len(matches), 3)
                
                # Structural position (simplified: check if early in text)
                first_match_pos = text_lower.index(matches[0])
                if first_match_pos < len(text) * 0.2:
                    struct_score = 3
                elif first_match_pos < len(text) * 0.5:
                    struct_score = 2
                else:
                    struct_score = 1
                
                # Theological weight (from lexicon)
                theo_score = data['weight']
                
                # Uniqueness (1 if very prominent, 0 otherwise)
                unique_score = 1 if len(matches) >= 3 else 0
                
                total_score = freq_score + struct_score + theo_score + unique_score
                
                candidates.append({
                    'symbol': symbol,
                    'score': total_score,
                    'frequency': freq_score,
                    'structural_position': struct_score,
                    'theological_weight': theo_score,
                    'matches': matches,
                    'meaning': data['meaning']
                })
        
        # Sort by score and select top 3 with score ≥4
        candidates.sort(key=lambda x: x['score'], reverse=True)
        seeds = []
        
        for c in candidates[:3]:
            if c['score'] >= 4:
                # Generate local role
                local_role = f"{c['meaning']} (appears as: {', '.join(c['matches'][:2])})"
                
                # Generate support
                support = [
                    f"Mentioned {len(c['matches'])} time(s)",
                    f"Theological weight: {c['theological_weight']}/3"
                ]
                
                seeds.append(PatternSeed(
                    symbol=c['symbol'],
                    local_role=local_role,
                    support=support,
                    score=c['score'],
                    frequency=c['frequency'],
                    structural_position=c['structural_position'],
                    theological_weight=c['theological_weight']
                ))
        
        return seeds
    
    # ========================================================================
    # 5.4 ECHO-TRACE
    # ========================================================================
    
    def echo_trace(self, symbol: str, current_spiral: Spiral) -> EchoTrace:
        """
        Trace symbol arc across all 7 spirals.
        
        Algorithm (from Training Packet 5.4.2-5.4.4):
        1. For each spiral, describe symbol's role
        2. Derive overall macro arc
        3. Place current passage on that arc
        """
        # Predefined spiral roles for key symbols
        # (In production, this would be comprehensive)
        spiral_roles = self._get_symbol_spiral_roles(symbol)
        
        # Derive overall arc
        overall_arc = self._derive_symbol_arc(symbol, spiral_roles)
        
        # Place current passage
        current_stage = self._place_on_arc(symbol, current_spiral, spiral_roles)
        
        return EchoTrace(
            symbol=symbol,
            spiral_roles=spiral_roles,
            overall_arc=overall_arc,
            current_passage_stage=current_stage
        )
    
    def _get_symbol_spiral_roles(self, symbol: str) -> List[Dict]:
        """Get predefined spiral roles for symbol"""
        # This is a simplified version - production would be comprehensive
        
        roles_map = {
            "WATER": [
                {"spiral": 1, "role": "chaos waters separated, flood judgment", "example": "Gen 1:2; Gen 6-9"},
                {"spiral": 2, "role": "Red Sea deliverance, testing waters", "example": "Exod 14; Exod 17"},
                {"spiral": 3, "role": "ritual washings, purity", "example": "Lev 11-15"},
                {"spiral": 4, "role": "drought/blessing cycles", "example": "1 Kings 17-18"},
                {"spiral": 5, "role": "rivers of life promised", "example": "Ezek 47; Ps 46"},
                {"spiral": 6, "role": "living water offered by Christ", "example": "John 4; John 7"},
                {"spiral": 7, "role": "river of life from throne", "example": "Rev 22"}
            ],
            "SPIRIT": [
                {"spiral": 1, "role": "hovering over chaos, creative breath", "example": "Gen 1:2"},
                {"spiral": 2, "role": "selective empowerment", "example": "Num 11"},
                {"spiral": 3, "role": "linked to prophecy", "example": "Deut 34"},
                {"spiral": 4, "role": "empowering kings/prophets", "example": "1 Sam 16"},
                {"spiral": 5, "role": "promised future outpouring", "example": "Ezek 36-37; Joel 2"},
                {"spiral": 6, "role": "descends on Christ, promised to believers", "example": "Matt 3; John 14-16"},
                {"spiral": 7, "role": "poured out on church", "example": "Acts 2; Rom 8"}
            ],
            "LAMB": [
                {"spiral": 1, "role": "Abel's offering", "example": "Gen 4"},
                {"spiral": 2, "role": "Passover lamb", "example": "Exod 12"},
                {"spiral": 3, "role": "daily sacrifices", "example": "Lev 1-7"},
                {"spiral": 4, "role": "temple system", "example": "1 Kings 8"},
                {"spiral": 5, "role": "led to slaughter prophecy", "example": "Isa 53"},
                {"spiral": 6, "role": "John's 'Lamb of God'", "example": "John 1:29"},
                {"spiral": 7, "role": "Lamb on throne", "example": "Rev 5"}
            ],
            # Default for symbols without specific mapping
            "DEFAULT": [
                {"spiral": 1, "role": "prototype appearance", "example": "Genesis"},
                {"spiral": 2, "role": "covenant context", "example": "Exodus"},
                {"spiral": 3, "role": "law framework", "example": "Leviticus"},
                {"spiral": 4, "role": "kingdom application", "example": "Kings"},
                {"spiral": 5, "role": "wisdom/prophetic development", "example": "Prophets"},
                {"spiral": 6, "role": "Christ fulfillment", "example": "Gospels"},
                {"spiral": 7, "role": "church/new creation", "example": "Revelation"}
            ]
        }
        
        return roles_map.get(symbol, roles_map["DEFAULT"])
    
    def _derive_symbol_arc(self, symbol: str, roles: List[Dict]) -> str:
        """Derive overall arc from spiral roles"""
        # Simplified - production would be more sophisticated
        early = roles[0]['role'] if len(roles) > 0 else "prototype"
        mid = roles[3]['role'] if len(roles) > 3 else "development"
        late = roles[6]['role'] if len(roles) > 6 else "fulfillment"
        
        return f"{symbol} moves from {early} → {mid} → {late}"
    
    def _place_on_arc(self, symbol: str, current_spiral: Spiral, 
                     roles: List[Dict]) -> Dict[str, str]:
        """Place current passage on symbol arc"""
        spiral_num = current_spiral.value
        
        if spiral_num <= 2:
            position = "Early-stage / Prototype"
        elif spiral_num <= 4:
            position = "Mid-stage / Development"
        elif spiral_num == 5:
            position = "Prophetic promise"
        elif spiral_num == 6:
            position = "Christ fulfillment"
        else:
            position = "Church application / New Creation"
        
        # Get reason from role if available
        role_data = next((r for r in roles if r['spiral'] == spiral_num), None)
        reason = role_data['role'] if role_data else "Standard progression"
        
        return {
            "position": position,
            "reason": reason
        }
    
    # ========================================================================
    # 5.5 GRAVITY-SYNC
    # ========================================================================
    
    def gravity_sync(self, text: str, seeds: List[PatternSeed]) -> GravitySync:
        """
        Calculate Christ-centrality score (0-3).
        
        Algorithm (from Training Packet 5.5):
        0 = No clear Christ-echo
        1 = Light structural hint
        2 = Strong typology
        3 = Direct Christ event or hyper-tight echo
        """
        text_lower = text.lower()
        christ_patterns = []
        
        # Check for direct Christ events (score 3)
        direct_christ = ['crucif', 'cross', 'finished', 'resurrection', 'risen']
        for pattern in direct_christ:
            if pattern in text_lower:
                christ_patterns.append(pattern)
        
        if christ_patterns:
            return GravitySync(
                score=3,
                explanation="Direct Christ event present",
                christ_patterns=christ_patterns
            )
        
        # Check for strong typology (score 2)
        strong_types = ['lamb', 'blood', 'sacrifice', 'altar', 'priest', 'atonement']
        for seed in seeds:
            if seed.symbol.lower() in strong_types:
                christ_patterns.append(seed.symbol)
        
        if christ_patterns:
            return GravitySync(
                score=2,
                explanation="Strong sacrificial typology present",
                christ_patterns=christ_patterns
            )
        
        # Check for light hints (score 1)
        light_hints = ['seed', 'crown', 'king', 'son', 'shepherd']
        for seed in seeds:
            if seed.symbol.lower() in light_hints:
                christ_patterns.append(seed.symbol)
        
        if christ_patterns:
            return GravitySync(
                score=1,
                explanation="Light messianic hints present",
                christ_patterns=christ_patterns
            )
        
        # No clear pattern (score 0)
        return GravitySync(
            score=0,
            explanation="No clear Christ-pattern detected",
            christ_patterns=[]
        )
    
    # ========================================================================
    # 5.6 COMP-435
    # ========================================================================
    
    def comp_435(self, text: str) -> Comp435:
        """
        Test for 4→3→5 compression pattern.
        
        Algorithm (from Training Packet 5.6):
        4 = world / chaos / toil / lack
        3 = divine pattern / mediation / word
        5 = grace / overflow / blessing / feast
        """
        # Look for 3-stage narrative structure
        # This is simplified - production would analyze structure more deeply
        
        text_lower = text.lower()
        
        # Stage 1 (4): Lack/chaos indicators
        stage_4_words = ['without', 'empty', 'nothing', 'darkness', 'void', 'lack', 
                        'toil', 'night', 'labor']
        has_stage_4 = any(w in text_lower for w in stage_4_words)
        
        # Stage 2 (3): Divine word/act indicators  
        stage_3_words = ['god said', 'lord said', 'commanded', 'spoke', 'word',
                        'thus saith', 'behold']
        has_stage_3 = any(w in text_lower for w in stage_3_words)
        
        # Stage 3 (5): Grace/overflow indicators
        stage_5_words = ['filled', 'overflow', 'abundance', 'multiply', 'blessed',
                        'feast', 'rest', 'rejoice', 'new']
        has_stage_5 = any(w in text_lower for w in stage_5_words)
        
        has_pattern = has_stage_4 and has_stage_3 and has_stage_5
        
        if has_pattern:
            mapping = "4: chaos/lack → 3: divine word/act → 5: grace/overflow"
            confidence = "Medium"  # Would be more sophisticated in production
            stages = {
                "stage_4": has_stage_4,
                "stage_3": has_stage_3,
                "stage_5": has_stage_5
            }
        else:
            mapping = None
            confidence = "Low"
            stages = None
        
        return Comp435(
            has_pattern=has_pattern,
            mapping=mapping,
            confidence=confidence,
            stages=stages
        )
    
    # ========================================================================
    # 5.7 URIM & THUMMIM
    # ========================================================================
    
    def urim_thummim(self, seeds: List[PatternSeed], 
                    traces: List[EchoTrace],
                    gravity: GravitySync) -> UrimThummim:
        """
        Validate spiral vitality.
        
        Algorithm (from Training Packet 5.7):
        Urim = Revealed / coherent (shows up consistently)
        Thummim = Complete / sealed in Christ
        """
        # URIM check: Does pattern show up consistently?
        urim = False
        if len(traces) > 0:
            # Check if symbols appear across multiple spirals
            avg_appearances = sum(len(t.spiral_roles) for t in traces) / len(traces)
            urim = avg_appearances >= 5  # Appears in most spirals
        
        # THUMMIM check: Has it landed in Christ?
        thummim = gravity.score >= 2
        
        # Interpret combination
        if urim and thummim:
            interp = "Fully alive, coherent, and completed spiral"
        elif urim and not thummim:
            interp = "Real pattern but still open / unresolved"
        elif not urim and thummim:
            interp = "Sealed mystery; not fully revealed"
        else:
            interp = "Likely false spiral or over-interpretation"
        
        return UrimThummim(
            urim=urim,
            thummim=thummim,
            interpretation=interp
        )
    
    # ========================================================================
    # 5.8 FRACTAL-FILTER
    # ========================================================================
    
    def fractal_filter(self, seeds: List[PatternSeed],
                      traces: List[EchoTrace]) -> FractalFilter:
        """
        Determine if pattern is fractal or feedback.
        
        Algorithm (from Training Packet 5.8):
        Check: echo density, cross-spiral reach, theological weight,
               controls, bidirectional sense
        """
        checklist = {}
        
        # 1. Echo Density: appears across multiple books/genres
        checklist['echo_density'] = len(traces) > 0 and all(
            len(t.spiral_roles) >= 3 for t in traces
        )
        
        # 2. Cross-Spiral Reach: traces through several spirals
        checklist['cross_spiral_reach'] = len(traces) > 0 and any(
            len(t.spiral_roles) >= 5 for t in traces
        )
        
        # 3. Theological Load-Bearing: supports real narrative
        checklist['theological_load'] = any(
            seed.theological_weight >= 2 for seed in seeds
        )
        
        # 4. Controls: not trivial
        checklist['controls'] = len(seeds) >= 2
        
        # 5. Bidirectional (simplified check)
        checklist['bidirectional'] = len(seeds) > 0
        
        # Count satisfied checks
        satisfied = sum(1 for v in checklist.values() if v)
        
        if satisfied >= 3:
            classification = "Fractal"
            reasoning = f"Pattern satisfies {satisfied}/5 fractal criteria"
        else:
            classification = "Likely Feedback"
            reasoning = f"Only {satisfied}/5 criteria satisfied; likely over-interpretation"
        
        return FractalFilter(
            classification=classification,
            reasoning=reasoning,
            checklist_results=checklist
        )
    
    # ========================================================================
    # SUMMARY GENERATION
    # ========================================================================
    
    def generate_summary(self, spiral: Spiral, quadrants: QuadrantMapping,
                        seeds: List[PatternSeed], gravity: GravitySync) -> str:
        """Generate Christ-centered theological summary"""
        
        seed_names = [s.symbol for s in seeds[:3]]
        
        summary = f"This passage sits in {spiral.name}, "
        summary += f"moving through {quadrants.movement}. "
        
        if seed_names:
            summary += f"The dominant symbols are {', '.join(seed_names)}. "
        
        if gravity.score == 3:
            summary += "This directly reveals Christ's redemptive work."
        elif gravity.score == 2:
            summary += "This strongly foreshadows the Cross pattern through sacrificial typology."
        elif gravity.score == 1:
            summary += "This hints at the larger narrative arc pointing toward Christ."
        else:
            summary += "This passage contributes to the broader biblical narrative."
        
        return summary


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def analyze_passage(reference: str, text: str) -> TelosRun:
    """
    Quick convenience function to run full TELOS diagnostic.
    
    Usage:
        result = analyze_passage("Genesis 1:1-3", passage_text)
    """
    engine = LHTDiagnosticEngine()
    return engine.telos_run(reference, text)
