# Portfolio - Kelton Jay Hevelone
The present repository is a collection of the various projects and tools that I have developed for my coursework and thesis at the Free University of Bolzano/Bozen and my internship at Eurac Research.

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

### Thesis: Master's Thesis from the Free University of Bolzano/Bozen
My master's thesis, entitled "Automatic Speech Recognition for the South Tyrolean German Dialects," sought to train a functional speech recognition model for the German dialects, capable of outputting in the dialects themselves, while altering its output for the individual writing preferences of the user. The Project consisted likewise with linguistic work with the establishment of dialect writing norms for the purpose of normalizing the input script to the model, called Computational Tyrolean - CompTyr, and fieldwork with the elicitation of over seven hours of labeled dialect data from native speakers to establish the JaCo corpus. *Code was adapted from Le Duy Khanh for the purposes of the project, built originally from [Meta's ASR tutorial](https://huggingface.co/blog/fine-tune-wav2vec2-english). Original repos for [pretraining](https://github.com/khanld/Wav2vec2-Pretraining?tab=readme-ov-file) and [finetuning](https://ithub.com/khanld/ASR-Wav2vec-Finetune) can be found at their respective links.*
* ***Pretraining:***
  * **pretrain_wav2vec.py** : script adapted for pretraining the Wav2Vec 2.0 model from Meta for the task of Automatic Speech Recognition (ASR). 
* ***Finetuning:***
  *  *base:*
     *  **base_dataset.py** : script to load the text dataset, clean its contents, and derives the character dictionary from which the model transcribes.
     *  **base_trainer.py** : script to initiate and loop through training epochs with additional functions to resume from checkpoints, load a pretrained model, push to GitHub, and calculate metrics on parameters.
  *  *dataloader:*
     *  **dataset.py** : script to load in the audio dataset using the DataCollator from Meta.
  *  *logger:* 
     *  **pbar.py** : script to create and output a progress bar in training.
     *  **tensorboard.py** : script to write training output to a Tensorboard. 
  *  *trainer:*
     *  **trainer.py** : script to train the model, including the forward and backwards passes, optimizing steps, clipping gradients, updating parameters, logging, and evaluating.
  *  *utils:*
     *  **feature.py** : script with functions to load audio data and to chunk or pad chunked audio.
     *  **metric.py** : script with a function to calculate the Word Error Rate (WER) metric.
     *  **utils.py** : script with functions to set seeds and initialize modules. 
  *  **train.py** : main script which runs the finetuning pipeline.
  *  **model_implementation.py** : script to load and implement outputted finetuned models from the training pipeline. 

### Internship:
* **ELANtranscriber.py** : tool to scrape speaker annotation data from ELAN (.eaf) files.
* **prep4finetune.py** : tool to prepare audio data for finetuning the Whisper LLM by chunking and creating preliminary transcriptions in CSV files.
* **YouTubeScraper.py** : tool (class) to scrape audio and video data from YouTube, extract embedded subtitle text in the video, and prepare audio/text from videos for finetuning the Whisper LLM.

### Tools:
* **2wav_converter.py** : tool to convert .mp3 or .m4a audio files to .wav.
* **SmartChunker.py** : tool (class) developed to smart chunk audio files based on Voice Activity Detection (VAD) with an automatic text alignment feature utilizing annotated ELAN files.
* **audio_compressor.py** : tool to compress or decompress all .wav files in a given directory.
* **audio_metrics_calculator.py** : tool to calculate the duration and size of a folder of audio files.
* **corrupted_audio_check.py** : tool to check for corruption in a directory of audio files.
* **csvcleaner.py** : tool to convert semicolon delimited csv UTF-8 files from Excel into standard comma separated csv files.
* **podcast_scraper.py** : tool to automatically scrape audios from a website with imbedded data.  
