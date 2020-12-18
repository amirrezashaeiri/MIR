import numpy as np
from math import exp, sqrt, pi, log
from operator import itemgetter


def gaussian_probability(x, mean, stdev):
    stdev += 1
    exponent = exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
    return (1 / (sqrt(2 * pi) * stdev)) * exponent


class Classifier:
    def __init__(self, train_features, train_labels, test_features=None, test_labels=None):
        self.train_features = train_features
        self.train_labels = train_labels

        self.test_features = test_features
        self.test_labels = test_labels
        self.test_predictions = None

    def train(self):
        pass

    def predict(self, test_features):
        pass

    def evaluate(self):
        TP, TN, FP, FN = 0, 0, 0, 0
        for test_label, test_prediction in zip(self.test_labels, self.test_predictions):
            if test_label == test_prediction:
                if test_label == 1:
                    TP += 1
                elif test_label == -1:
                    TN += 1
            elif test_label != test_prediction:
                if test_label == 1:
                    FN += 1
                elif test_label == -1:
                    FP += 1
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        F1 = (2 * precision * recall) / (precision + recall)
        print("Precision: {p}, "
              "Recall: {r}, "
              "Accuracy: {a}, "
              "F1: {f1}".format(p=precision, r=recall, a=accuracy, f1=F1))


class NaiveBayes(Classifier):
    def __init__(self, train_features, train_labels, test_features=None, test_labels=None):
        super().__init__(train_features, train_labels, test_features, test_labels)
        self.label_feature_summaries = dict()
        self.label_dictionary = dict()

    def create_label_dictionary(self):
        for label, features in zip(self.train_labels, self.train_features):
            if label not in self.label_dictionary:
                self.label_dictionary[label] = []
            self.label_dictionary[label] += [features]

    def summarize_dataset(self, label, documents):
        summaries = [(np.mean(column), np.std(column), len(column)) for column in zip(*documents)]
        self.label_feature_summaries[label] = summaries

    def create_label_summaries(self):
        for label in self.label_dictionary:
            self.summarize_dataset(label, self.label_dictionary[label])

    def train(self):
        self.create_label_dictionary()
        self.create_label_summaries()
        return

    def predict_one(self, ind, test):
        total_doc_count = len(self.train_features)
        class_probabilities = dict()
        for label in self.label_feature_summaries:
            label_summary = self.label_feature_summaries[label]
            class_probabilities[label] = log(label_summary[0][-1] / total_doc_count)
            for feature, feature_summary in zip(test, label_summary):
                mean, std, _ = feature_summary
                class_probabilities[label] += log(gaussian_probability(feature, mean, std))
        self.test_predictions[ind] = max(class_probabilities.items(), key=itemgetter(1))[0]

    def predict(self, test_features=None):
        if self.test_features is None:
            self.test_features = test_features
        self.test_predictions = [None for _ in self.test_features]
        for i in range(len(self.test_features)):
            self.predict_one(i, self.test_features[i])


train_features = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 3, 3, 3, 3]]
train_labels = [1, 1, -1]
test_features = [[2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 4, 4, 4], [5, 2, 7, 5, 2]]
test_labels = [1, 1, -1, -1]
NB = NaiveBayes(train_features=train_features,
                train_labels=train_labels,
                test_features=test_features,
                test_labels=test_labels)
NB.train()
NB.predict()
NB.evaluate()
