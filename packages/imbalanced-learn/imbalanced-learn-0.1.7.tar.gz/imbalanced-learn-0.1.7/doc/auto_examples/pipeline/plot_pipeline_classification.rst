

.. _sphx_glr_auto_examples_pipeline_plot_pipeline_classification.py:



=========================
Pipeline Object
=========================

An example of the Pipeline object working with transformers and resamplers.





.. rst-class:: sphx-glr-script-out

 Out::

      precision    recall  f1-score   support

              0       0.61      0.89      0.73       409
              1       0.93      0.72      0.81       841

    avg / total       0.83      0.78      0.79      1250




|


.. code-block:: python


    print(__doc__)

    from sklearn.cross_validation import train_test_split as tts
    from sklearn.datasets import make_classification
    from sklearn.decomposition import PCA
    from sklearn.neighbors import KNeighborsClassifier as KNN
    from sklearn.metrics import classification_report


    from imblearn.pipeline import make_pipeline
    from imblearn.under_sampling import EditedNearestNeighbours
    from imblearn.under_sampling import RepeatedEditedNearestNeighbours

    # Generate the dataset
    X, y = make_classification(n_classes=2, class_sep=1.25, weights=[0.3, 0.7],
                               n_informative=3, n_redundant=1, flip_y=0,
                               n_features=5, n_clusters_per_class=1,
                               n_samples=5000, random_state=10)

    # Instanciate a PCA object for the sake of easy visualisation
    pca = PCA(n_components=2)

    # Create the samplers
    enn = EditedNearestNeighbours()
    renn = RepeatedEditedNearestNeighbours()

    # Create teh classifier
    knn = KNN(1)


    # Make the splits
    X_train, X_test, y_train, y_test = tts(X, y, random_state=42)

    # Add one transformers and two samplers in the pipeline object
    pipeline = make_pipeline(pca, enn, renn, knn)

    pipeline.fit(X_train, y_train)
    y_hat = pipeline.predict(X_test)

    print(classification_report(y_test, y_hat))

**Total running time of the script:**
(0 minutes 0.964 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_pipeline_classification.py <plot_pipeline_classification.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_pipeline_classification.ipynb <plot_pipeline_classification.ipynb>`
