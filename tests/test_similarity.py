import pytest
import os
from synonyms import (
    build_semantic_descriptors_from_files,
    run_similarity_test,
    cosine_similarity,
    most_similar_word,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'syn_tests')

# List of test files for positive-path tests (none available yet)
CORPUS_FILES = [
    os.path.join(DATA_DIR, f)
    for f in [
        'c_file1.txt',
        'c_file2.txt',
        'c_file3.txt',
    ]
]

# All c_dummy_test*.txt files are negative-path: just check for non-negative score
DUMMY_TEST_FILES = [
    os.path.join(DATA_DIR, f)
    for f in [
        'c_dummy_test1.txt',
        'c_dummy_test2.txt',
        'c_dummy_test3.txt',
        'c_dummy_test4.txt',
        'c_dummy_test5.txt',
    ]
]

def test_dummy_files_no_crash():
    descriptors = build_semantic_descriptors_from_files(CORPUS_FILES)
    for test_file in DUMMY_TEST_FILES:
        score = run_similarity_test(test_file, descriptors, cosine_similarity)
        assert score >= 0.0, f"Score should be non-negative for {test_file}"

# If you add real multi-question test files, add an accuracy assertion here.

def test_cosine_similarity_empty():
    assert cosine_similarity({}, {}) == 0.0
    assert cosine_similarity({'a': 1}, {}) == 0.0
    assert cosine_similarity({}, {'b': 2}) == 0.0

def test_most_similar_word_missing():
    descriptors = {'a': {'b': 1}, 'b': {'a': 1}}
    # 'c' is missing from descriptors
    result = most_similar_word('c', ['a', 'b'], descriptors, cosine_similarity)
    assert result in ['a', 'b']
    # All choices missing
    result = most_similar_word('a', ['x', 'y'], descriptors, cosine_similarity)
    assert result == 'x'  # defaults to first choice 