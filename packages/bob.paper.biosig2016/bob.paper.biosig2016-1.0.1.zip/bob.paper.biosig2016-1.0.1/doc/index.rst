.. vim: set fileencoding=utf-8 :
.. Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
.. Mon 19 Sep 11:35:15 CEST 2016

=====================================================
Reproducing results of paper published in BIOSIG 2016
=====================================================
        
This package is part of the Bob_ toolkit and it allows to reproduce the following paper::

    @inproceedings{MuckenhirnBIOSIG2016,
        author = {Muckenhirn, Hannah and Magimai.-Doss, Mathew and Marcel, S{\'{e}}bastien},
        month = sep,
        title = {Presentation Attack Detection Using Long-Term Spectral Statistics for Trustworthy Speaker Verification},
        booktitle = {Proceedings of International Conference of the Biometrics Special Interest Group (BIOSIG)},
        year = {2016},
    }

        


I- Installation
--------------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. ASVspoof_: http://datashare.is.ed.ac.uk/handle/10283/853


To run all the experiments, two databases need to be downloaded: AVspoof_ and ASVspoof_. The paths to folders with the corresponding data need to be updated in the following files inside the ``src/bob.paper.biosig2016/bob/paper/biosig2016/config/database`` directory:

* asvspoof_cm.py
* avspoof_detect_physical.py

Once the databases are dowloaded, the corresponding Bob's interfaces need to be updated too. Please run the following commands::

    For AVspoof database: $ ./bin/bob_dbmanage.py avspoof download 
    For ASVspoof database: $ ./bin/bob_dbmanage.py asvspoof download


II- Running experiments
-----------------------
Training a Presentation Attack Detection (PAD) classifier is done with the script ``./bin/spoof.py``, from Bob's package ``bob.pad.base``, or the script ``./bin/spoof_mlp.py``. They both take several parameters, including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A PAD algorithm

All these steps of the PAD system are given as configuration files.

1. AVspoof database
-------------------
This part explains how to reproduce the results obtained on the AVspoof database, showed in Table 2 of the paper.

To train the PAD system with a Linear Discriminant Analysis classifier, you need to run the following command:

  $ ./bin/spoof.py -d avspoof-detect-physical -p energy-2gauss-remove-head-tail -e <Feature_Extractor> -a lda -s <Folder_Name> -groups dev eval -vv

To train the PAD system with a Multi-Layer Perceptron with one hidden layer composed of 200 hidden units, you need to run the following command:

  $ ./bin/spoof_mlp.py -d avspoof-detect-physical -p energy-2gauss-remove-head-tail -e <Feature_Extractor> -a mlp-sigmoid-200-neurons-stoch -s <Folder_Name> -groups dev eval -vv

<Folder_Name> is the folder in which the results of all the subtasks and the final score files are stored. <Feature_Extractor> corresponds to the features extracted, which can be one of the followings:
* mean-spectrum-32ms
* std-spectrum-32ms
* mean-std-spectrum-32ms

To evaluate those systems, you need to run the following command:

  $ ./bin/evaluate_pad.py -d <Folder_Name_Scores>

This script will output the Eauql Error Rate (EER) computed on the development set and the Half Total Error Rate computed on the evaluation set. <Folder_Name_Scores> should contain exactly four files names ``scores-dev-real``, ``scores-dev-attack``, ``scores-eval-real`` and ``scores-eval-attack`` , which correspond to the score files generated with the  ``./bin/spoof.py`` or ``./bin/spoof_mlp.py`` script.



2. ASVspoof database
--------------------
This part explains how to reproduce the results obtained on the ASVspoof database, showed in Table 3 of the paper.

To train the PAD system with a Linear Discriminant Analysis classifier, you need to run the following command:

  $ ./bin/spoof.py -d asvspoof-cm -p energy-2gauss-remove-head-tail -e mean-std-spectrum-256ms -a lda -s <Folder_Name> -groups dev eval -vv

The training of the PAD system on the ASVspoof database with a Multi-Layer Perceptron was done with the toolkit Quicknet, developed by the ICSI Speech Group. We stored the score files in the folder ```quicknet_mlp_scores``.

To evaluate those systems, you need to run the following command:

  $ ./bin/compute_EER_perattack_eval.py -d <Name_Scores_Eval_Real> -t <Name_Scores_Eval_Attack> -o <Output_File>

This script output the EER computed on each type of attack of the evaluation set, the average of these EERs over the knwon attacks, the unknown attacks and all the attacks. This script will print its output in the terminal and in the file specified by <Output_File>. <Name_Scores_Eval_Real> and <Name_Scores_Eval_Attack> correspond respectively to the file containing the scores of the real accesses and of the attacks of the evaluation set. 
