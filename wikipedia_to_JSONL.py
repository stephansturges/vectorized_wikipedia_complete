import os
import json
import re
import tiktoken

from concurrent.futures import ProcessPoolExecutor

def cut_string_before_substring(input_string, substring):
    # Find the index of the first occurrence of the substring
    index = input_string.find(substring)

    # If the substring is not found, return the original string
    if index == -1:
        return input_string

    # Otherwise, return the substring of the input string up to the index
    return input_string[:index]




def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("gpt2")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_input_string(input_str, max_tokens, overlap_tokens, num_tokens_from_string):
    if num_tokens_from_string(input_str) <= max_tokens:
        return [input_str]

    parts = [input_str]
    while any(num_tokens_from_string(part) > max_tokens for part in parts):
        for idx, part in enumerate(parts):
            if num_tokens_from_string(part) > max_tokens:
                part_length = len(part)
                half_length = part_length // 2
                overlap_start = max(0, half_length - overlap_tokens // 2)
                overlap_end = min(part_length, half_length + overlap_tokens // 2)

                left_part = part[:overlap_end]
                right_part = part[overlap_start:]

                parts[idx] = left_part
                parts.insert(idx + 1, right_part)

    return parts

def process_file(filename):
    json_objects = []

    with open(os.path.join(input_dir, filename), 'r') as f:
        json_data = json.load(f)

    # Extract the title and text fields from the JSON data
    title = json_data['title']
    text = json_data['text']

    # Clear the text field
    string = "".join(str(x) for x in text)
    head, sep, tail = string.partition('==References')
    string = head.replace("{| |}", "").replace("()", "")
    string = re.sub('{[^>]+}', '', string)

    head, sep, tail = string.partition('{|')
    string = head

#    string = cut_string_before_substring('==Refere')

    head, sep, tail = string.partition('==Refere')
    string = head
    head, sep, tail = string.partition('== Refernces')
    string = head
    head, sep, tail = string.partition('== REfe')
    string = head
    head, sep, tail = string.partition('== refere')
    string = head
    head, sep, tail = string.partition('== Refe')
    string = head
    head, sep, tail = string.partition('== Refere')
    string = head
    head, sep, tail = string.partition('== Refrence')
    string = head
    # head, sep, tail = string.partition('== Other')
    # string = head
    # head, sep, tail = string.partition('==Other')
    # string = head
    head, sep, tail = string.partition('== Other web')
    string = head
    head, sep, tail = string.partition('==Other web')
    string = head
    head, sep, tail = string.partition('==Other wbes')
    string = head
    head, sep, tail = string.partition('== Notes')
    string = head
    head, sep, tail = string.partition('==Notes')
    string = head
    head, sep, tail = string.partition('== Sources')
    string = head
    head, sep, tail = string.partition('==Sources')
    string = head
    head, sep, tail = string.partition('== sources')
    string = head
    head, sep, tail = string.partition('== Source')
    string = head
    head, sep, tail = string.partition('==Source')
    string = head
    head, sep, tail = string.partition('== source')
    string = head
    # Create the input string for the JSON object
    
    input_str = f'Title: {title} Content: {string}'

    # Tokenize the input string and get the token count
    
    # Tokenize the input string and get the token count
    token_count = num_tokens_from_string(str(input_str))


    max_tokens = 4000
    overlap_tokens = 200

    # Split the input string if it has more than max_tokens
    
    if token_count > max_tokens:
        input_substrs = split_input_string(input_str, max_tokens, overlap_tokens, num_tokens_from_string)

        for input_substr in input_substrs:
            json_obj = {
                'model': 'text-embedding-ada-002',
                'input': input_substr
            }
            json_objects.append(json_obj)
    else:
        json_obj = {
            'model': 'text-embedding-ada-002',
            'input': input_str
        }
        json_objects.append(json_obj)

    return json_objects

input_dir = './wikiplaintext/'
output_file_pattern = './jsonlfiles/requests_for_openai_embeddings_{:03d}.jsonl'



# Number of cores you want to use for parallel processing
num_cores = 4

# Get a list of all filenames in the input directory
filenames = os.listdir(input_dir)[0:3]

# Process the files in parallel using a process
# Get a sorted list of all filenames in the input directory
filenames = sorted(os.listdir(input_dir))

# Define the chunk size (number of input JSON files to process at once)
chunk_size = 10000

# Calculate the number of chunks
num_chunks = (len(filenames) + chunk_size - 1) // chunk_size

for chunk_idx in range(num_chunks):
    # Calculate the start and end indices for the current chunk
    start_idx = chunk_idx * chunk_size
    end_idx = min((chunk_idx + 1) * chunk_size, len(filenames))

    # Get the list of filenames for the current chunk
    chunk_filenames = filenames[start_idx:end_idx]

    # Process the files in the current chunk in parallel using a process pool
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(executor.map(process_file, chunk_filenames))

    # Combine the results from all processes for the current chunk
    all_json_objects = [json_obj for sublist in results for json_obj in sublist]

    # Write the combined list of JSON objects to a JSONL file
    output_file = output_file_pattern.format(chunk_idx)
    with open(output_file, 'w') as f:
        for json_obj in all_json_objects:
            f.write(json.dumps(json_obj) + '\n')
