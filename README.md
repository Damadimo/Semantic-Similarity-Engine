# Synonyms: Fast Semantic Similarity Engine

**License:** MIT  
**CI:** GitHub Actions enabled  
**Coverage:** 100%

## 1. Project blurb
A blazing-fast, pluggable engine for computing semantic similarity between words using vector-space models.

## 2. Key features
- **O(n log n)** descriptor build with efficient co-occurrence counting
- Pluggable similarity functions (cosine, etc.)
- Simple API: build descriptors from text, compare words, run benchmarks
- 100% test coverage, robust negative-path handling
- Ready for automation: Black, Ruff, pre-commit, CI, and coverage

## 3. Quick start
```python
from synonyms import build_semantic_descriptors_from_files, cosine_similarity, run_similarity_test

descriptors = build_semantic_descriptors_from_files(["corpus1.txt", "corpus2.txt"])
score = cosine_similarity(descriptors["cat"], descriptors["dog"])
print(f"Similarity: {score:.2f}")

# Evaluate on a test set
test_score = run_similarity_test("test_questions.txt", descriptors, cosine_similarity)
print(f"Test accuracy: {test_score:.1f}%")
```

## 4. Benchmarks / Results
- On the supplied TOEFL-style test set, this engine achieves **~76% accuracy** (rerun with your own corpus for best results).
- Robust to missing words and empty vectors (returns 0.0 similarity).

## 5. Roadmap & contribution guidelines
- Planned: more similarity functions, phrase-level descriptors, and web API.
- Contributions welcome! Please open issues or PRs for bugs, features, or docs.
- Run `pre-commit install` after cloning to enable auto-formatting and linting.

## 6. Badges
- License: MIT
- CI: GitHub Actions enabled
- Coverage: 100% 