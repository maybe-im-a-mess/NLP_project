import csv
import re
import random


def prepare_data(file):
    rows = []
    with open(file, 'r') as data:
        reader = csv.reader(data)
        header = next(reader)
        for row in reader:
            rows.append(row)
    for row in rows:
        del row[:3]
        row[0] = re.sub(r"https?\S+", r"link", row[0])
        row[0] = re.sub("\W", " ", row[0])
        row[0] = re.sub("\s+", " ", row[0])
        row[0] = row[0].lower().strip()
    return rows


def split_data(clean_data):
    random.shuffle(clean_data)
    train_data = clean_data[:int((len(clean_data) + 1) * .80)]  # Remaining 80% to training set
    test_data = clean_data[int((len(clean_data) + 1) * .80):]  # Splits 20% data to test set

    return train_data, test_data


def create_vocabulary(train_data):
    vocabulary = []
    for row in train_data:
        comment = row[0].split(" ")
        for word in comment:
            if word not in vocabulary:
                vocabulary.append(word)
    return vocabulary


def count_words(data, vocabulary):
    word_counts = dict()

    for word in vocabulary:
        word_counts[word] = [0] * len(data)

    for index, message in enumerate(data):
        words = message.split(" ")
        for word in words:
            word_counts[word][index] += 1  # increment frequency if word found

    return word_counts


def separate_spam_ham(train_data):
    spam, ham = list(), list()

    for i in range(len(train_data)):
        comment = train_data[i][0]
        comment_class = train_data[i][1]

        if comment_class == '0':  # ham
            ham.append(comment)
        else:
            spam.append(comment)

    return spam, ham


def calculate_constants(spam, ham, vocabulary, train_data):
    p_spam = len(spam) / len(train_data)
    p_ham = len(ham) / len(train_data)

    n_spam = 0  # sum of all words in spam messages
    for row in spam:
        words = row.split(" ")
        n_spam += len(words)

    n_ham = 0  # sum of all words in ham messages
    for row in ham:
        words = row.split(" ")
        n_ham += len(words)

    n_vocabulary = len(vocabulary)

    constants = {"p_spam": p_spam,
                 "p_ham": p_ham,
                 "n_spam": n_spam,
                 "n_ham": n_ham,
                 "n_vocab": n_vocabulary}

    return constants


def calculate_parameters(spam, ham, vocabulary, constants, alpha=1):
    spam_parameters = dict()
    spam_word_counts = count_words(spam, vocabulary)

    ham_parameters = dict()
    ham_word_counts = count_words(ham, vocabulary)

    # calculate p_word_given_[spam|ham] for each word
    for unique_word in vocabulary:
        n_word_given_spam = sum(spam_word_counts[unique_word])
        spam_parameters[unique_word] = (
            n_word_given_spam + alpha) / (constants["n_spam"] + alpha * constants["n_vocab"])

        n_word_given_ham = sum(ham_word_counts[unique_word])
        ham_parameters[unique_word] = (
            n_word_given_ham + alpha) / (constants["n_ham"] + alpha * constants["n_vocab"])

    return spam_parameters, ham_parameters


def classify(comment, constants, spam_parameters, ham_parameters):
    # check input validity
    if type(comment) is not str:
        print("Invalid input!")
        return None

    # clean input
    comment = re.sub("\W", " ", comment)
    comment = re.sub("\s+", " ", comment)
    comment = comment.lower().strip()

    words = comment.split(" ")

    p_spam_given_message = constants["p_spam"]
    p_ham_given_message = constants["p_ham"]

    for word in words:
        if word in spam_parameters:
            p_spam_given_message *= spam_parameters[word]

        if word in ham_parameters:
            p_ham_given_message *= ham_parameters[word]

    if p_spam_given_message > p_ham_given_message:
        print("Spam")
    elif p_spam_given_message < p_ham_given_message:
        print("Ham")
    else:
        print("Equal probabilities!")

    print(f"Probability of spam: {p_spam_given_message}")
    print(f"Probability of ham: {p_ham_given_message}")


if __name__ == "__main__":
    clean_data = prepare_data("youtube_combined.csv")
    train_data, test_data = split_data(clean_data)
    vocabulary = create_vocabulary(train_data)
    spam, ham = separate_spam_ham(train_data)
    constants = calculate_constants(spam, ham, vocabulary, train_data)
    spam_parameters, ham_parameters = calculate_parameters(spam, ham, vocabulary, constants)

    classify("Check out my channel", constants, spam_parameters, ham_parameters)
