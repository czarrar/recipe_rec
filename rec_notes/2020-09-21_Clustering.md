I want to group the different recipes into meaningful clusters.

# PCA

I compressed the data first by selecting the components that explained 95% of the variance.

## Determining the number of components

Python doesn't appear to have the proper tools to easily determine the number of . In the future, we could be smart about this by using R: https://cran.r-project.org/web/packages/PCDimension/vignettes/PCDimension.pdf.


# Visualize

Sklearns documentation shows some nice examples of different embeddings. From it, 

https://scikit-learn.org/stable/auto_examples/manifold/plot_manifold_sphere.html#sphx-glr-auto-examples-manifold-plot-manifold-sphere-py

I liked this blog page since it shows what I've experienced, which is that t-SNE separates different clusters of high-dimensional data well whereas MDS tends to clump everything together.

https://www.cnblogs.com/jins-note/p/9719157.html

This page gives the plotting of the t-SNE results with seaborn

https://towardsdatascience.com/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b

## Understanding differences of MDS vs t-SNE

I've been trying to find a good spot from which I can understand what's going on here. This resource is awesome!

* https://jakevdp.github.io/PythonDataScienceHandbook/05.10-manifold-learning.html
* For the notebooks: https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/Index.ipynb
* Also this: https://scikit-learn.org/stable/modules/manifold.html

The MDS is a "linear_embedding, which essentially consist of rotations, translations, and scalings of data into higher-dimensional spaces. Where MDS breaks down is when the embedding is nonlinear—that is, when it goes beyond this simple set of operations." An issue results because MDS will try to preserve the relationship between faraway points but we actually want to preserve relations between nearby points.

The sklearn site also provides this information: "While Isomap, LLE and variants are best suited to unfold a single continuous low dimensional manifold, t-SNE will focus on the local structure of the data and will tend to extract clustered local groups of samples as highlighted on the S-curve example. This ability to group samples based on the local structure might be beneficial to visually disentangle a dataset that comprises several manifolds at once as is the case in the digits dataset."

These are the recommendations given in the paper, so clear!

* For toy problems such as the S-curve we saw before, locally linear embedding (LLE) and its variants (especially_modified LLE_), perform very well. This is implemented in`sklearn.manifold.LocallyLinearEmbedding`.
* For high-dimensional data from real-world sources, LLE often produces poor results, and isometric mapping (IsoMap) seems to generally lead to more meaningful embeddings. This is implemented in`sklearn.manifold.Isomap`
* For data that is highly clustered,_t-distributed stochastic neighbor embedding_(t-SNE) seems to work very well, though can be very slow compared to other methods. This is implemented in`sklearn.manifold.TSNE`.

The main issue with t-SNE is the time that it takes to run.



# Clustering

