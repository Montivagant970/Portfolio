"""elantranscriber extracts text data from ELAN files and automatically saves a transcription to the specified directory.

The function takes four arguments: 
(1) the name of the audio file as a string, 
(2) the path to the recipent directory for the output, 
(3) the option to produce an additional transcription with timestamps and speaker IDs, 
(4) the option to set the upperbound for the number of speakers the function looks for in the file.

NB: The function automatically produces a text-only transcription. Setting the third argument to 'True' outputs a second transcription with timestamps and speaker IDs.
NB: The function is written so as to work even if the upperbound is never reached. Therefore, this argument should always be set higher than the expected number of speakers 
in the files. Due to indexing, the input should be: desired_number_of_speakers + 1. The default limit is set to 10 speakers, if left unspecified.

The function can be used within Google Drive with Google Colab or locally by specifying the desired working directory. The working directory
should house all the ELAN files to be processed.

This project was a tool developed for the EURAC internship project finetuning the Whisper LLM to South Tyrolean German dialect."""

#Set-up
from bs4 import BeautifulSoup
import re
import pickle
import glob

from google.colab import drive 
drive.mount('/content/gdrive')

%cd '/path/to/desired/working/directory'


#elantranscriber
def elantranscriber(audio, out_dir, info = False, num_speakers = 11):
  source = open(audio).read() #reads in the .eaf file
  soup = BeautifulSoup(source, 'xml') #turns the .eaf file into a soup object for scraping

  rcpt_list = [] #creates a recipient list for the scraped content

  for num in range(1, num_speakers): #iterates through each speaker in the file
    try:
      part = soup.find('TIER', attrs = {'LINGUISTIC_TYPE_REF':"default-lt", 'TIER_ID' : f'{audio[:11]}_S{num}'}) #pulls the unit of the ELAN file housing the text and time data. 'f'{audio[:11]}_S{num}'' may need to be updated for the particular structure of the file at hand - this argument is the speaker encoding in the HTML

      for unit in part.find_all('ALIGNABLE_ANNOTATION'): #find the annotations/time data
        sent = unit.get_text().strip().lower() #pulls the text from each annotation

        u = re.sub(r'[#><:¥()↓↑»«°]', '', sent)
        v = re.sub('\s{2}', ' ', u)
        w = re.sub('^\s+', '', v)
        x = re.sub('(xxx)', '[xxx]', w)
        y = re.sub('(hhh)', '[hhh]', x)
        z = re.sub(r'(\s+\?)', '?', y) #cleans the text for unwanted characters, fixes spacing, and updates annotations for laughter [hhh] and incomprehensible segments [xxx]

        startid = unit.attrs['TIME_SLOT_REF1'] #pulls the time reference for the start time of the segment
        endid = unit.attrs['TIME_SLOT_REF2'] #pulls the time reference for the end time of the segment

        tstart = soup.find('TIME_SLOT', attrs = {'TIME_SLOT_ID' : startid}).attrs['TIME_VALUE'] #retrieves the start time from the startid
        tend = soup.find('TIME_SLOT', attrs = {'TIME_SLOT_ID' : endid}).attrs['TIME_VALUE'] #retrieves the end time from the startid

        rcpt_list.append((f'S{num}', z, int(tstart), int(tend))) #appends a list with tuples containing the speaker ID, the segment, and the start and the end times

      sorted_list = sorted(rcpt_list, key = lambda x: x[2]) #sorts the list by order of speaking

      out_stamps = [f'{entry[0]} :: [{entry[2]//60000}:{str(((entry[2]%60000)/60000)*.6)[2:4]} - {entry[3]//60000}:{str(((entry[2]%60000)/60000)*.6)[2:4]}] :: {entry[1]}' for entry in sorted_list] #creates the output for the transcription with timestamps
      out = [f'{entry[1]}' for entry in sorted_list] #creates the output for the transcription

    except AttributeError:
      break

  if info == True: #saves a file with the transcription with timestamps and speaker ID if argument is set to 'True'
    with open(f'{out_dir}/{audio}_transcription_TS.txt', 'w') as fout:
      for line in out_stamps:
        fout.write('%s\n' % line)
  else:
    pass

  with open(f'{out_dir}/{audio}_transcription.txt', 'w') as fout: #saves a file with the transcription
    for line in out:
      fout.write('%s\n' % line)
    print(f'{audio} has been successfully transcribed.')

  return


#Running elantranscriber
destination = '/path/to/desired/output/directory'
for elan in glob.glob('*.eaf'): 
  elan_transcriber(elan[-17:], destination, True) #this indexing needs to be changed for the specific file names being used
