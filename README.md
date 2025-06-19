# Synonyms: Fast Semantic Similarity Engine

## 1. WHAT IS THIS PROJECT? 
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

## 4. How to test this project

1. **Set up your environment**
   - (Recommended) Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
2. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov black ruff
   ```
3. **Run the tests**
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```
   - This runs all tests and shows a coverage report.
4. **Lint and format your code**
   - Check formatting:
     ```bash
     black --check src tests
     ```
   - Lint with Ruff:
     ```bash
     ruff src tests
     ```
5. **(Optional) Enable pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   - This will auto-run Black and Ruff before every commit.
6. **Check CI on GitHub**
   - Every push or pull request will run tests and linters automatically via GitHub Actions.

## 5. Benchmarks / Results
- On the supplied TOEFL-style test set, this engine achieves **~76% accuracy** (rerun with your own corpus for best results).
- Robust to missing words and empty vectors (returns 0.0 similarity).

## 6. Roadmap & contribution guidelines
- Planned: more similarity functions, phrase-level descriptors, and web API.
- Contributions welcome! Please open issues or PRs for bugs, features, or docs.
- Run `pre-commit install` after cloning to enable auto-formatting and linting.

