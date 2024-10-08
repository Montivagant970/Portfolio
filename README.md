# Portfolio - Kelton Jay Hevelone
The present repository is a collection of the various projects and tools that I have developed for my coursework at the Free University of Bolzano/Bozen and my internship at Eurac Research.

### Coursework:
* ***Artificial Intelligence:***
  * **minesweepersolver.ipynb** : notebook with a solver for Minesweeper using z3 based on SMT, developed as an exercise for Artificial Intelligence.
  * **tspsolver.ipynb** : notebook with a solver for the Traveling Sales Person (TSP) problem using MiniZinc for constraint satisfaction, developed as an exercise for Artificial Intelligence.
  * **minigridsolver.ipynb** : notebook with a solver for a Minigrid environment using PDDL planning, developed as an exercise for Artificial Intelligence.
    * **minigrid-domain.pddl** : file describing the PDDL domain including predicates and actions.
    * **minigrid-problem.pddl** : file describing the PDDL problem including objects, init states, and goals.
* ***Computational Linguistics:***
  *  **Final_CL.ipynb** : notebook outlining the final project I developed for Computational Linguistics on topic modelling, specifically Principle Component Analyses (PCA) and Latent Dirichlet Analyses (LDA), for *The Complete Anglo-Saxon Poetry Corpus*. The notebook contains all code, documentation, analyses, descriptions, and graphics of the project.
* ***Machine Learning:***
  * **Final_ML.ipynb** : notebook outlining the final project I developed for Machine Learning on the automatic classification of fake news content. The notebook contains all code, documentation, analyses, descriptions, and graphics of the project.
    * **FakeNewsClassifier.py** : Multinomial Naiive Bayes classifier (class) which sorts news text as either 'real' or 'fake' with around 75% accuracy, developed for the final project of Machine Learning.
    *  **NewsClassifier.py** : a tweaked version of the *FakeNewsClassifier* which sorts news by topic, developed for the final project of Machine Learning.
    *  **scikitbayes.py** : function which tests the fake news dataset on the Gaussian and Multinomial Naiive Bayes classifiers from Scikit-learn, developed for the final project of Machine Learning.
    *  **scikitkNN.py** : function which tests the fake news dataset on the k-Nearest Neighbor classifier from Scikit-learn, developed for the final project of Machine Learning.
    *  **main.py** : exam submission file which runs all the above scripts.
* ***Speech Technologies:***
  *  **Final_ST.ipynb** : notebook outlining the final project I developed for Speech Technologies for two separate experiments, namely a Whisper STT model evaluation and a machine learning implementation for accent recognition, on *The Speech Accent Archive* from George Mason University. The notebook contains all code, documentation, analyses, descriptions, and graphics of the project.

### Internship:
* **ELANtranscriber.py** : tool to scrape speaker annotation data from ELAN (.eaf) files.
* **prep4finetune.py** : tool to prepare audio data for finetuning the Whisper LLM by chunking and creating preliminary transcriptions in CSV files.
* **YouTubeScraper.py** : tool (class) to scrape audio and video data from YouTube, extract embedded subtitle text in the video, and prepare audio/text from videos for finetuning the Whisper LLM.

### Tools:
* **csvcleaner.py** : tool to convert semicolon delimited csv UTF-8 files from Excel into standard comma separated csv files.
* **audio_metrics_calculator.py** : tool to calculate the duration and size of a folder of audio files.

### Master's Thesis from the Free University of Bolzano/Bozen:
~ work in progress: will update later ~

### Personal Projects:
~ work in progress: will update later ~
