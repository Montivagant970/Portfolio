"""The following code contains both the SmartChunker Class and an implementation of the SmartChunker for the creation of input datasets for Wav2Vec 2.0.
The Smart Chunker was developed to intelligently chunk audio files for the finetuning stage of training by creating cut off points based on Voice Activity
Detection (VAD). These VAD breaks are matched to the corresponding time stamps of the annotated audio data as scraped from an ELAN file. The SmartChunker
then saves these chunks and outputs the data necessary to then create the input CSV for Wav2Vec 2.0 finetuning, which is carried out in the implementation
code following the Class.

This tool was developed for my master's thesis on "Automatic Speech Recognition for the South Tyrolean German Dialects"."""

import librosa
import glob
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import bisect
import IPython
import soundfile as sf
import random
from sklearn.model_selection import train_test_split
import csv

os.chdir('/path/to/desired/working/directory')

## Chunk by VAD
class SmartChunker:
  def __init__(self, audio):
    self.audio = audio
    return None

  def audio_data(self, audio):
    sig, sr = librosa.load(audio, sr = 16000)
    audio_name = audio.split("/")[-1]
    print(f'\nProcessing Audio: {audio_name}')
    return sig, sr

  def energy(self, sig, sr, time_frame, time_step):
      num_frames = int(time_frame * sr)
      num_steps = int(time_step * sr)

      rms = []
      for i in range(0, len(sig), num_steps):
          rms.append(np.sqrt(np.mean(sig[i:i+num_frames]**2)))

      return np.array(rms)

  def VAD(self, sig, sr, threshold, time_frame, time_step):
      e = self.energy(sig, sr, time_frame, time_step)
      return np.array(e > threshold, dtype=int)

  def segment_audio(self, threshold, time_frame, time_step):
    sig, sr = self.audio_data(self.audio)
    vad = self.VAD(sig, sr, threshold, time_frame, time_step)

    change_points = vad[1:] - vad[:-1]

    onsets = np.where(change_points == 1)[0]
    offsets = np.where(change_points == -1)[0]

    num_steps = int(time_step * sr)
    # print(onsets, offsets)

    lower_bound = onsets[0] * num_steps  # Set initial lower bound
    last_pause = None  # Initialize last_pause
    segs = []
    time_stamps = []

    for onset, offset in zip(onsets, offsets):
        upper_bound = offset * num_steps

        # Check conditions for chunking
        if upper_bound < lower_bound + 160000:  # < 10 seconds
            last_pause = upper_bound  # Update last_pause as fallback
        elif 160000 <= upper_bound - lower_bound < 240000:  # 10-15 seconds
            segs.append(sig[lower_bound:upper_bound])
            time_stamps.append((lower_bound / sr, upper_bound / sr))  # Record timestamps
            lower_bound = upper_bound  # Update lower_bound
            last_pause = None  # Reset last_pause after successful chunk
        else:  # Fallback to the last pause if > 15 seconds
            if last_pause:  # Ensure last_pause is valid
                segs.append(sig[lower_bound:last_pause])
                time_stamps.append((lower_bound / sr, last_pause / sr))
                lower_bound = last_pause
            else:  # Handle case where no valid last_pause exists
                segs.append(sig[lower_bound:upper_bound])
                time_stamps.append((lower_bound / sr, upper_bound / sr))
                lower_bound = upper_bound

    # Append the remaining audio segment
    final_upper_bound = offsets[-1] * num_steps
    segs.append(sig[lower_bound:final_upper_bound])
    time_stamps.append((lower_bound / sr, final_upper_bound / sr))

    # Remove unusable segment if too short
    if len(segs[-1]) / sr < 2:  # Adjusted logic for segment length
        print(f"          Unusable audio segment number {len(segs)}, since it has a length of {len(segs[-1]) / sr} seconds. Removing from segments...")
        segs.pop(-1)
        time_stamps.pop(-1)

    if 'chunked_audios' not in os.listdir():
      os.mkdir('chunked_audios')
    else:
      pass

    for i, seg in enumerate(segs):
      audio = self.audio.split('/')[-1]
      sf.write(f'chunked_audios/{audio[:-4]}_{i+1}.wav', seg, samplerate = sr)

    return segs, time_stamps

  def extract_transcriptions(self):
    for elan_file in glob.glob('ELAN Files/*.eaf'):
      if elan_file.split('/')[-1][:-4] in self.audio:
        l = elan_file.split('/')[-1]
        print(f'Transcribing: {l}')
        elan = elan_file.split('/')[-1]

        source = open(f'ELAN Files/{elan}').read() #reads in the .eaf file
        soup = BeautifulSoup(source, 'xml') #turns the .eaf file into a soup object for scraping

        content = []
        prelabels = []
        pre_tstarts = []
        pre_tends = []

        part = soup.find('TIER', attrs = {'LINGUISTIC_TYPE_REF':"praat", 'TIER_ID' : 'ORT-MAU'}) # , 'TIER_ID' : f'{audio[:11]}_S{num}' pulls the unit of the ELAN file housing the text and time data. 'f'{audio[:11]}_S{num}'' may need to be updated for the particular structure of the file at hand - this argument is the speaker encoding in the HTML


        for i, unit in enumerate(part.find_all('ALIGNABLE_ANNOTATION')): #find the annotations/time data
          sent = unit.get_text().strip()#.lower() #pulls the text from each annotation

          startid = unit.attrs['TIME_SLOT_REF1'] #pulls the time reference for the start time of the segment
          endid = unit.attrs['TIME_SLOT_REF2'] #pulls the time reference for the end time of the segment

          tstart = soup.find('TIME_SLOT', attrs = {'TIME_SLOT_ID' : startid}).attrs['TIME_VALUE'] #retrieves the start time from the startid
          tend = soup.find('TIME_SLOT', attrs = {'TIME_SLOT_ID' : endid}).attrs['TIME_VALUE'] #retrieves the end time from the startid

          if sent != '':
            prelabels.append(sent)
            pre_tstarts.append(int(tstart)/1000)
            pre_tends.append(int(tend)/1000)

        labels = {i + 1 : label for i, label in enumerate(prelabels)}
        tstarts = {i + 1 : tstart for i, tstart in enumerate(pre_tstarts)}
        tends = {i + 1 : tend for i, tend in enumerate(pre_tends)}

        return labels, tstarts, tends

  def chunk_transcripts(self, threshold, time_frame, time_step):
    segs, time_stamps = self.segment_audio(threshold, time_frame, time_step)
    labels, tstarts, tends = self.extract_transcriptions()
    out = []
    audio = self.audio.split('/')[-1]

    for i, time_stamp in enumerate(time_stamps):
      mins = []
      maxs = []
      transcription = []
      for id, tstart in tstarts.items():
        mins.append((abs(tstart - time_stamp[0]), id))
      for id, tend in tends.items():
        maxs.append((abs(tend - time_stamp[1]), id))
      sorted_mins = sorted(mins, key = lambda x: x[0])
      sorted_maxs = sorted(maxs, key = lambda x: x[0])
      min_id = sorted_mins[0][1]
      max_id = sorted_maxs[0][1]

      for x in range(min_id, max_id + 1):
        transcription.append(labels[x])

      out.append((f'{audio[:-4]}_{i+1}.wav', ' '.join(transcription)))

    return out


## Implementation and Wav2Vec 2.0 Dataset Creation
# Run the SmartChunker
full_transcripts = []
print('---Begin Audio and Transcript Processing---')
for audio in glob.glob('/content/gdrive/MyDrive/JaCo/Finetuning Processing/Audios/*.wav'):
  out = SmartChunker(audio).chunk_transcripts(0.009, 0.02, 0.01)
  full_transcripts.append(out)

# Prepare for CSV Dataset Creation
combined_transcripts = [item for lis in full_transcripts for item in lis]

random.shuffle(combined_transcripts)
P3_train, P3_test = train_test_split(combined_transcripts, test_size=0.17, random_state=47)
print('Ratio of Test to Train is:', len(P3_test) / len(P3_train))

P3_train.insert(0, ('path', 'transcript'))
P3_test.insert(0, ('path', 'transcript'))

os.chdir('/output/directory/for/csvs') #CHANGE OUTPUT DIRECTORY FOR CSVS

# Create Datasets
with open('path2txt_P3_train.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  for path, text in P3_train:
    if path == 'path':
      writer.writerow([path, text])
    else:
      writer.writerow(['/desired/path/' + path, text]) #CHANGE PATH NAME

with open('path2txt_P3_test.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  for path, text in P3_test:
    if path == 'path':
      writer.writerow([path, text])
    else:
      writer.writerow(['/desired/path' + path, text]) #CHANGE PATH NAME
