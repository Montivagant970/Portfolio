# Portfolio - Kelton Jay Hevelone
The present repository is a collection of the various projects and tools that I have developed for my coursework at the Free University of Bolzano/Bozen and my internship at Eurac Research.

### Internship:
* **ELANtranscriber.py** : tool to scrape speaker annotation data from ELAN (.eaf) files.
* **prep4finetune.py** : tool to prepare audio data for finetuning the Whisper LLM by chunking and creating preliminary transcriptions in CSV files.
* **YouTubeScraper.py** : tool (class) to scrape audio and video data from YouTube, extract embedded subtitle text in the video, and prepare audio/text from videos for finetuning the Whisper LLM.

### Coursework:
* ***Artificial Intelligence:***
  * **minesweepersolver.ipynb** : notebook with a solver for Minesweeper using z3 based on SMT, developed as an exercise for Artificial Intelligence.
  * **tspsolver.ipynb** : notebook with a solver for the Traveling Sales Person (TSP) problem using MiniZinc for constraint satisfaction, developed as an exercise for Artificial Intelligence.
  * **minigridsolver.ipynb** : notebook with a solver for a Minigrid environment using PDDL planning, developed as an exercise for Artificial Intelligence.
    * **minigrid-domain.pddl** : file describing the PDDL domain including predicates and actions.
    * **minigrid-problem.pddl** : file describing the PDDL problem including objects, init states, and goals.
* ***Machine Learning:***
  * **FakeNewsClassifier.py** : class to classify news text as either 'real' or 'fake,' developed as the final project for Machine Learning. 

### Personal Projects:

### Tools:
* **csvcleaner.py** : tool to convert semicolon delimited csv UTF-8 files from Excel into standard comma separated csv files.
* **audio_metrics_calculator.py** : tool to calculate the duration and size of a folder of audio files.
