# Batch Transcribe
Python script for transcribing all audio files in a specified directory using whisper-ctranslate2 with parallel processing.

## Usage

### Transcribe a specific directory
```bash
python3 ~/batch_transcribe.py /path/to/audio/files
```
 
### With custom output directory
```bash
python3 ~/batch_transcribe.py /path/to/audio/files -o /path/to/output
```
 
### Adjust parallel workers (default: 2)
```bash
python3 ~/batch_transcribe.py /path/to/audio/files -w 4
```
 
### Process only specific file types
```bash
python3 ~/batch_transcribe.py /path/to/audio/files -e mp3 wav
```
## Settings
 
Edit the `SETTINGS` dictionary in `batch_transcribe.py`:
```python
SETTINGS = {
    "device": "cpu",
    "patience": 2,
    "suppress_tokens": "",
    "word_timestamps": "True",
    "model": "large-v2",
    "language": "ja",
    "task": "transcribe",
    "output_format": "srt",
}
```
