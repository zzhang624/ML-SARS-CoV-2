# ML-SARS-CoV-2

The IPYNB file is the source code for the article [Machine Learning Reveals the Critical Interactions for SARS-CoV-2 Spike Protein Binding to ACE2](https://pubs.acs.org/doi/full/10.1021/acs.jpclett.1c01494).

<p align="center">
  <img src="https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/fig_results/fig_abstract.jpeg">
</p>

We trained ML classifiers to distinguish between the configurations from the SARS-CoV and SARS-CoV-2 molecular dynamics simulations and, in the process, rate the importance of each feature to the classification. The feature importance profile hence reveals specific residues that exemplify the different behaviors of the two RBDs.

For input features, we used inverse contact distances between residues in the RBD and in ACE2, emphasizing the differences between interacting residues across the interface. A residue pair was included only if its distance between heavy atoms on ACE2 and RBD ever fell below 15 Å, resulting in a data set of 4886 features. The distance of 15 Å is large enough to capture all contacts between the RBD and ACE2 and also to provide a reasonable speed for ML training. 

To minimize the bias from a particular model and increase robustness of the results, three different architectures of supervised ML classifiers were used: a linear logistic regression (LR) model, a tree-based random forest (RF) model, and a multilayer perceptron (MLP) neural network.

The three classifiers were trained to distinguish configurations of SARS-CoV RBD bound to ACE2 from those of SARS-CoV-2 RBD bound to ACE2. Highly correlated features were deleted before training. Different choices of removal generate different input data sets, which leads to different importance profiles. The choices of deletion were shuffled multiple times, and the resulting importance profiles were averaged until they were found to be converged: ![alt text](https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/fig_results/shuffle.png?raw=true) The feature importance profiles were extracted from three classifiers, allowing us to focus on distinct RBD residues. The results from each model were compared against each other for cross-validation:![alt text](https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/fig_results/final.png?raw=true)


## Machine learning details

The contact distances, defined as the closest distance between heavy atoms of residues on
the ACE2 and RBD region of spike protein were extracted from the simulation trajectories.
Only residue pairs with distances less than 15 ˚A in at least one frame were used as features
for machine learning, forming a dataset of 4886 features. The distances were inverted and
normalized to have a mean of 0 and standard deviation of 1. Highly correlated features were
removed with a threshold of 0.9. Specifically, we calculated the correlation matrix of input
features, keeping the upper (right) triangular matrix without the main diagonal (to avoid
duplication and correlation with themselves). We removed a column (i.e., feature), if any
element(s) in the column of the upper triangular matrix is/are larger than the threshold
value. While the order of columns (features) in the matrix is not relevant for the ML, it does
affect which features are removed during this process, which can produce different profiles.
The order of columns also influenced the number of removed features, which was ∼3300.

Different choices of removal led to different datasets and importance profiles. Converged
results were derived by averaging the importance profiles of different datasets generated
by shuffling the choices 20 times. Because all machine learning methods used
here are supervised learning, all data points were labeled as CoV or CoV-2. We tuned
the hyperparameters for each ML approach to reach an accuracy of 1, i.e., all frames were
correctly classified as from SARS-CoV or SARS-CoV-2 simulations. The residue importance
was derived by summing the importance of distance pairs containing a given residue and
normalizing the results to have a maximum of 1.

### Logistic Regression

Logistic regression (LR) is similar to linear regression but uses a sigmoidal function,
<p align="center">
  <img width="450" src="https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/equations/LR.jpg">
</p>
where X is an inputted 
feature and Y is the output whose range is between 0 and 1. In
classification, the data points are classified according to an output threshold value of 0.5.
The LR implementation in the scikit-learn library was used. The importance of a feature
is the corresponding weight (β1 to βp, normalized) in equation. When dividing data into
training and test sets, different random states led to different importance profiles in the LR
classifier.
Bootstrapping was used to generate multiple training sets and to obtain
converged average importance profiles in the LR classifier:
<p align="center">
  <img src="https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/fig_results/LR_converge.png">
</p>

### Random Forest

A random forest (RF) is composed of multiple decision trees. The classification result of
one random forest is decided by the majority vote from all of the decision trees. During the
training process, the decision tree algorithm iteratively searches features and determines a
threshold value to split the dataset in such a way that the lowest Gini impurity as possible is
obtained in each internal node. A lower Gini impurity of the split data indicates that more
information is obtained. The importance of a feature is calculated as the total reduction of
the Gini impurity contributed by this feature. The RF classifier has an internal bootstrapping process and generates consistent profiles: 
<p align="center">
  <img width="450" src="https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/fig_results/RF_compare.png">
</p>
We implemented RF through the
scikit-learn library. We included 500 trees in our model and generated bootstrap samples
when building trees. The maximum depth of each tree was 60 and the number of features
considered in each node was set to 50.

### Multilayer Perceptron and Layer-Wise Relevance Propagation

A multilayer perceptron (MLP) is a type of feed-forward artificial neural network. Compared to linear classification or regression models, an MLP includes extra hidden layer(s) of
perceptrons (nodes) between input and output layers. Except for the input layer, each node
uses a nonlinear activation function to deal with the signals propagated from the previous
layer. We used the scikit-learn implementation of MLP. We set one hidden layer with 55
nodes (roughly the square root of the product of the number of input nodes number and
output nodes) using the Rectified Linear Unit (ReLU) as the activation function. ReLU was
chosen because it is faster, capable of outputting true zero, and easier to optimize than sigmoid or tanh activation functions. Labels were one-hot encoded. During training, Adam, a stochastic gradient-based optimizer, was used to optimize weights between nodes. Feature
importance was extracted from MLP using Layer-Wise Relevance Propagation (LRP). If
MLP makes a correct prediction or classification, LRP determines which features contribute
more to this decision than others. LRP propagates
relevance R from the output layer to the input layer thought the weights of the network and
neural activations. The propagation follows the LPR-0 rule:
<p align="center">
  <img width="300" src="https://github.com/zzhang624/ML-SARS-CoV-2/blob/main/equations/LRP.jpg">
</p>
where
Rk and Rj are the relevances of two neurons in one layer and the previous layer, separately,
and aj is the activation and wjk is the weight between two neurons. The importance of one
feature is calculated from the average relevance of the corresponding input neuron over all
frames.
