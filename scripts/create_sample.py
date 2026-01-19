import pandas as pd
import json
import os
import shutil

# Config
RAW_PATH = "data/raw"
SAMPLE_PATH = "data/sample"
SAMPLE_SIZE = 100

def create_sample_data():
    if not os.path.exists(SAMPLE_PATH):
        os.makedirs(SAMPLE_PATH)
        print(f"[INFO] Created directory: {SAMPLE_PATH}")

    # Load file list
    json_path = os.path.join(RAW_PATH, "file_list.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        file_list = json.load(f)

    for file_info in file_list:
        file_name = file_info['name']
        src_path = os.path.join(RAW_PATH, file_name)
        dst_path = os.path.join(SAMPLE_PATH, file_name)
        
        print(f"[INFO] Processing {file_name}...")
        
        try:
            # Read minimal rows using pandas
            df = pd.read_csv(
                src_path,
                sep=file_info['sep'],
                header=file_info['header'],
                names=file_info['cols'],
                encoding=file_info.get('encoding', 'utf-8'),
                nrows=SAMPLE_SIZE,
                engine='python' # Safer for varied separators
            )
            
            # Save to sample directory
            # If header was None, we save without header, but we provided names in read_csv.
            # However, the original file might NOT have a header.
            # If file_info['header'] is None, original file has no header.
            # So we should write without header.
            
            has_header = file_info['header'] is not None
            
            df.to_csv(
                dst_path, 
                sep=file_info['sep'], 
                index=False, 
                header=has_header,
                encoding='utf-8'
            )
            print(f"[SUCCESS] Created sample for {file_name} ({len(df)} rows)")
            
        except Exception as e:
            print(f"[ERROR] Failed to process {file_name}: {e}")

    # Copy metadata files
    try:
        shutil.copy(json_path, os.path.join(SAMPLE_PATH, "file_list.json"))
        print(f"[INFO] Copied file_list.json")
        
        stopwords_src = os.path.join(RAW_PATH, "stopwords.txt")
        if os.path.exists(stopwords_src):
            shutil.copy(stopwords_src, os.path.join(SAMPLE_PATH, "stopwords.txt"))
            print(f"[INFO] Copied stopwords.txt")
            
    except Exception as e:
        print(f"[ERROR] Failed to copy metadata files: {e}")

if __name__ == "__main__":
    create_sample_data()
