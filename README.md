# Notebook Markdown Translator

A powerful Python tool for extracting markdown cells from Jupyter notebooks, facilitating translation through LLMs, and applying translations back to create multilingual notebooks.

## 🌟 Features

- 📥 Extract markdown cells from Jupyter notebooks to structured JSON
- 🔄 Apply translated content back to create new notebooks
- 📊 Progress tracking with rich console output
- 🛡️ Type-safe implementation with comprehensive error handling
- 🎯 Command-line interface for easy automation
- 🔍 Preserves notebook structure and metadata

## 🚀 Quick Start

### Installation

1. Clone the repository:

```bash
git clone https://github.com/byigitt/notebook-markdown-translator.git
cd notebook-markdown-translator
```

2. Create a virtual environment and install using uv:

```bash
uv venv
. .venv/Scripts/activate  # On Windows
uv pip install -e .
```

### Basic Usage

1. Extract markdown from a notebook:

```bash
python -m notebook_translator extract path/to/your/notebook.ipynb
```

This creates a `notebook.md.json` file containing all markdown cells in a simple format:

```json
{
  "cells": {
    "0": "# Introduction\nThis is the first cell",
    "5": "## Data Processing\nHere's how we process the data",
    "8": "### Results\nThese are our findings"
  }
}
```

2. Translate the content:

   - Use the generated JSON file with your preferred LLM
   - Only the text content needs to be translated
   - Cell indices must remain unchanged

Here's a recommended prompt for LLM translation (customize the target language as needed):

```
You are an expert in Turkish translation and an experienced educator. Translate the following content into Turkish while strictly adhering to these guidelines:

- Do not translate specific terms such as 'token'; they should remain in their original language.
- Translate the descriptive parts into Turkish.
- Do not modify the markdown structure; preserve it exactly as it is.
- Maintain the JSON format precisely, translating only the text content inside the objects.
- Ensure the translation follows all Turkish grammar, spelling, and punctuation rules meticulously.
- Do not alter the context, logic, or meaning of the text; stay within the given context at all times.
- Present the translation in a clear and instructional manner to make it easy to understand.
- Do not translate terminology related to the code or code blocks.

Here's your json content:
[Paste your JSON content here]
```

Example translation:

```json
{
  "cells": {
    "0": "# Giriş\nBu ilk hücre",
    "5": "## Veri İşleme\nVerileri nasıl işlediğimiz burada anlatılıyor",
    "8": "### Sonuçlar\nBulgularımız bunlar"
  }
}
```

3. Apply translations back:

```bash
python -m notebook_translator apply translated.md.json original_notebook.ipynb
```

### Command Options

#### Extract Command

```bash
python -m notebook_translator extract <notebook.ipynb> [options]
```

Options:

- `-o, --output PATH`: Custom output path for the JSON file (default: `<notebook_name>.md.json`)

#### Apply Command

```bash
python -m notebook_translator apply <markdown.json> <notebook.ipynb> [options]
```

Options:

- `-o, --output PATH`: Custom output path for the translated notebook (default: `<notebook_name>_translated.ipynb`)

## 🛠️ Development

### Setup Development Environment

1. Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

2. Run tests:

```bash
pytest
```

### Project Structure

```
notebook-markdown-translator/
├── src/
│   └── notebook_translator/
│       ├── __init__.py
│       ├── cli.py                 # Command-line interface
│       ├── markdown_extractor.py  # Core extraction logic
│       └── types.py               # Pydantic models
└── pyproject.toml                 # Project configuration
```

## 🔒 Type Safety & Error Handling

- Full type hints with runtime validation using Pydantic
- Comprehensive error messages with rich console output
- Proper exception hierarchy for different error cases
- MyPy strict mode enabled for static type checking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Latest Updates

- Simplified JSON structure to focus only on markdown content
- Added translation prompt template
- Added example of translation workflow
- Improved error handling with rich console output
- Added progress bars for extraction and application
- Fixed metadata type validation
- Added comprehensive .gitignore
- Added proper project structure with src layout
