"""YouTubeScraper is a class containing two tools for working with YouTube videos: contentextractor and researchextractor.

contentextractor is a simple method which downloads the full video and audio to the specified working directory. To specify not wanting either the video or
the audio, the respective arguments in the method call must be set to False (as both are by default True, i.e. on).

researchextractor was developed as a tool for preparing videos with embedded subtitles and their respective audios for the finetuning of the Whisper LLM. 

The method allows the user to:
(1) save audio and video files
(2) create, save, and process frames from the video using OCR to extract embedded subtitle text
(3) chunk the audio and OCR output into the desired Whisper input (csv file with pathname in column 1 and text content in column 2; 30 second 
audio chunks corresponding to each row in the csv)
(4) output an informational csv for debugging, which includes the frame name, the mean OCR score at that frame, and 
the OCR transcription. 

The return output of the researchextractor is a defaultdict with the frame names as keys and the OCR transcription as its respective value.

The function can be used within Google Drive with Google Colab or locally by specifying the desired working directory. The working directory should house 
the text document holding the urls to all the videos to be processed, if working with a list of urls. Or if working with a single video, the url can be copied
directly into the script. 

This project was a tool developed for the EURAC internship project finetuning the Whisper LLM to South Tyrolean German dialect."""

## Set-Up ##
!pip install git+https://github.com/pytube/pytube #python -m
!pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
!pip install paddleocr
!pip install fastDamerauLevenshtein

import cv2
from pytube import YouTube
import os
import re
from PIL import Image
import numpy as np
from numpy import mean
from moviepy.editor import VideoFileClip
from paddleocr import PaddleOCR, draw_ocr
import csv
from fastDamerauLevenshtein import damerauLevenshtein
from collections import defaultdict
import librosa
import soundfile as sf
import time

from google.colab import drive
drive.mount('/content/gdrive')

%cd '/path/to/desired/working/directory'


## YouTubeScraper ##
class YouTubeScraper:
  def __init__(self):
    return None

  @staticmethod
  def rename(filename): #standardizes the filenames
    s = re.sub(r'\s', '', filename)
    return re.sub(r'[-–]', '_', s)

  def contentextractor(self, url, audio = True, video = True):
    """method to quickly retrieve the full audio and video files from a YouTube video.

       audio: optional argument which save the FULL audio from the video as an .wav file to the working directory (default on).
       video: optional argument with saves the video as an .mp4 file to the working directory (default on)."""

    yt = YouTube(link) #creates a YouTube object for the given video
    stream = yt.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first() #creates a Stream object from the YouTube object
    fname = self.rename(stream.default_filename) #renames the stream and sets to new variable
    stream.download(filename = fname) #temporarily downloads the video to the working directory

    if audio == True:
      audio_clip = VideoFileClip(fname).audio #extracts the audio from the video
      audio_clip.write_audiofile(fname[:-4] + '.wav') #download the audio in wav format
      audio_clip.close()
    if video == False:
      os.remove(fname) #deletes video if not desired

    return

  def researchextractor(self, url, audio = False, chunks = False, csv_info = False, frames = False, video = False):
    """method to aid in research, specifically in finetuning the Whisper LLM, using YouTube videos. The method can save audio and video files; create, save, and process frames from the video
       using OCR to extract embedded subtitle text; chunk the audio and OCR output into the desired Whisper input (csv file with pathname in column 1 and text content in column 2); create 30
       second audio chunks corresponding to each row in the csv; and an informational csv for debugging, which includes the frame name, the mean OCR score at that frame, and the OCR transcription.
       The return output of the researchextractor is a defaultdict with the frame names as keys and the OCR transcription as its respective value. Optional arguments must be specified.

       url: url of the video on YouTube.
       audio: optional argument which saves the FULL audio from the video as an .wav file to the working directory (default off).
       chunks: optional argument which saves the audio in chunks of 30 seconds (default off).
       csv_info: optional argument which creates and saves a csv to the working directory with the frame names, the transcription, and the respective OCR confidence score (default off).
       frames: optional argument which saves the individual frames from the video as .jpeg files to the working directory (default off).
       video: optional argument with saves the video as an .mp4 file to the working directory (default off)."""

    ### Set-Up / Load-In ###
    ocr_model = PaddleOCR(use_angle_cls=True, lang='de') #instantiates the OCR model
    count = 0 #sets the iterative frame count to 0
    success = True #starts the success loop for the text extraction to True
    storage = {} #creates a storage dictionary to be transformed into the output
    output = defaultdict(list) #instantiates the output defaultdictionary

    yt = YouTube(url) #creates a YouTube object for the given video
    stream = yt.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first() #creates a Stream object from the YouTube object
    fname = self.rename(stream.default_filename) #renames the stream and sets to new variable
    stream.download(filename = fname) #temporarily downloads the video to the working directory

    vidcap = cv2.VideoCapture(fname) #creates a VideoCapture object


    ### Creating the Informational CSV ###
    if csv_info == True:
      if 'Output_Prepared_CSVs' not in os.listdir():
        os.mkdir('Output_Prepared_CSVs')
      dataout = open(f'Output_Prepared_CSVs/{fname[:-4]}_info.csv' , 'w')
      dataout.write('fname' + '\t' +'mean_ocr_score' + '\t' +  'text' + '\n')


    ### Text Extraction with OCR from Video Frames ###
    while success:
      try:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*2000)) #captures a frame every two seconds
        success, image = vidcap.read() #scrapes the frame and whether extraction was successful

        try:
          im = Image.fromarray(image) #transforms the array to an image
          cropped = im.crop((50, 500, 1250, 700)) #crops the image to the area likely to hold subtitles

          result = ocr_model.ocr(np.array(cropped.convert("RGB"))) #runs OCR on the cropped image

          texts = [line[1][0] for line in result[0]]  #extracts detected texts
          scores = [line[1][1] for line in result[0]] #extracts confidence scores

          storage[f"{fname[:-4]}_frame_{count}"] = ' '.join(texts) #stores the frame name and text content

          if csv_info == True:
            dataout.write(f"{fname[:-4]}_frame_{count}" + '\t' + str(mean(scores)) + '\t' +  ' '.join(texts) + '\n') #writes the informational CSV with frame names, OCR confidence scores, and texts, if selected

          if frames == True:
            if 'Output_Frames' not in os.listdir():
              os.mkdir('Output_Frames')
            cv2.imwrite(f"Output_Frames/{fname[:-4]}_frame_{count}.jpg", image) #outputs the frames with content, if selected

        except:
          storage[f"{fname[:-4]}_frame_{count}"] = 'no_ocr' #adds frames without text to the storage

          if csv_info == True:
            dataout.write(f"{fname[:-4]}_frame_{count}" + '\t' + '0' + '\t' +  'no_ocr' + '\n') #adds the same information to the informational csv

        count += 1 #advance the frame count by 1

      except Exception as e:
        print(e)


    ### Creating the Function Output ###
    transcr = [i for i in storage.items() if i[1] != 'no_ocr'] #selects all the frames with text content
    current_frame = transcr[0][0]
    for a,b in zip(transcr, transcr[1:]):
      if damerauLevenshtein(a[1], b[1]) > 0.8: #if the Levenshtein distance between two texts is similar enough
        output[current_frame].append(a[1]) #append to the current frame one or more OCR transcriptions (in the case that the subtitles last over multiple frames)
      else:
        output[current_frame].append(a[1])
        current_frame = b[0] #otherwise advance to the next frame with new text


    ### Saving the Informational CSV ###
    if csv_info == True:
      dataout.close()


    ### Saving the Full Audiofile or Chunking it for Whisper ###
    if audio == True or chunks == True:
      try:
        audio_clip = VideoFileClip(fname).audio #try extracting the audio from the video
      except OSError:
        time.sleep(15) #if the downloaded video hasn't yet shown up in the working directory, wait 15 seconds

      audio_clip = VideoFileClip(fname).audio #extracts the audio from the video
      audio_clip.write_audiofile(fname[:-4] + '.wav') #download the audio in wav format
      audio_clip.close()

      if chunks == True:
        if 'Output_Chunked_Audios' not in os.listdir(): #creates the two output folders if they do not yet exist
          os.mkdir('Output_Chunked_Audios')
        if 'Output_Prepared_CSVs' not in os.listdir():
          os.mkdir('Output_Prepared_CSVs')

        sig, sr = librosa.load(fname[:-4] + '.wav', sr = 16000) #loads the audio into a signal array and sampling rate using librosa

        with open(f'Output_Prepared_CSVs/{fname[:-4]}.csv' , 'w') as csvfile:
          writer = csv.writer(csvfile)
          counter = 1 #provides a count for the filenames to align them with the audios
          scaler = 1 #serves as the number which finds the correct upperbound for each 30 second chunk
          lowerbound = 0 #serves as the number for the lowerbound for each 30 second chunk
          finaliter = False #allows for the final iteration to be included
          hold = [] #holds the output for each 30 second chunk

          for i, info in enumerate(output.items()):
            digits = re.findall('[\d]', info[0][-4:]) #extract the frame number from the frame name
            if len(digits) == 4:
              framenum = int(digits[0] + digits[1] + digits[2] + digits[3])
            elif len(digits) == 3:
              framenum = int(digits[0] + digits[1] + digits[2])
            elif len(digits) == 2:
              framenum = int(digits[0] + digits[1])
            else:
              framenum = int(digits[0])

            if i == 0: #if it's the first iteration, pass these conditionals so that the scaler can be calculated
              pass
            elif i == len(output) - 1: #if it's the final iteration, change the Boolean so that the final iteration can be included in the output (see below) and save the final audio chunk with content (which is not necessarily the last audio chunk, ergo this saving process must happen here)
              finaliter = True
              wavfile = f'{fname[:-4]}_chunk_{counter}.wav' #creates the local pathname
              chunk = sig[((scaler - 1) * 480000) : ((scaler - 1) * 480000) + 480000] #parses the audio into chunks of 30 seconds where dialog occurs
              sf.write(f'Output_Chunked_Audios/{wavfile}', chunk, samplerate = sr, subtype = 'PCM_24') #downloads the chunked audio data
              chunk = sig[((scaler) * 480000) : ((scaler) * 480000) + 240000] #DEBUG LINE: creates a chunk of 15 seconds to catch any remaining dialog, if it exists
              sf.write(f'Output_Chunked_Audios/{wavfile[:-4]}b.wav', chunk, samplerate = sr, subtype = 'PCM_24') #DEBUG LINE: dowloads this short chunk
              pass
            else: #otherwise (for all other cases) evaluate the following
              if lowerbound <= framenum <= scaler*15: #if the frame number (still) falls within the same 30 second bounds, skip to keep extending the 'hold' list for the current chunk
                pass
              else: #if the iteration is no longer in the previous running 30 second chunk, output the list housing the text in that chunk, advance the counter by 1, and empty the 'hold' list for the next iteration
                wavfile = f'{fname[:-4]}_chunk_{counter}.wav' #creates the local pathname
                chunk = sig[((scaler - 1) * 480000) : ((scaler - 1) * 480000) + 480000] #parses the audio into chunks of 30 seconds where dialog occurs
                sf.write(f'Output_Chunked_Audios/{wavfile}', chunk, samplerate = sr, subtype = 'PCM_24') #downloads the chunked audio data
                content = ' | '.join(hold) #prepares the content for output
                writer.writerow([wavfile, content]) #write the output csv for finetuning the Whisper model with path location in column 1 and text content in column 2
                counter += 1
                hold = []

            scaler = int(framenum / 15) + (framenum % 15 > 0) #calculates the scaler which finds the appropriate upperbound for any given frame number
            lowerbound = (scaler - 1) * 15 #defines the lower bound of the 30 second chunk

            if lowerbound <= framenum <= scaler*15: #if the frame number lies within a specific 30 second chunk (which it must, since both values are tailored to the frame - might be redundant?)
              hold.extend(info[1]) #extend the 'hold' list with texts that belong to the same 30 second chunk

            if finaliter == True: #if it's the final iteration, output the final list
              content = ' | '.join(hold) #prepares the content for output
              writer.writerow([wavfile, content]) #write the output csv for finetuning the Whisper model with path location in column 1 and text content in column 2
              finaliter = False #resets the Boolean

        if audio == False:
          os.remove(fname[:-4] + '.wav') #remove the audio file from the working directory if not desired


    ### Saving, i.e. Retaining the Already Saved, Video File ###
    if video == False:
      os.remove(fname)

    return output


## Working with YouTubeScraper ##
### List of URLs as txt File ###
scraper = YouTubeScraper()
with open('file.txt', 'r') as filein:
  videos = filein.readlines()

for link in videos:
  scraper.researchextractor(link, audio = True, chunks = True, csv_info = True, frames = True, video = True) #can be substituted for the contentextractor

### Single File ###
scraper = YouTubeScraper()
link = 'https://www.youtube.com/link...'
scraper.contentextractor(link) #can be substituted for the researchextractor
