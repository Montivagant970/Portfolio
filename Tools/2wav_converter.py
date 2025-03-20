"""The following code converts all files in a given directory to .wav, if in .mp3 or .m4a formats.

This tool was developed for my master's thesis on "Automatic Speech Recognition for the South Tyrolean German Dialects"."""

## Set-up ##
import glob
import librosa
from pydub import AudioSegment
import os

os.chdir('/path/to/desired/working/directory')

## Converting all .mp3 to .wav
audiopaths2change = [audio for audio in glob.glob('*.mp3')]
for audio in audiopaths2change:
  try:
    sound = AudioSegment.from_mp3(audio)
    sound.export(audio[:-4] + ".wav", format="wav")
    os.remove(audio)
  except:
    print(f'Audio {audio} could not be converted.')

## Converting all .m4a to .wav
audiopaths2change = [audio for audio in glob.glob('*.m4a')] #.m4a
for audio in audiopaths2change:
  try:
    sound = AudioSegment.from_file(audio, format='m4a')
    sound.export(audio[:-4] + ".wav", format="wav")
    os.remove(audio)
  except:
    print(f'Audio {audio} could not be converted.')
