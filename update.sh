#!/bin/bash

echo "Updating the AwesomeMalDevLinks collection..."

python app/scrape_urls.py
python app/llm_summarize.py
bash app/makearchive.sh

echo "Done"