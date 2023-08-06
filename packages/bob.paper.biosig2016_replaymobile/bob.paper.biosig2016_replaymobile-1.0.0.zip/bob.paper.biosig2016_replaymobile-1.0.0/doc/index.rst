.. vim: set fileencoding=utf-8 :
.. Sushil Bhattacharjee <sushil.bhattacharjee@idiap.ch>
.. Thu 15 Sep 13:43:22 2016

==========================================================================
Package for Replay-Mobile facePAD database paper, presented at BioSIG-2016 
==========================================================================


If you use this package, please cite the following paper::

    @inproceedings{costaBiosig2016,
        author = {A. Costa-Pazo and S. Bhattacharjee and E. Vazquez-Fernandez and S. Marcel},
        title = {The Replay-Mobile Face Presentation Attack Database},
        year = {2016},
        month = sep,
        booktitle = {Proceedings of the 15th International Conference of the Biometrics Special Interest Group (BIOSIG)},
        address = {Darmstadt, Germany},
    }

This python package contains scripts to be used to reproduce the face-PAD results presented in the paper.
This document explains the commnands to be executed in this package, to reproduce the results shown in the paper. Before using this package, please make sure the 'Bob_' package **bob.db.replaymobile** is available in your python environment.
Some programs provided in the current package can also be used with the **bob.db.replay** (Replay-Attack database) package. If you wish to use this package with the Replay-Attack database, please make sure **bob.db.replay** is also available in your python environment.


Reproducing results of the paper
--------------------------------
To reproduce the results in the paper, first, please install the package, following the instructions in the 'Installation' section below.
In the rest of this document, the term **$PKGHOME** will refer to the folder where the package has been installed.

Feature-sets: Experiments presented in the paper are based on two kinds of features extracted from the individual frames of videos comprising the database, namely, image-quality measures (IQM) and Gabor-jet features.
The Gabor-jet features (as well as the code for extracting them) are proprietory to Gradiant (Spain), and are not distributed with this package.
The IQM features computed for the Replay-Mobile database and the older Replay-Attack database are made available via **FTP**, on the following links:

 - Replay-Mobile IQM features: http://www.idiap.ch/resource/biometric/data/biosig2016_replaymobile_iqm_features.tar.gz (contains folder `ReplayMobile_IQM`)
 - Replay-Attack IQM features: http://www.idiap.ch/resource/biometric/data/biosig2016_replayattack_iqm_features.tar.gz (contains folder `ReplayAttack_IQM`)


If you wish to run the experiments described here, please download the appropriate tar-files, extract feature-files and store them under the folder `$PKGHOME/features`.
After successful download, the folder `$PKGHOME/features/ReplayMobile_IQM` should contain the feature-files for the Replay-Mobile database.
If you also download the tar-file for the Replay-Attack database, the feature-files should be extracted and placed the folder `$PKGHOME/features/ReplayAttack_IQM`.


Next, we will look, in reverse order, at the steps required for recreating the results in the paper. The commands discussed below assume that your current working-directory is **$PKGHOME**.


DET Plots:
==========

The main results are the two DET plots shown in the 'Experimental Results' section. These plots are derived from the values shown in the Table comparing the IQM method and the Gabor-jet method on the Replay-Mobile database.
To reproduce these face-PAD results, use the following command:

.. code-block:: sh

    $ ./bin/biosig2016_plots.py -i  ./scores -o ./plots 

This command will look for score-files present in the folder `$PKGHOME/scores`, and will process the files to produce the required plots in the output folder `$PKGHOME/plots`. The command also produces a file `$PKGHOME/plots/perf_table_biosig2016.rst`, which contains the table of performance results comparing the two face-PAD methods for the various kinds of attacks represented in the database. This table is also printed out on the console.
The above command will produce 4 plot-files: two in .eps format, and the same two plots again in .pdf format. (The .pdf files can be viewed more easily, using a PDF-viewer.) In each format, the two files contain DET-plots for the two kinds of features (IQM, Gabor-jets), respectively.

The program `biosig2016_plots.py` looks for score-files with specific names: `$PKGHOME/scores/replaymobile_IqmScores_SVM.hdf5` and `$PKGHOME/scores/gabor-svm-C_SVC-RBF-g0.00025.hdf5`, which contain face-PAD classification scores for the IQM-method and the Gabor-jet-method, respectively.
The score-files are provided with the package, but may be recreated using commands discussed later.
We will see below, how to generate the score-files for the IQM-method (i.e., the file `$PKGHOME/scores/replaymobile_IqmScores_SVM.hdf5`).
As mentioned previously, the Gabor-jet implementation and the resulting features are not made public by Gradiant. Only the face-PAD classification scores are provided, in the file `$PKGHOME/scores/gabor-svm-C_SVC-RBF-g0.00025.hdf5`, to help recreate the DET plots.


Face-PAD scores based on IQM:
=============================

The IQM features for Replay-Mobile and Replay-Attack databases are provided via the **FTP**-links mentioned above. The features are organized in files (one per video) in HDF5 format. Each file contains a `N x 18` matrix, where `N` is the number of frames in the corresponding input video. 
The files are organized in sub-folders according to the 'grandtest' protocol provided by the database.
These files can be used to run face-PAD classification experiments using the provided python script `$PKGHOME/bin/iqm_classifier`. 
Some ways of using this program are described below. 

For a complete list of options this program provides, use the following command (again, assuming that your current working directory is `$PKGHOME`):

.. code-block:: sh

    $ ./bin/iqm_classifier.py -h

The program offers two modes of classification: the **split** mode and the **grandtest** mode.
The **split** mode (default) produces the score-file that is used to compute the APCER and BPCER values reported in the paper. 
Note that the **split** mode is supported only for the Replay-Mobile database.
In **grandtest** mode, the standard 'grandtest' protocol defined for the database is used. 
The program can be used in the **grandtest** mode by specifying the *'-g'* option. The **grandtest** mode is supported for both databases discussed here.

The commands below are shown with the minimum options necessary to reproduce the results in the paper. 
You may specify additional options as you see fit. 
In particular, by default the verbosity of the program is set to 0 (as quiet as possible). 
If you wish to see the program printing out intermediate results, you can use the verbosity-option *'-v 1'* or *'-v 2'*.

Split-mode
..........

Face-PAD results for Replay-Mobile database using image-quality features, in **split** mode, can be reproduced using the following command:

.. code-block:: sh

    $ ./bin/iqm_classifier.py -o ./scores/replaymobile_IqmScores_SVM.hdf5 replaymobile

This command takes a few minutes to execute, because, by default, a SVM-RBF classifier is trained for this task. (The output file, `$PKGHOME/scores/replaymobile_IqmScores_SVM.hdf5`, will be used in the `biosig2016_plots.py` program above, to produce the DET-plots for the IQM-based PAD method).
In this command, the program loads the image-quality features available in the folder `ReplayMobile_IQM`, which is assumed to be a subfolder of `$PKGHOME/features`. 
If your feature-files are not stored in expected folders, you can specify their location explicitly using the *'-b'* and *'⁻f'* options.

Grandtest-mode
..............

Face-PAD results in **grandtest** mode on `Replay-Mobile` using IQM features can be reproduced using the following command:

.. code-block:: sh

    $ ./bin/iqm_classifier.py -g -o ./scores/iqm_svm_gt_replaymobile.h5 replaymobile

This  command prints out on the console the EER on the development-set, and the HTER on the test-set for the **grandtest** protocol of the Replay-Mobile database. 
(Again, use the *'-v 2'* option to monitor progress.) The output-file ./scores/iqm_svm_gt_replaymobile.h5 contains the classification-scores from which the reported EER and HTER are computed.

Similarly, the **grandtest** face-PAD results for the `Replay-Attack` database can be generated using the following command:

.. code-block:: sh

    $ ./bin/iqm_classifier.py -g -f ReplayAttack_IQM -o ./scores/iqm_svm_gt_replay.h5 replay

This command will print out the EER on the development-set and HTER on the test-set of the Replay-Attack grandtest protocol, using the IQM features.

The score-files resulting from the **grandtest** experiments are not used for the DET-plots. They are simply stored for manual inspection if necessary.
    
Using LDA classifier
....................

By default the `iqm_classifier.py` uses the SVM-RBF classifier (with gamma-parameter set to 1.5 by default in this program). 
The *'-c'* option can be used to specify that a LDA classifier should be used instead.

Face-PAD using LDA on the grandtest protocol of Replay-Mobile:

.. code-block:: sh

    $ ./bin/iqm_classifier.py -c LDA -g -f ReplayMobile_IQM -o ./scores/iqm_lda_gt_replaymmobile.h5 replaymobile

and on the Replay-Attack database:

.. code-block:: sh

    $ ./bin/iqm_classifier.py -c LDA -g -f ReplayAttack_IQM -o ./scores/iqm_lda_gt_replay.h5 replay

These commands print out on the console the EER (on the development set) and HTER (for the test-set) for the respective classification results.
Note that results using LDA are only discussed in the online-version of the paper, not the version printed in the Proceedings (due to space constraints).
As with previous commands, the scores on which the printed results (EER, HTER) are based, are stored in the specified output file in HDF5 format.


Computing IQM features for videos in the database:
==================================================

The program `$PKGHOME/bin/compute_iqm_features.py` can be used to compute the 18 image-quality features mentioned in the paper. The program accepts an input video-file in .mov format, and produces a feature-file in HDF5 format. Video files in the Replay-Mobile and Replay-Attack databases can be processed using this program, in the following way:

.. code-block:: sh

    $ ./bin/compute_iqm_features.py -i <input_video_file.mov>  -o <output_feature_file.h5>

In order to generate feature-files for the database using this script, you will first need to download the `Replay-Mobile <https://www.idiap.ch/dataset/replay-mobile>`_ database. The `compute_iqm_features.py` script processes one file at a time, but may easily be modified to process a whole set of files in a single command.
This script can be used to produce the image-quality feature-files for the database. Because the scipt takes a long time to process a single video (the time depends on the resolution and the number of frames), the pre-computed feature-files are provided on the FTP site for your convenience.



Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _Replay-Mobile: https://www.idiap.ch/dataset/replay-mobile

