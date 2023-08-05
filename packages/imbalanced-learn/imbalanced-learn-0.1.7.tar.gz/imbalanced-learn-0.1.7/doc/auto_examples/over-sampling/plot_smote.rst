

.. _sphx_glr_auto_examples_over-sampling_plot_smote.py:


=============
SMOTE regular
=============

An illustration of the random SMOTE regular method.




.. image:: /auto_examples/over-sampling/images/sphx_glr_plot_smote_001.png
    :align: center





.. code-block:: python


    print(__doc__)

    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    # Define some color for the plotting
    almost_black = '#262626'
    palette = sns.color_palette()

    from sklearn.datasets import make_classification
    from sklearn.decomposition import PCA

    from imblearn.over_sampling import SMOTE

    # Generate the dataset
    X, y = make_classification(n_classes=2, class_sep=2, weights=[0.1, 0.9],
                               n_informative=3, n_redundant=1, flip_y=0,
                               n_features=20, n_clusters_per_class=1,
                               n_samples=5000, random_state=10)

    # Instanciate a PCA object for the sake of easy visualisation
    pca = PCA(n_components=2)
    # Fit and transform x to visualise inside a 2D feature space
    X_vis = pca.fit_transform(X)

    # Apply regular SMOTE
    sm = SMOTE(kind='regular')
    X_resampled, y_resampled = sm.fit_sample(X, y)
    X_res_vis = pca.transform(X_resampled)

    # Two subplots, unpack the axes array immediately
    f, (ax1, ax2) = plt.subplots(1, 2)

    ax1.scatter(X_vis[y == 0, 0], X_vis[y == 0, 1], label="Class #0", alpha=0.5,
                edgecolor=almost_black, facecolor=palette[0], linewidth=0.15)
    ax1.scatter(X_vis[y == 1, 0], X_vis[y == 1, 1], label="Class #1", alpha=0.5,
                edgecolor=almost_black, facecolor=palette[2], linewidth=0.15)
    ax1.set_title('Original set')

    ax2.scatter(X_res_vis[y_resampled == 0, 0], X_res_vis[y_resampled == 0, 1],
                label="Class #0", alpha=.5, edgecolor=almost_black,
                facecolor=palette[0], linewidth=0.15)
    ax2.scatter(X_res_vis[y_resampled == 1, 0], X_res_vis[y_resampled == 1, 1],
                label="Class #1", alpha=.5, edgecolor=almost_black,
                facecolor=palette[2], linewidth=0.15)
    ax2.set_title('SMOTE regular')

    plt.show()

**Total running time of the script:**
(0 minutes 0.397 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_smote.py <plot_smote.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_smote.ipynb <plot_smote.ipynb>`
