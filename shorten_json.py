import json


def shorten_jsonl_file(filename):
    short_filename = filename.replace('.jsonl', '_short.jsonl')
    with open(filename, 'r') as infile, open(short_filename, 'w') as outfile:
        lines = []
        for i, line in enumerate(infile):
            if i >= 10000:
                break
            lines.append(line)
        outfile.writelines(lines)


shorten_jsonl_file("requests_for_openai_embeddings.jsonl")