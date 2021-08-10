# ML-SARS-CoV-2

Here is the sourse code for the article [Machine Learning Reveals the Critical Interactions for SARS-CoV-2 Spike Protein Binding to ACE2](https://pubs.acs.org/doi/full/10.1021/acs.jpclett.1c01494).

We trained ML classifiers to distinguish between the configurations from the SARS-CoV and SARS-CoV-2 trajectories and, in the process, rate the importance of each feature to the classification. The feature importance profile hence reveals specific residues that exemplify the different behaviors of the two RBDs.

For input features, we used inverse contact distances between residues in the RBD and in ACE2, emphasizing the differences between interacting residues across the interface. A residue pair was included only if its distance between heavy atoms on ACE2 and RBD ever fell below 15 Å, resulting in a data set of 4886 features. The distance of 15 Å is large enough to capture all contacts between the RBD and ACE2 and also to provide a reasonable speed for ML training. 

To minimize the bias from a particular model and increase robustness of the results, three different architectures of supervised ML classifiers were used: a linear logistic regression (LR) model, a tree-based random forest (RF) model, and a multilayer perceptron (MLP) neural network.

The three classifiers were trained to distinguish configurations of SARS-CoV RBD bound to ACE2 from those of SARS-CoV-2 RBD bound to ACE2. Highly correlated features were deleted before training. Different choices of removal generate different input data sets, which leads to different importance profiles. The choices of deletion were shuffled multiple times, and the resulting importance profiles were averaged until they were found to be converged (Figure S6). The feature importance profiles were extracted from three classifiers, allowing us to focus on distinct RBD residues. The results from each model were compared against each other for cross-validation.
