#!/usr/bin/env python3
"""
PRIME Scanner: Detect coherence and fidelity in text entities

Measures:
- Token frequency (base 1 Hz analog)
- Pattern repetition (coherence - ξ)
- Information density (fidelity - φ)

Usage:
    prime_scan.py <file_or_text>
    prime_scan.py README.md
    prime_scan.py "This is a test sentence"
"""

import sys
import os
from collections import Counter
import math

def calculate_coherence(word_freq, total_words):
    """
    Coherence (ξ): Pattern repetition vs uniqueness
    
    High coherence = words repeat often (strong patterns)
    Low coherence = words mostly unique (chaotic/novel)
    """
    unique_words = len(word_freq)
    
    # Simple coherence: How much do words repeat?
    coherence = 1 - (unique_words / total_words)
    
    return round(coherence, 3)

def calculate_fidelity(word_freq, total_words):
    """
    Fidelity (φ): Information preservation quality
    
    Uses entropy as proxy for information density
    Golden ratio (1.618) represents ideal balance
    """
    # Calculate Shannon entropy
    entropy = 0
    for count in word_freq.values():
        probability = count / total_words
        entropy -= probability * math.log2(probability)
    
    # Max possible entropy for this corpus
    max_entropy = math.log2(total_words) if total_words > 0 else 1
    
    # Normalize and scale to golden ratio range
    # entropy/max_entropy gives us 0-1, scale to approximate phi
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    # Map to phi scale: 
    # High entropy (diverse) → higher phi (rich documentation)
    # Low entropy (repetitive) → lower phi (compressed)
    fidelity = normalized_entropy * 2.0  # Scale to ~0-2 range
    
    return round(fidelity, 3)

def interpret_coherence(xi):
    """Interpret coherence value"""
    if xi >= 0.8:
        return "🌟 Excellent - Crystal-like patterns"
    elif xi >= 0.7:
        return "⭐ Strong - Clear patterns"
    elif xi >= 0.5:
        return "💫 Moderate - Emerging patterns"
    elif xi >= 0.3:
        return "✨ Low - Mixed/Novel"
    else:
        return "💠 Minimal - Highly unique/chaotic"

def interpret_fidelity(phi):
    """Interpret fidelity value"""
    golden = 1.618
    if abs(phi - golden) < 0.1:
        return "🎯 Golden Ratio - Ideal documentation"
    elif phi > 2.0:
        return "🎪 Over-documented - May contain noise"
    elif phi > 1.4:
        return "📊 Rich - High information density"
    elif phi > 0.8:
        return "📝 Adequate - Good preservation"
    else:
        return "⚠️  Sparse - Potential information loss"

def scan_entity(text):
    """Scan text for PRIME metrics"""
    # Tokenize (simple word splitting)
    words = text.lower().split()
    total_words = len(words)
    
    if total_words == 0:
        return {
            'coherence_xi': 0.0,
            'fidelity_phi': 0.0,
            'total_tokens': 0,
            'unique_tokens': 0,
            'dominant_frequencies': [],
            'interpretation_xi': "No content",
            'interpretation_phi': "No content"
        }
    
    unique_words = len(set(words))
    
    # Frequency analysis
    word_freq = Counter(words)
    
    # Calculate metrics
    coherence = calculate_coherence(word_freq, total_words)
    fidelity = calculate_fidelity(word_freq, total_words)
    
    # Top frequencies (most common words)
    top_freq = word_freq.most_common(5)
    
    return {
        'coherence_xi': coherence,
        'fidelity_phi': fidelity,
        'total_tokens': total_words,
        'unique_tokens': unique_words,
        'dominant_frequencies': top_freq,
        'interpretation_xi': interpret_coherence(coherence),
        'interpretation_phi': interpret_fidelity(fidelity)
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: prime_scan.py <file_or_text>")
        print("\nExamples:")
        print("  prime_scan.py document.md")
        print('  prime_scan.py "Sample text to analyze"')
        sys.exit(1)
    
    # Try to read as file first, otherwise treat as text
    try:
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                text = f.read()
            source = sys.argv[1]
        else:
            text = ' '.join(sys.argv[1:])
            source = "<text input>"
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
    
    # Scan the entity
    metrics = scan_entity(text)
    
    # Display results
    print("🌟 PRIME Scan Results")
    print(f"Source: {source}")
    print(f"\n{'='*50}")
    print(f"Coherence (ξ):  {metrics['coherence_xi']}")
    print(f"  → {metrics['interpretation_xi']}")
    print(f"\nFidelity (φ):   {metrics['fidelity_phi']}")
    print(f"  → {metrics['interpretation_phi']}")
    print(f"\nTotal Tokens:   {metrics['total_tokens']}")
    print(f"Unique Tokens:  {metrics['unique_tokens']}")
    print(f"Repetition:     {metrics['total_tokens'] - metrics['unique_tokens']}")
    
    print(f"\n{'='*50}")
    print("Dominant Frequencies (Top 5):")
    for word, count in metrics['dominant_frequencies']:
        percentage = (count / metrics['total_tokens']) * 100
        print(f"  '{word}': {count} ({percentage:.1f}%)")
    
    # Overall health assessment
    print(f"\n{'='*50}")
    print("PRIME Health Assessment:")
    
    xi = metrics['coherence_xi']
    phi = metrics['fidelity_phi']
    
    if xi > 0.7 and 0.8 < phi < 2.0:
        print("✅ Entity is HEALTHY")
        print("   Strong coherence, good documentation fidelity")
    elif phi > 2.0:
        print("⚠️  Entity may be OVER-DOCUMENTED")
        print("   Consider condensing or refactoring")
    elif phi < 0.8:
        print("⚠️  Entity may be UNDER-DOCUMENTED")
        print("   Consider adding context or detail")
    elif xi < 0.5:
        print("💡 Entity is NOVEL/EXPLORATORY")
        print("   Low pattern repetition suggests new territory")
    else:
        print("💫 Entity is EMERGING")
        print("   Patterns forming, documentation developing")
    
    print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
