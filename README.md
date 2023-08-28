# vectorized_wikipedia_complete
This is a complete dump of English language Wikipedia vectorized with SBERT all-mpnet-base-v2

# What is the point? 

I created this to be able to insert ALL of Wikipedia in English into a Pinecone / vector database to enable AI chatbots to source content!

It was pretty cool, I was able to make my own plugin for chatGPT which would browse Wikipedia for FACTUAL answers about even the most obscure stuff that is not available directly from the model, allowing it to answer questions where the model just hallucinates random garbage. 

Check out this example: 
https://twitter.com/StephanSturges/status/1652660433193521152?s=20

![image](https://github.com/stephansturges/vectorized_wikipedia_complete/assets/20320678/e37deb29-109c-4cdf-bf34-cdb89856949f)


# This repo contains:

1. some terrible code to convert a downloaded dump of wikipedia to plain text, then to JSON, then to clean up the JSONs, then make long JSONL files of the text
2. some terrible code to run SBERT from sentence-transformers, specifically model all-mpnet-base-v2 and create vector embeddings for each item in the JSON files


# The data is here:

Grab the actual outputs on Kaggle, split into two repos because it exceeds the file size, here:

# Support Wikipedia!

Don't forget to support the Wikimedia foundation for all the great content https://donate.wikimedia.org

# License

Copyright 2023 Stephan Sturges

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
