import json
import csv
import os
import glob
from concurrent.futures import ThreadPoolExecutor

def process_jsonl_file(jsonl_file):
    # Create a corresponding CSV file
    csv_file = os.path.splitext(jsonl_file)[0] + '.csv'
    
    with open(jsonl_file, 'r') as jf, open(csv_file, 'w', newline='') as cf:
        csv_writer = csv.writer(cf)
        
        # Write the header row
        header = ['gpttext']
        header.extend([str(i) for i in range(768)])
        csv_writer.writerow(header)
        
        for line in jf:
            json_data = json.loads(line)
            gpttext = json_data['input']
            embeddings = json_data['data'][0]['embedding']
            
            row = [gpttext]
            row.extend(embeddings)
            csv_writer.writerow(row)

output_folder = './jsonfiles_sbert_out'

# Get all JSONL files in the output folder
jsonl_files = glob.glob(os.path.join(output_folder, '*.jsonl'))

# Process the files in parallel using multithreading
with ThreadPoolExecutor() as executor:
    executor.map(process_jsonl_file, jsonl_files)
