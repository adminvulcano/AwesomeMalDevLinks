# AwesomeMalDevLinks - Data Processing Pipeline

This directory contains scripts to scrape security research URLs, generate LLM summaries, and archive the results.

This readme has been AI generated. 


## Setup with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root with the following API keys:

```bash
# Required for scraping URLs
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Required for LLM summaries
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Full Pipeline

Run the complete pipeline using the update script:

```bash
bash update.sh
```

This executes three steps in sequence:

1. **Scrape URLs** - `python app/scrape_urls.py`
2. **Generate LLM summaries** - `python app/llm_summary.py`
3. **Create archives** - `bash app/makearchive.sh`

### Individual Steps

#### 1. Scrape URLs

Reads URLs from `data/in/*.txt` files and scrapes content using Firecrawl:

```bash
python app/scrape_urls.py
```

- **Input**: Text files in `data/in/` (one URL per line)
- **Output**: Markdown, HTML, and JSON files in `data/out/<topic>/`
- Each topic file (e.g., `maldev.txt`) creates a corresponding output directory

#### 2. Generate LLM Summaries

Processes scraped markdown files and generates AI-powered summaries:

```bash
# Process all files
python app/llm_summary.py

# Test mode (process only 3 random files)
python app/llm_summary.py --test
```

- **Input**: `.md` files in `data/out/<topic>/`
- **Output**: `.llm` files alongside each markdown file
- Skips files that already have summaries
- Uses OpenAI GPT-5.2 for summarization

#### 3. Create Archives

Packages results into zip files:

```bash
bash app/makearchive.sh
```

- **Input**: `.md` files in `data/out/<topic>/`
- **Output**: `<topic>.zip` files in `data/result/`

## Directory Structure

```
data/
├── in/           # Input URL lists (*.txt)
├── out/          # Scraped content and summaries
│   └── <topic>/  # One directory per topic
│       ├── *.md  # Scraped markdown
│       ├── *.html # Scraped HTML
│       ├── *.json # Metadata
│       └── *.llm  # LLM summaries
└── result/       # Zip archives
```

## Notes

- The scraper skips URLs that have already been processed (checks for existing output files)
- LLM summarizer skips files that already have `.llm` summaries
- Content longer than 256,000 characters is truncated before summarization
- API calls include retry logic (3 attempts) for reliability
