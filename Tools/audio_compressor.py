"""The following definitions compress or decompress all .wav files at a given directory, while also saving safe copies to be deleted after ensuring a successful compression/decompression.

This tool was developed for my master's thesis on "Automatic Speech Recognition for the South Tyrolean German Dialects"."""

import zipfile
from zipfile import ZipFile
import os
import glob
import shutil

%cd '/path/to/desired/working/directory'

## Compressor
def compressor():
  # Create a folder of copies to safeguard against loss
  os.makedirs('safecopies')
  audiopaths2copy = [audio for audio in glob.glob('*.wav')]
  for audio in audiopaths2copy:
    shutil.copy(audio, 'safecopies')
  
  # Define the audios to be zipped
  audiopaths2zip = [audio for audio in glob.glob('*.wav')]
  
  # Run metrics on pre-zipped file sizes
  presizes = [os.path.getsize(audio) for audio in audiopaths2zip]
  pretotal = round((sum(presizes) / 1e+9), 2)
  print(f'Pre-Compression File Size Total Amounts to : {pretotal}GB\n')
  
  # Compress the files
  print('Compressing...\n')
  for audio in audiopaths2zip:
    with ZipFile(audio[:-4] + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
      zip.write(audio, os.path.basename(audio))
    os.remove(audio)
  
  # Run metrics on post-zipped file sizes
  postsizes = [os.path.getsize(audio) for audio in glob.glob('*.zip')]
  posttotal = round((sum(postsizes) / 1e+9), 2)
  print(f'''Pre-Compression File Size Total Amounts to : {posttotal}GB
      That is a reduction of {round(((pretotal - posttotal) / pretotal * 100), 2)}% or {round(pretotal - posttotal, 2)}GB.''')

## Decompressor
def decompressor():
  # Create a folder of copies to safeguard against loss
  os.makedirs('safecopies')
  audiopaths2copy = [audio for audio in glob.glob('*.zip')]
  for audio in audiopaths2copy:
    shutil.copy(audio, 'safecopies')
  
  # Define the audios to be zipped
  audiopaths2unzip = [audio for audio in glob.glob('*.zip')]
  
  # Run metrics on pre-zipped file sizes
  presizes = [os.path.getsize(audio) for audio in audiopaths2unzip]
  pretotal = round((sum(presizes) / 1e+9), 2)
  print(f'Pre-Compression File Size Total Amounts to : {pretotal}GB\n')
  
  # Compress the files
  print('Decompressing...\n')
  for audio in audiopaths2unzip:
    with zipfile.ZipFile(audio, 'r') as zip:
      zip.extractall()
    os.remove(audio)

  # Run metrics on post-zipped file sizes
  postsizes = [os.path.getsize(audio) for audio in glob.glob('*.wav')]
  posttotal = round((sum(postsizes) / 1e+9), 2)
  print(f'''Pre-Compression File Size Total Amounts to : {posttotal}GB
      That is an inflation of {round(((posttotal - pretotal) / posttotal * 100), 2)}% or {round(posttotal - pretotal, 2)}GB.''')
