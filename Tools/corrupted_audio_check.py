"""The following function checks all audio files at a given directory and checks for corruption.

This tool was developed for my master's thesis on "Automatic Speech Recognition for the South Tyrolean German Dialects"."""

import glob
import subprocess
import os

os.chdir('/path/to/desired/working/directory')

def check_audio_integrity(audio_files):
    """
    Tests each audio file for integrity using FFmpeg.
    Reports any corrupt or problematic files.

    :param audio_files: List of audio file paths.
    :return: Dictionary with results for each file.
    """
    results = {}

    for audio in audio_files:
        try:
            # Run ffmpeg to analyze the file
            result = subprocess.run(
                ['ffmpeg', '-v', 'error', '-i', audio, '-f', 'null', '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stderr_output = result.stderr.decode('utf-8')

            # Check if errors were reported
            if stderr_output:
                results[audio] = {"status": "corrupt", "details": stderr_output}
                print(f"Corrupt: {audio}\nDetails: {stderr_output}")
            else:
                results[audio] = {"status": "clean"}
                print(f"Clean: {audio}")
        except Exception as e:
            # Handle unexpected errors
            results[audio] = {"status": "error", "details": str(e)}
            print(f"Error processing {audio}: {e}")

    return results

# List of audio file paths
audios = [audio for audio in glob.glob('*.wav')]

# Run the integrity check
integrity_results = check_audio_integrity(audios)

# Print summary
print("Integrity Check Results:", integrity_results)
