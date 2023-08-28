import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
from multiprocessing import Pool, cpu_count

wiki_xml_file = 'enwiki-20230301-pages-articles-multistream.xml'  # update this
json_save_dir = './wikiplaintext/'

def dewiki(text):
    text = wtp.parse(text).plain_text()
    text = htt(text)
    text = text.replace('\\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def analyze_chunk(text):
    try:
        if '<redirect title="' in text:
            return None
        if '(disambiguation)' in text:
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        content = dewiki(content)
        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as oops:
        print(oops)
        return None

def save_article(article):
    doc = analyze_chunk(article)
    if doc:
        print('SAVING:', doc['title'])
        filename = doc['id'] + '.json'
        with open(json_save_dir + filename, 'w', encoding='utf-8') as outfile:
            json.dump(doc, outfile, sort_keys=True, indent=1, ensure_ascii=False)
    return None

def articles_generator(filename):
    article = ''
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:
                yield article
            else:
                article += line

def main():
    with Pool(int(cpu_count()/2)) as p:
        p.map(save_article, articles_generator(wiki_xml_file))

if __name__ == '__main__':
    main()
