""" Naive Bayes """
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import itertools
from scipy.stats import norm
import scipy.stats
from sklearn.naive_bayes import GaussianNB
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

iris = sns.load_dataset("iris")

sns.FacetGrid(iris, hue="species").map(
    plt.scatter, "sepal_length", "sepal_width", ).add_legend()
plt.title('Scatter plot')
df1 = iris[["sepal_length", "sepal_width", 'species']]


def predict_NB_gaussian_class(X, mu_list, std_list, pi_list):
    # Returns the class for which the Gaussian Naive Bayes objective function has greatest value
    scores_list = []
    classes = len(mu_list)

    for p in range(classes):
        score = (norm.pdf(x=X[0], loc=mu_list[p][0][0], scale=std_list[p][0][0])
                 * norm.pdf(x=X[1], loc=mu_list[p][0][1], scale=std_list[p][0][1])
                 * pi_list[p])
        scores_list.append(score)

    return np.argmax(scores_list)


def predict_Bayes_class(X, mu_list, sigma_list):
    # Returns the predicted class from an optimal bayes classifier - distributions must be known
    scores_list = []
    classes = len(mu_list)

    for p in range(classes):
        score = scipy.stats.multivariate_normal.pdf(
            X, mean=mu_list[p], cov=sigma_list[p])
        scores_list.append(score)

    return np.argmax(scores_list)


mu_list = np.split(df1.groupby('species').mean().values, [1, 2])
std_list = np.split(df1.groupby('species').std().values, [1, 2], axis=0)
pi_list = df1.iloc[:, 2].value_counts().values / len(df1)

# Our 2-dimensional distribution will be over variables X and Y
N = 100
X = np.linspace(4, 8, N)
Y = np.linspace(1.5, 5, N)
X, Y = np.meshgrid(X, Y)

#fig = plt.figure(figsize = (10,10))
#ax = fig.gca()
color_list = ['Blues', 'Greens', 'Reds']
my_norm = colors.Normalize(vmin=-1., vmax=1.)

g = sns.FacetGrid(iris, hue="species", palette='colorblind').map(
    plt.scatter, "sepal_length", "sepal_width",) .add_legend()
my_ax = g.ax

# Computing the predicted class function for each value on the grid
zz = np.array([predict_NB_gaussian_class(np.array([xx, yy]).reshape(-1, 1), mu_list, std_list, pi_list)
               for xx, yy in zip(np.ravel(X), np.ravel(Y))])

# Reshaping the predicted class into the meshgrid shape
Z = zz.reshape(X.shape)
print(Z)
# Plot the filled and boundary contours
my_ax.contourf(X, Y, Z, 2, alpha=.1, colors=('blue', 'green', 'red'))
my_ax.contour(X, Y, Z, 2, alpha=1, colors=('blue', 'green', 'red'))

# Addd axis and title
my_ax.set_xlabel('Sepal length')
my_ax.set_ylabel('Sepal width')
my_ax.set_title('Gaussian Naive Bayes decision boundaries')

plt.show()
