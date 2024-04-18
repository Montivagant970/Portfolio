"""YouTubeScraper is a class containing two tools for working with YouTube videos: contentextractor and researchextractor.

contentextractor is a simple method which downloads the full video and audio to the specified working directory. To specify not wanting one or the other, 
the respective arguments must be set to False (see below under method definition for more information).

researchextractor was developed as a tool for preparing videos with embedded subtitles and their respective audios for the finetuning of the Whisper LLM. 

The method allows the user to:
(1) save audio and video files
(2) create, save, and process frames from the video using OCR to extract embedded subtitle text
(3) chunk the audio and OCR output into the desired Whisper input (csv file with pathname in column 1 and text content in column 2; 30 second 
audio chunks corresponding to each row in the csv)
(4) output an informational csv for debugging, which includes the frame name, the mean OCR score at that frame, and 
the OCR transcription. 

The return output of the researchextractor is a defaultdict with the frame names as keys and the OCR transcription as its respective value.

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
       using OCR to extract embedded subtitle text; chunk the audio and OCR output into the desired Whisper input (csv file with pathname in column 1 and text content in column 2; 30 second 
       audio chunks corresponding to each row in the csv); and an informational csv for debugging, which includes the frame name, the mean OCR score at that frame, and the OCR transcription.
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
        chunks = [sig[chunk : chunk + 480000] for chunk in range(0, len(sig), 480000)] #parses the audio into chunks of 30 seconds
        for i, chunk in enumerate(chunks):
          sf.write(f'Output_Chunked_Audios/{fname[:-4]}_chunk_{i+1}.wav', chunk, samplerate = sr, subtype = 'PCM_24') #downloads the chunked audio data

        with open(f'Output_Prepared_CSVs/{fname[:-4]}.csv' , 'w') as csvfile:
          writer = csv.writer(csvfile)
          multiplier = 1 #defines the frames selected and the upperbound for each 30 second chunk
          lowerbound = 0 #the bottom bound of the 30 second chunk
          hold = []
          while multiplier != len(output):
            for frame, text in output.items(): #extract the frame number from the frame name
              digits = re.findall('[\d]', frame[-4:])
              if len(digits) == 4:
                framenum = int(digits[0] + digits[1] + digits[2] + digits[3])
              elif len(digits) == 3:
                framenum = int(digits[0] + digits[1] + digits[2])
              elif len(digits) == 2:
                framenum = int(digits[0] + digits[1])
              else:
                framenum = int(digits[0])

              if lowerbound <= framenum <= multiplier*15: #if the frame number lies within a specific 30 second chunk
                hold.extend(text) #gather texts that belong to the same 30 second chunk

            if hold == []:
              break
            else:
              path = os.getcwd() + '/Output_Prepared_CSVs' + f'/{fname[:-4]}_chunk_{multiplier}.wav' #creates the local pathname
              content = ' | '.join(hold) #prepares the content for output
              writer.writerow([path, content]) #write the output csv for finetuning the Whisper model with path location in column 1 and text content in column 2

            lowerbound = multiplier * 15
            multiplier += 1
            hold = []

        if audio == False:
          os.remove(fname[:-4] + '.wav') #remove the audio file from the working directory if not desired


    ### Saving, i.e. Retaining the Already Saved, Video File ###
    if video == False:
      os.remove(fname)

    return output