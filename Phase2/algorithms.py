from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
def SVM(X,Y,C):

    # X = [[0, 0], [1, 1]]
    # y = [0, 1]
    clf = svm.SVC(C)
    clf.fit(X, Y)
    return clf
    # clf.predict([[-1, 5]])

#usage : SVM( [[0, 0], [1, 1]],[0, 1],0.5).predict([[-1, 5]])



def random_forrest(X,Y):
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)

    #Train the model using the training sets y_pred=clf.predict(X_test)
    # clf.fit([[0, 0], [1, 1]],[0, 1])
    clf.fit(X,Y)
    return clf
    # y_pred=clf.predict([[1,1]])

#usage : random_forrest([[0, 0], [1, 1]],[0, 1]).predict([[1,1]])