.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Thu 23 Jun 13:43:22 2016

=======================================================
Package for BTAS 2016 Speaker Anti-spoofing Competition
=======================================================

If you use this package, please cite the following paper::

    @inproceedings{KorshunovBtas2016c,
        author = {P. Korshunov AND S. Marcel AND H. Muckenhirn AND A. R. Goncalves AND A. G. Souza Mello AND 
		R. P. Velloso Violato AND F. O. Simoes AND M. U. Neto AND 
		M. de Assis Angeloni AND J. A. Stuchi AND H. Dinkel AND N. Chen AND
		Y. Qian AND D. Paul AND G. Saha AND Md Sahidullah},
        title = {Overview of BTAS 2016 Speaker Anti-spoofing Competition},
        year = {2016},
        month = sep,
        booktitle = {IEEE International Conference on Biometrics: Theory, Applications and Systems (BTAS)},
        address = {Niagara Falls, NY, USA},
    }

This package contains Baseline system and information on how to obtain and process data used in BTAS 2016 Speaker Anti-spoofing Competition. It also provides scores submitted by the participants of the competition and scripts for processing and analysis of these scores that help in reproducing the results (error rates and DET curves) presented in the above paper.

Reproducing results of the competition
--------------------------------------

Scores submitted in the competition can be found inside folder `submissions`. Folder 
`submissions/to_recover_test_files` contains all the information that allows recovery of the anonymized test data.

The provided score files need to be pre-processed (split into `real` and `attack` lists correctly), which can be done by running the following:

.. code-block:: sh

    $ ./preprocess_scores.sh ./submissions dev
    $ ./preprocess_scores.sh ./submissions test

For test scores, the scores of anchor files (from Dev set) are compared with the corresponding scores for the dev set to check if they are equal. The anchor scores are ignored in error rate computation.

To compute all Error Rates presented in the Table 2 and Table 3 of the paper, run the following:

.. code-block:: sh

    $ ./evaluate_scores.sh ./submissions dev
    $ ./evaluate_scores.sh ./submissions test

For each submission, the script will generate text files with prefix `stats_` with computed error rates for Dev or Test sets. Also, a more detailed error rates and plots are generated for each different type of attacks for each submission inside folders prefixes with `plots_`.

To plot DET curves as presented in Figure 1 of the paper, run the following:

.. code-block:: sh

    $ ./plot_combined_det.sh ./submissions dev <output folder name>
    $ ./plot_combined_det.sh ./submissions test <output folder name>

The script will generate PDF files inside provided `<output folder name>` for corresponding Dev and Test scores.

Real and spoofed speech data used in the competition
----------------------------------------------------

AVspoof_ database was used the competition. It contains real (genuine) speech samples from 44 participants (31 males and 13 females) recorded over the period of two months in four sessions, each scheduled several days apart in different setups and environmental conditions such as background noises. Ten types of attacks were also generated using speech synthesis, voice conversion, and by replaying sample with two different mobile phones and a laptop.

All samples of the database are split into three non-overlapping sets: training, development, and evaluation. Each set consists of two parts: (i) real or genuine data and (ii) spoofed data or attacks. The samples were given in WAV format with 16 KHz sampling rate.

Training, development, and test sets used in the competition can be downloaded from Idiap repository_::

	* btas2016_data.tar.gz - a training and development sets of WAV audio files (9.2 GB). These files are used to train 
	and tune Presentation Attack Detection (PAD) system. 
	* btas2016_data_test_v2.tar.gz - a test set of WAV audio files (5.2 GB). These files are used to compute evaluation 
	scores using the pre-trained and tuned PAD system.
	* btas2016_data_test.tar.gz - this is a first version of the test set (6.1 GB). The differences compared to the 
	version 2 that was used for the evaluation is that this Test set is missing preprocessing step that includes removal 
	of silent head and tail from all audio files (to avoid biases). Train and Dev set were preprocessed in this way. 
	This version of Test set can be used to study the effects of additional channel information (silence) on the PAD 
	system, when this information is not present in Train and Dev sets but is present in Test set.


It is better to move all the data (once, it is uncompressed into 'train' and 'dev' folders) into one joint folder, say, 'data'. Then, the provided file lists can be used directly with this data folder. The data files in the repository_ (`btas2016_doc.tar.gz`, `btas2016_doc_test.tar.gz`, and `btas2016_doc_test_with_ids.tar.gz`) contain file lists::

	* train-real-list.txt
	* train-attack-list.txt
	* dev-real-list.txt
	* dev-attack-list.txt
	* test-list.txt - file list for Test set with anonymized Ids and attack names, which also includes anchor files from 
	Dev set that were used to ensure that participants submit scores for test set that are consistent with the scores 
	obtained on the dev set.
	* test-real-list.txt - file list of genuine speech for Test set with de-anonymized info, released after the 
	competition was finished. 
	* test-attack-list.txt - file list of spoofed speech for Test set with de-anonymized info, released after the 
	competition was finished. 

These files lists have the following format:
    ID relative_file_name sample_type

where 'ID' - the id of the corresponding subject, 'relative_file_name' - a relative path to the audio file, and 'sample_type' indicates whether the sample is a real (tagged as 'genuine') data or an attack (the name of attack is written).


Running Baseline system
-----------------------

A simple Baseline system was provided in the competition, which is a Python script that utilizes some functions from Bob_ toolkit to process provided data, train a classifier, and compute scores. To train the Baseline system on training set, run the following (make sure AVspoof database interface `bob.db.avspoof` is installed in your environment):

.. code-block:: sh

    $ python baseline.py --input-dir <folder where the training data is> --skip-evaluation avspoof --protocol physical_access

To evaluate the system using Development data, run the following (it is assumed the classifier has been trained):

.. code-block:: sh

    $ python baseline.py --input-dir <folder where the Dev data is> --skip-training avspoof --protocol physical_access

To test the system on the Test set, run the following:

.. code-block:: sh

    $ python baseline_test.py --input-dir <folder where the test data is> --skip-training avspoof_btas2016 --protocol btas2016

Note that for testing, `avspoof_btas2016` database interface is used (please install `bob.db.avspoof_2016` package with pip).

Baseline system is a Python script that gives EER of 5.91% on the provided development set (see installation and usage instructions below). The script reads audio files provided for BTAS 2016 anti-spoofing competition, extract features, train logistic regression classifier on the training set and, by using the trained classifier, computes score for the development set. From the resulted scores, EER value is computed and Detection Error Tradeoff (DET) curve is plotted. So, this script can be a starting point in the development of an anti-spoofing system using Bob_. It allows to see how the provided data can be read and processed. 


Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. _repository: https://www.idiap.ch/dataset/avspoof/download-proc

