import os
import json
import glob
import argparse
from sentence_transformers import SentenceTransformer


def read_jsonl(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def write_jsonl(data, file_path):
    with open(file_path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def process_embedding(model, input_data):
    input_text = input_data["input"]
    embedding = model.encode([input_text])[0]

    output_data = {
        "model": "text-embedding-ada-002",
        "input": input_text,
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index": 0,
                "embedding": embedding.tolist()
            }
        ],
        "model": "text-embedding-ada-002-v2",
        "usage": {
            "prompt_tokens": 0,  # Fill in the correct prompt_tokens
            "total_tokens": 0    # Fill in the correct total_tokens
        }
    }

    return output_data


def process_file(model, input_file_path, output_folder):
    input_data = list(read_jsonl(input_file_path))

    output_data = [process_embedding(model, data) for data in input_data]

    output_file_name = os.path.basename(input_file_path).replace(".jsonl", "_sbertout.jsonl")
    output_file_path = os.path.join(output_folder, output_file_name)
    write_jsonl(output_data, output_file_path)


def main(args):
    model = SentenceTransformer('all-mpnet-base-v2')

    os.makedirs(args.output_folder, exist_ok=True)

    jsonl_files = glob.glob(os.path.join(args.input_folder, "*_*.jsonl"))

    for file_path in jsonl_files:
        process_file(model, file_path, args.output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSONL files and generate embeddings.')
    parser.add_argument('--input-folder', required=True, help='Path to the folder containing input JSONL files.')
    parser.add_argument('--output-folder', required=True, help='Path to the folder where the output JSONL files will be written.')

    args = parser.parse_args()
    main(args)
