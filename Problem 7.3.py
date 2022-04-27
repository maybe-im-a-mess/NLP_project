import csv
import re


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


def create_vocabulary(data):
    vocabulary = []
    for row in data:
        comment = row[0].split(" ")
        for word in comment:
            if word not in vocabulary:
                vocabulary.append(word)
    return vocabulary


def word_counter(comments, vocabulary):
    counter ={}
    for word in vocabulary:
        counter[word] = [0] * len(comments)
    for index, comment in enumerate(comments):
        words = comment.split(" ")
        for word in words:
            counter[word][index] += 1
    return counter


def separate_spam_ham(data):
    spam, ham = [], []
    for i in range(len(data)):
        comment = data[i][0]
        com_class = data[i][1]

        if com_class == '0':
            ham.append(comment)
        else:
            spam.append(comment)

    return spam, ham


def calculate_constants(spam, ham, vocabulary):
    p_spam = len(spam)
    p_ham = len(ham)

    n_spam = 0
    for comment in spam:
        words = comment.split(" ")
        n_spam += len(words)

    n_ham = 0
    for comment in ham:
        words = comment.split(" ")
        n_ham += len(words)

    n_vocabulary = len(vocabulary)

    constants = {"p_spam": p_spam,
                 "p_ham": p_ham,
                 "n_spam": n_spam,
                 "n_ham": n_ham,
                 "n_vocabulary": n_vocabulary}

    return constants


def calculate_parameters(spam, ham, vocabulary, constants, alpha=1):
    spam_param = {}
    spam_word_counter = word_counter(spam, vocabulary)
    ham_param = {}
    ham_word_counter = word_counter(ham, vocabulary)

    for unique_word in vocabulary:
        n_word_given_spam = sum(spam_word_counter[unique_word])
        spam_param[unique_word] = (n_word_given_spam + alpha) / (constants["n_spam"] + alpha * constants["n_vocabulary"])

        n_word_given_ham = sum(ham_word_counter[unique_word])
        ham_param[unique_word] = (n_word_given_ham + alpha) / (constants["n_ham"] + alpha * constants["n_vocabulary"])

    return spam_param, ham_param


def classify(comment, constants, spam_param, ham_param):
    comment = re.sub('\W', ' ', comment)
    comment = comment.lower().split()

    p_spam_given_comment = constants["p_spam"]
    p_ham_given_comment = constants["p_ham"]

    for word in comment:
        if word in spam_param:
            p_spam_given_comment *= spam_param[word]

        if word in ham_param:
            p_ham_given_comment *= ham_param[word]

    print('Probability of spam: ', p_spam_given_comment)
    print('Probability of ham: ', p_ham_given_comment)

    if p_ham_given_comment > p_spam_given_comment:
        print('Label: Ham')
    elif p_ham_given_comment < p_spam_given_comment:
        print('Label: Spam')
    else:
        print('Equal proabilities!')


if __name__ == "__main__":
    data = prepare_data("youtube_combined.csv")
    vocabulary = create_vocabulary(data)
    spam, ham = separate_spam_ham(data)
    constants = calculate_constants(spam, ham, vocabulary)
    spam_parameters, ham_parameters = calculate_parameters(spam, ham, vocabulary, constants)

    classify("check my channel", constants, spam_parameters, ham_parameters)
