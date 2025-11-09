


#neww

import re
from config.config import ESG_WEIGHTS
from collections import defaultdict
import sys
import platform

# ESG Keywords with scores
ESG_SCORING_KEYWORDS = {
    "environmental": {
        "positive": {
            "carbon reduction": 0.8, "renewable energy": 0.8, "emissions reduction": 0.7,
            "clean energy": 0.7, "sustainability": 0.6, "recycling": 0.5,
            "energy efficiency": 0.6, "green": 0.4, "circular economy": 0.7,
            "net zero": 0.9, "carbon neutral": 0.8, "climate action": 0.7
        },
        "negative": {
            "environmental fine": -1.2, "pollution": -0.8, "spill": -1.0,
            "contamination": -0.9, "emissions increased": -0.8, "non-compliance": -1.0,
            "environmental violation": -1.2, "waste increased": -0.5, "deforestation": -0.9
        }
    },
    "social": {
        "positive": {
            "diversity": 0.7, "inclusion": 0.7, "equal opportunity": 0.8,
            "gender equality": 0.8, "employee wellbeing": 0.6, "work-life balance": 0.5,
            "training programs": 0.6, "community engagement": 0.6, "human rights": 0.8,
            "fair wages": 0.7, "safety programs": 0.7, "employee satisfaction": 0.6
        },
        "negative": {
            "discrimination": -1.2, "harassment": -1.2, "labor violation": -1.0,
            "workplace accident": -0.8, "union dispute": -0.6, "unfair practice": -0.9,
            "child labor": -1.5, "forced labor": -1.5, "unsafe conditions": -1.0, "lawsuit": -0.7
        }
    },
    "governance": {
        "positive": {
            "board independence": 0.8, "transparent": 0.7, "ethics policy": 0.7,
            "compliance program": 0.7, "risk management": 0.6, "audit committee": 0.6,
            "whistleblower": 0.6, "anti-corruption": 0.8, "board diversity": 0.8,
            "stakeholder engagement": 0.6
        },
        "negative": {
            "fraud": -1.5, "corruption": -1.5, "bribery": -1.5,
            "conflict of interest": -0.9, "regulatory fine": -1.0, "governance failure": -1.2,
            "investigation": -0.8, "scandal": -1.0, "insider trading": -1.3, "breach": -0.9
        }
    }
}


def compile_regex_patterns():
    """Pre-compile regex patterns for faster matching"""
    patterns = {}
    for category in ESG_SCORING_KEYWORDS:
        patterns[category] = {
            'positive': {},
            'negative': {}
        }
        for sentiment in ['positive', 'negative']:
            for keyword in ESG_SCORING_KEYWORDS[category][sentiment]:
                # Use word boundaries for more accurate matching
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                patterns[category][sentiment][keyword] = pattern
    return patterns


# Pre-compile patterns once at module load
COMPILED_PATTERNS = compile_regex_patterns()


def calculate_keyword_score_fast(text, category):
    """Ultra-fast keyword scoring using pre-compiled regex"""
    positive = ESG_SCORING_KEYWORDS[category]["positive"]
    negative = ESG_SCORING_KEYWORDS[category]["negative"]
    patterns = COMPILED_PATTERNS[category]

    score = 3.0  # Neutral base
    found_positive, found_negative = [], []

    # Positive keywords - using pre-compiled regex
    for kw, weight in positive.items():
        matches = patterns['positive'][kw].findall(text)
        count = len(matches)
        if count:
            score += weight * min(count, 3)
            found_positive.append(f"{kw} ({count}x)")

    # Negative keywords
    for kw, weight in negative.items():
        matches = patterns['negative'][kw].findall(text)
        count = len(matches)
        if count:
            score += weight * min(count, 2)
            found_negative.append(f"{kw} ({count}x)")

    score = max(1.0, min(5.0, score))
    return {
        "score": round(score, 2), 
        "positive_signals": found_positive, 
        "negative_signals": found_negative
    }


def smart_chunk_text(text, chunk_size=20000):
    """
    Smart chunking that splits on paragraph boundaries
    Larger chunks for faster processing
    """
    chunks = []
    current_chunk = ""
    
    # Split by paragraphs (double newline)
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks if chunks else [text]


def calculate_overall_esg_score(full_text, progress_callback=None, use_parallel=False):
    """
    Optimized ESG score calculation - SEQUENTIAL processing for Windows compatibility
    
    Args:
        full_text (str): Complete document text
        progress_callback (callable): Optional callback(progress, message)
        use_parallel (bool): Ignored on Windows, always uses sequential
    
    Returns:
        dict: ESG scoring results
    """
    try:
        if progress_callback:
            progress_callback(5, "🔍 Preparing text analysis...")
        
        # Smart chunking - larger chunks, fewer iterations
        chunks = smart_chunk_text(full_text, chunk_size=20000)
        num_chunks = len(chunks)
        
        print(f"🔹 Processing {num_chunks} smart chunks (sequential mode)...")
        
        if progress_callback:
            progress_callback(10, f"📄 Analyzing {num_chunks} sections...")
        
        categories = ['environmental', 'social', 'governance']
        
        # Sequential processing (Windows-safe)
        env_scores, soc_scores, gov_scores = [], [], []
        env_pos, env_neg = [], []
        soc_pos, soc_neg = [], []
        gov_pos, gov_neg = [], []
        
        progress_per_chunk = 60 / num_chunks
        
        for i, chunk in enumerate(chunks):
            progress = 15 + int((i + 1) * progress_per_chunk)
            
            # Update progress with category names
            if i % 3 == 0:
                msg = "🌍 Analyzing Environmental factors..."
            elif i % 3 == 1:
                msg = "👥 Analyzing Social factors..."
            else:
                msg = "🏛️ Analyzing Governance factors..."
            
            if progress_callback:
                progress_callback(progress, msg)
            
            # Calculate scores for this chunk
            env = calculate_keyword_score_fast(chunk, "environmental")
            soc = calculate_keyword_score_fast(chunk, "social")
            gov = calculate_keyword_score_fast(chunk, "governance")
            
            env_scores.append(env["score"])
            soc_scores.append(soc["score"])
            gov_scores.append(gov["score"])
            
            # Collect signals
            env_pos.extend(env["positive_signals"])
            env_neg.extend(env["negative_signals"])
            soc_pos.extend(soc["positive_signals"])
            soc_neg.extend(soc["negative_signals"])
            gov_pos.extend(gov["positive_signals"])
            gov_neg.extend(gov["negative_signals"])
        
        if progress_callback:
            progress_callback(80, "📊 Calculating final scores...")
        
        # Average scores across chunks
        env_avg = sum(env_scores) / len(env_scores)
        soc_avg = sum(soc_scores) / len(soc_scores)
        gov_avg = sum(gov_scores) / len(gov_scores)
        
        # Deduplicate signals and take top ones
        env_pos_unique = list(dict.fromkeys(env_pos))[:10]
        env_neg_unique = list(dict.fromkeys(env_neg))[:10]
        soc_pos_unique = list(dict.fromkeys(soc_pos))[:10]
        soc_neg_unique = list(dict.fromkeys(soc_neg))[:10]
        gov_pos_unique = list(dict.fromkeys(gov_pos))[:10]
        gov_neg_unique = list(dict.fromkeys(gov_neg))[:10]
        
        if progress_callback:
            progress_callback(90, "✅ Finalizing results...")
        
        # Calculate weighted overall score
        overall = (
            env_avg * ESG_WEIGHTS["environmental"] +
            soc_avg * ESG_WEIGHTS["social"] +
            gov_avg * ESG_WEIGHTS["governance"]
        )

        # Determine risk level
        if overall >= 4.0:
            risk_level, emoji = "Low Risk", "🟢"
        elif overall >= 3.0:
            risk_level, emoji = "Medium Risk", "🟡"
        else:
            risk_level, emoji = "High Risk", "🔴"

        if progress_callback:
            progress_callback(100, "✅ Analysis complete!")

        return {
            "overall_score": round(overall, 2),
            "risk_level": risk_level,
            "risk_emoji": emoji,
            "environmental": {
                "score": round(env_avg, 2),
                "positive_signals": env_pos_unique,
                "negative_signals": env_neg_unique
            },
            "social": {
                "score": round(soc_avg, 2),
                "positive_signals": soc_pos_unique,
                "negative_signals": soc_neg_unique
            },
            "governance": {
                "score": round(gov_avg, 2),
                "positive_signals": gov_pos_unique,
                "negative_signals": gov_neg_unique
            },
        }

    except Exception as e:
        print(f"❌ Error calculating ESG score: {e}")
        import traceback
        traceback.print_exc()
        if progress_callback:
            progress_callback(100, "❌ Error occurred")
        return None


def generate_score_summary(scores):
    """Create a readable summary of ESG scores"""
    if not scores:
        return "Unable to generate score summary."
    
    env = scores['environmental']
    soc = scores['social']
    gov = scores['governance']
    
    summary = f"""
## {scores['risk_emoji']} ESG Risk Assessment: {scores['risk_level']}
**Overall Score: {scores['overall_score']}/5.0**

### 🌍 Environmental Score: {env['score']}/5.0
**Strengths:** {', '.join(env['positive_signals'][:5]) or 'None identified'}
**Risks:** {', '.join(env['negative_signals'][:5]) or 'None identified'}

### 👥 Social Score: {soc['score']}/5.0
**Strengths:** {', '.join(soc['positive_signals'][:5]) or 'None identified'}
**Risks:** {', '.join(soc['negative_signals'][:5]) or 'None identified'}

### 🏛️ Governance Score: {gov['score']}/5.0
**Strengths:** {', '.join(gov['positive_signals'][:5]) or 'None identified'}
**Risks:** {', '.join(gov['negative_signals'][:5]) or 'None identified'}
"""
    return summary


def analyze_esg_gaps(scores):
    """Analyze weaknesses or gaps based on ESG scores"""
    if not scores:
        return ["Unable to analyze ESG gaps."]
    
    gaps = []

    if scores["environmental"]["score"] < 3.5:
        gaps.append("🌍 Environmental: Strengthen climate action and emissions reduction strategies")
    
    if scores["social"]["score"] < 3.5:
        gaps.append("👥 Social: Enhance diversity, inclusion, and employee wellbeing programs")
    
    if scores["governance"]["score"] < 3.5:
        gaps.append("🏛️ Governance: Improve board independence and transparency mechanisms")
    
    # Check for negative signals
    if scores["environmental"]["negative_signals"]:
        gaps.append("⚠️ Address environmental compliance issues identified")
    
    if scores["social"]["negative_signals"]:
        gaps.append("⚠️ Resolve social/labor-related concerns")
    
    if scores["governance"]["negative_signals"]:
        gaps.append("⚠️ Strengthen governance controls and ethics frameworks")

    if not gaps:
        gaps.append("✅ No major ESG gaps identified. Strong performance across all areas.")

    return gaps