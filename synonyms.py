
import math

def cosine_similarity(vec1, vec2):
    dot_product = 0
    mag_vec1 = 0
    mag_vec2 = 0

    # Calculate the dot product
    for key in vec1:
        if key in vec2:
            dot_product += vec1[key] * vec2[key]

    # Calculate the magnitudes of each vectoir
    for value in vec1.values():
        mag_vec1 += value ** 2

    for value in vec2.values():
        mag_vec2 += value ** 2

    if mag_vec1 == 0 or mag_vec2 == 0:
        return -1  # Cannot compute similarity

    # square rooting them so its actually the magnitude :O
    mag_vec1 = mag_vec1 ** 0.5
    mag_vec2 = mag_vec2 ** 0.5

    return dot_product / (mag_vec1 * mag_vec2)


def build_semantic_descriptors(sentences):
    d = {}

    for sentence in sentences:

        # gets the unique words in each sentence
        only_words = set(sentence)

        # iterate through each word in the unique words set
        for word in only_words:
            # initialize a dictionary for each word in d
            if word not in d:
                d[word] = {}

            # count how often each word appears in this sentence, except for the pivot word, "word"
            for samesent_word in only_words:
                if samesent_word != word:
                    
                    # add count to each word, unless it already exists then set count to 1
                    if samesent_word in d[word]:
                        d[word][samesent_word] += 1
                    else:
                        d[word][samesent_word] = 1
    return d


def build_semantic_descriptors_from_files(filenames):
    sentences = []

    # loop to iterate through each file
    for file_name in filenames:

        # read each file
        f = open(file_name, 'r')
        text = f.read()
        f.close()

        # set all of its contents to lower case (since the meaning of words doesn't depend on case)
        text = text.lower()

        # Replace sentence-ending punctuation with periods
        text = text.replace("!", ".")
        text = text.replace("?", ".")

        # Replace specified all the punctuation with spaces
        text = text.replace(",", " ")
        text = text.replace("-", " ")
        text = text.replace("--", " ")
        text = text.replace(":", " ")
        text = text.replace(";", " ")

        # Split into sentences
        sentenceslist = text.split('.')

        for sentence in sentenceslist:
            words = sentence.split()

            # Makes sure im not appending empty list of words
            if words:
                sentences.append(words)

    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = -1
    best_choice = choices[0]  # Default to the first choice

    for choice in choices:
        if word in semantic_descriptors and choice in semantic_descriptors:
            # compares target word with each choise using the similarity_fn
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            # if the target word and the choice are not in semantic_descriptors, their similarity can't be computed
            # therefore set the similarity to -1
            similarity = -1

            #
        if similarity > max_similarity:
            # continuously update the best choice depending on similarity values
            max_similarity = similarity
            best_choice = choice
    return best_choice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    numberQs = 0

    f = open(filename, 'r')
    for line in f:
        words = line.strip().split()
        if len(words) >= 3:
            guess = most_similar_word(words[0], words[2:], semantic_descriptors, similarity_fn)
            if guess == words[1]:
                correct += 1
            numberQs += 1
    f.close()

    if numberQs == 0:
        return 0.0
    return (correct / numberQs) * 100.0
