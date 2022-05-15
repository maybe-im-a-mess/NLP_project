from spam_filter import *


def test_filter(test_data, constants, spam_parameters, ham_parameters):
    classified_data = []
    for i in range(len(test_data)):
        comment = test_data[i][0]
        classified_comment = classify(comment, constants, spam_parameters, ham_parameters)
        classified_data.append(classified_comment)

    return classified_data


def confusion_matrix(classified_data, test_data):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(test_data)):
        comment_class = train_data[i][1]
        if comment_class == '0':           # ham
            if test_data[i][1] == classified_data[i]:
                tn += 1
            if test_data[i][1] != classified_data[i]:
                fp += 1

        if comment_class == '1':           # spam
            if test_data[i][1] == classified_data[i]:
                tp += 1
            if test_data[i][1] != classified_data[i]:
                fn += 1

    return tp, tn, fp, fn


def calculate_accuracy(test_data, tp, tn, fp, fn):
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    return accuracy


def calculate_precision(test_data, tp, fp):
    precision = tp / (tp + fp)

    return precision


def calculate_recall(test_data, tp, fn):
    recall = tp / (tp + fn)

    return recall


def calculate_f1(precision, recall):
    f1 = 2 * precision * recall / (precision + recall)

    return f1


if __name__ == "__main__":
    clean_data = prepare_data("youtube_combined.csv")
    train_data, test_data = split_data(clean_data)
    vocabulary = create_vocabulary(test_data)
    spam, ham = separate_spam_ham(test_data)
    constants = calculate_constants(spam, ham, vocabulary, test_data)
    spam_parameters, ham_parameters = calculate_parameters(spam, ham, vocabulary, constants)
    classified_data = test_filter(test_data, constants, spam_parameters, ham_parameters)

    tp, tn, fp, fn = confusion_matrix(classified_data, test_data)
    precision = calculate_precision(test_data, tp, fp)
    recall = calculate_recall(test_data, tp, fn)

    print("Accuracy is ", calculate_accuracy(test_data, tp, tn, fp, fn))
    print("Precision is ", precision)
    print("Recall is ", recall)
    print("F1 is ", calculate_f1(precision, recall))
