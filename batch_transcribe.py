#!/usr/bin/env python3
"""
Bulk Whisper transcription script
Processes multiple audio files with your preset settings
"""

import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Whisper arguments
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

def transcribe_file(audio_file, output_dir):
    """Transcribe a single audio file"""
    try:
        cmd = [
            "whisper-ctranslate2",
            str(audio_file),
            "--device", SETTINGS["device"],
            "--patience", str(SETTINGS["patience"]),
            "--suppress_tokens", SETTINGS["suppress_tokens"],
            "--word_timestamps", SETTINGS["word_timestamps"],
            "--model", SETTINGS["model"],
            "--language", SETTINGS["language"],
            "--task", SETTINGS["task"],
            "--output_format", SETTINGS["output_format"],
            "--output_dir", str(output_dir),
        ]
        
        print(f"▶ {audio_file.name}")
        result = subprocess.run(cmd, text=True)
        
        if result.returncode == 0:
            print(f"✓ {audio_file.name}\n")
            return True
        else:
            print(f"✗ {audio_file.name}\n")
            return False
    except Exception as e:
        print(f"✗ Error: {audio_file.name}: {e}\n")
        return False

def main():
    parser = argparse.ArgumentParser(description="Bulk transcribe audio files")
    parser.add_argument("input_dir", help="Directory containing audio files")
    parser.add_argument("-o", "--output_dir", help="Output directory (default: same as input)")
    parser.add_argument("-w", "--workers", type=int, default=2, help="Number of parallel workers (default: 2)")
    parser.add_argument("-e", "--extensions", nargs="+", default=["wav", "mp3", "m4a", "flac", "ogg"], 
                       help="Audio file extensions to process")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_dir)
    if not input_path.is_dir():
        print(f"Error: {args.input_dir} is not a valid directory")
        sys.exit(1)
    
    output_dir = Path(args.output_dir) if args.output_dir else input_path
    output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_files = []
    for ext in args.extensions:
        audio_files.extend(input_path.glob(f"*.{ext}"))
        audio_files.extend(input_path.glob(f"*.{ext.upper()}"))
    
    audio_files = sorted(set(audio_files))
    
    if not audio_files:
        print(f"No audio files found in {input_path}")
        sys.exit(1)
    
    print(f"Found {len(audio_files)} audio files to transcribe")
    print(f"Output directory: {output_dir}")
    print()
    
    completed = 0
    
    if args.workers == 1:
        for audio_file in audio_files:
            if transcribe_file(audio_file, output_dir):
                completed += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(transcribe_file, f, output_dir) for f in audio_files]
            for future in as_completed(futures):
                if future.result():
                    completed += 1
    
    print()
    print("=" * 50)
    print(f"Transcription complete! {completed}/{len(audio_files)} successful")
    print("=" * 50)

if __name__ == "__main__":
    main()
