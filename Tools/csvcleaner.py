"""csvcleaner takes a semicolon delimited csv UTF-8 file from Excel and converts it into a comma separated csv file in an effort to standardize file types.

The function can be used within Google Drive with Google Colab or locally by specifying the desired working directory. The working directory
should house the csv file to be processed.

This tool was developed for the EURAC internship project finetuning the Whisper LLM to South Tyrolean German dialect."""

## Set up ##
import csv
import os

os.chdir('/path/to/desired/working/directory')


## csvcleaner ##
def csvcleaner(file):
  out = {}

  with open(file, encoding='utf-8-sig') as filein:
    reader = csv.reader(filein, delimiter = ',', dialect='excel')
    for row in reader:
      out[row[0]] = row[1] #reads in the CSV file and temporarily stores it in a dictionary

  with open(file, 'w') as csvfile:
      writer = csv.writer(csvfile)
      for path, text in out.items():
        writer.writerow([path, text]) #rewrites the file with the comma delimitation
