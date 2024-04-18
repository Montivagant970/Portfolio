"""prep4finetune preprepares audio data to be used in finetuning the Whisper LLM by parsing the data into the specified input format.

The function takes audio data, parses it into 30 second chunks, preprocesses it in Whisper to create a preliminary transcription, and 
saves the outputs in CSV format with the pathname to the audio in column 1 and its respective transcription in column 2.

The function will create two folders: (1) 'Output Chunked Audios' which will store the 30 second snippets of audio produced by the function 
and (2) 'Output Prepared CSVs' which will house the resulting spreadsheet(s).

It (optionally) outputs the chunks (as signal arrays) which can be saved through assigning the output of the function to a variable, 
if that data is desired. Otherwise, it processes and outputs to the working directory.

The function can be used within Google Drive with Google Colab or locally by specifying the desired working directory. The working directory
should house all the audio files to be processed.

This project was a tool developed for the EURAC internship project finetuning the Whisper LLM to South Tyrolean German dialect."""

## Set-up ##
import librosa
import glob
import csv
from tqdm import tqdm
import soundfile as sf
import os

from google.colab import drive
drive.mount('/content/gdrive')

%cd '/path/to/desired/working/directory'


## Loading the Whisper Model and Processor ##
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
forced_decoder_ids = processor.get_decoder_prompt_ids(language="german", task="transcribe")


## prep4finetune ##
def prep4finetune(audio):
  if 'Output Chunked Audios' not in os.listdir(): #creates the two output folders if they do not yet exist
    os.mkdir('Output Chunked Audios')
    os.mkdir('Output Prepared CSVs')
  else:
    pass

  sig, sr = librosa.load(audio, sr = 16000) #loads the audio into a signal array and sampling rate using librosa
  chunks = [sig[chunk : chunk + 480000] for chunk in range(0, len(sig), 480000)] #parses the audio into chunks of 30 seconds

  out = {} #instantiates an output dictionary for the CSV
  for i, chunk in tqdm(enumerate(chunks), unit = 'Chunk'): #iteratively processes each chunk through Whisper Small
    print(f" Chunk #{i+1} is being processed.")

    input_features = processor(chunk, sampling_rate = sr, return_tensors = "pt").input_features #reads in audio (input must be an array)

    predicted_ids = model.generate(input_features, forced_decoder_ids = forced_decoder_ids) #generates token ids

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens = True) #decodes the predicted ids to create transcription

    if len(transcription[0]) < 50: #DEBUG LINE: if the model crashes and produces a unreasonably short transcription, parse the 30 second chunk into two 15 second chunks and reprocess (seems to resolve the issue)
      for i2, snip in enumerate(range(0, len(chunk), 240000)):
        snippet = chunk[snip : snip + 240000] #parses the 30 second chunk into two 15 second chunks

        input_features = processor(snippet, sampling_rate = sr, return_tensors = "pt").input_features #reads in audio (input must be an array)

        predicted_ids = model.generate(input_features, forced_decoder_ids = forced_decoder_ids) #generates token ids

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens = True) #decodes the predicted ids to create transcription

        out[os.getcwd() + f'/{audio[:-4]}_chunk{i+1}.{i2+1}.wav'] = transcription #updates the dictionary with the pathname for the audio chunk (key) and the transcription (value)

        sf.write(f'Output Chunked Audios/{audio[:-4]}_chunk{i+1}.{i2+1}.wav', snippet, samplerate = sr, subtype = 'PCM_24') #writes the chunk to a wav file and outputs to the 'Output Chunked Audios' folder

    else:
      out[os.getcwd() + f'/{audio[:-4]}_chunk{i+1}.wav'] = transcription #updates the dictionary with the pathname for the audio chunk (key) and the transcription (value)

      sf.write(f'Output Chunked Audios/{audio[:-4]}_chunk{i+1}.wav', chunk, samplerate = sr, subtype = 'PCM_24') #writes the chunk to a wav file and outputs to the 'Output Chunked Audios' folder

  with open(f'Output Prepared CSVs/{audio[:-4]}.csv', 'w') as csvfile: #prepares and saves the csv file to the 'Output Prepared CSVs' folder
    writer = csv.writer(csvfile)
    for path, text in out.items():
      writer.writerow([path, text[0]])

  return chunks #returns the signal arrays of all chunks in the audio (if desired)


## Working with prep4finetune ##
for track in tqdm(glob.glob('*.wav'), unit = 'Track'): #iterates through all wav files in the working directory
  print(f' Track: {track}.')
  prep4finetune(track)

print(' Operation complete.')
