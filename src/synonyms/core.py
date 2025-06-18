"""
Core semantic similarity functions for the synonyms package.

Implements vector-based similarity, semantic descriptor building, and evaluation utilities.
"""

from __future__ import annotations
from typing import Callable, Sequence, Mapping, Any
import math
from collections import Counter
from itertools import combinations


def cosine_similarity(vec1: Mapping[str, float], vec2: Mapping[str, float]) -> float:
    """
    Compute the cosine similarity between two sparse vectors.

    Args:
        vec1: First vector as a mapping from terms to weights.
        vec2: Second vector as a mapping from terms to weights.

    Returns:
        Cosine similarity as a float in [0, 1]. Returns 0.0 if either vector is zero.
    """
    dot_product = sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in set(vec1) | set(vec2))
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)


def build_semantic_descriptors(sentences: Sequence[Sequence[str]]) -> dict[str, dict[str, int]]:
    """
    Build semantic descriptors for each word based on co-occurrence in sentences.

    Args:
        sentences: A sequence of sentences, each a sequence of words.

    Returns:
        A dictionary mapping each word to a Counter of co-occurring words.
    """
    descriptors: dict[str, Counter[str]] = {}
    for sentence in sentences:
        unique_words = set(sentence)
        for w1, w2 in combinations(unique_words, 2):
            for a, b in [(w1, w2), (w2, w1)]:
                if a not in descriptors:
                    descriptors[a] = Counter()
                descriptors[a][b] += 1
    # Convert Counters to dicts for compatibility
    return {k: dict(v) for k, v in descriptors.items()}


def build_semantic_descriptors_from_files(filenames: Sequence[str]) -> dict[str, dict[str, int]]:
    """
    Build semantic descriptors from a list of text files.

    Args:
        filenames: List of file paths to read.

    Returns:
        Semantic descriptors as produced by build_semantic_descriptors.
    """
    sentences: list[list[str]] = []
    for file_name in filenames:
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read().lower()
        for p in ["!", "?", "."]:
            text = text.replace(p, ".")
        for p in [",", "-", "--", ":", ";"]:
            text = text.replace(p, " ")
        for sentence in text.split('.'):
            words = sentence.split()
            if words:
                sentences.append(words)
    return build_semantic_descriptors(sentences)


def most_similar_word(
    word: str,
    choices: Sequence[str],
    semantic_descriptors: Mapping[str, Mapping[str, int]],
    similarity_fn: Callable[[Mapping[str, int], Mapping[str, int]], float],
) -> str:
    """
    Return the choice most similar to the given word using the provided similarity function.

    Args:
        word: The target word.
        choices: List of candidate words.
        semantic_descriptors: Mapping of word to its semantic descriptor.
        similarity_fn: Function to compute similarity between two descriptors.

    Returns:
        The most similar word from choices.
    """
    best_choice = choices[0]
    max_similarity = float('-inf')
    for choice in choices:
        if word in semantic_descriptors and choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            similarity = 0.0
        if similarity > max_similarity:
            max_similarity = similarity
            best_choice = choice
    return best_choice


def run_similarity_test(
    filename: str,
    semantic_descriptors: Mapping[str, Mapping[str, int]],
    similarity_fn: Callable[[Mapping[str, int], Mapping[str, int]], float],
) -> float:
    """
    Evaluate the accuracy of the most_similar_word function on a test file.

    Args:
        filename: Path to the test file.
        semantic_descriptors: Mapping of word to its semantic descriptor.
        similarity_fn: Function to compute similarity between two descriptors.

    Returns:
        Percentage of correct answers as a float.
    """
    correct = 0
    total = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            if len(words) >= 3:
                guess = most_similar_word(words[0], words[2:], semantic_descriptors, similarity_fn)
                if guess == words[1]:
                    correct += 1
                total += 1
    return (correct / total) * 100.0 if total else 0.0 