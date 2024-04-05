"""The following code calculates the total duration of a directory of audio files in seconds, minutes, or hours, as well as the total memory taken up by the audio files.

These tools were developed for the EURAC internship project finetuning the Whisper LLM to South Tyrolean German dialect."""

#Set-up
import librosa
import glob
import os

%cd '/path/to/desired/working/directory'


#Audio length calculator
audio_lengths = [librosa.get_duration(path = audio) for audio in glob.glob('*.mp3')]
print(f"""The total audio data amounts to:

{sum(audio_lengths)} Seconds (total)
{sum(audio_lengths)/60} Minutes (total)
{sum(audio_lengths)/3600} Hours (total)

i.e. {int(sum(audio_lengths)//3600)}:{int((sum(audio_lengths)%3600)//60)}:{int((sum(audio_lengths)%3600)%60)}.""")


#Audio size calculator
sizes = [os.stat(audio).st_size for audio in glob.glob('*.mp3')]
print(f'The total size of the files are {sum(sizes) / 1e+9} GB, i.e. {sum(sizes)} bytes.')
