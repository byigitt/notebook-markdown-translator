"""Module for extracting markdown content from Jupyter notebooks."""

from pathlib import Path
import json
import nbformat

from .types import MarkdownContent


class MarkdownExtractor:
    """Extracts and manages markdown content from Jupyter notebooks."""

    def __init__(self, notebook_path: str | Path) -> None:
        """
        Initialize the markdown extractor.

        Args:
            notebook_path: Path to the Jupyter notebook file

        Raises:
            FileNotFoundError: If notebook file doesn't exist
            ValueError: If the notebook format is invalid
        """
        self.notebook_path = Path(notebook_path)
        if not self.notebook_path.exists():
            raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    def extract_markdown(self) -> MarkdownContent:
        """
        Extract markdown cells from the notebook.

        Returns:
            MarkdownContent: Container with extracted markdown cells

        Raises:
            ValueError: If notebook cannot be parsed
        """
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)

            markdown_cells = {}
            for idx, cell in enumerate(notebook.cells):
                if cell.cell_type == 'markdown':
                    markdown_cells[idx] = cell.source

            return MarkdownContent(cells=markdown_cells)
        except Exception as e:
            raise ValueError(f"Failed to parse notebook: {str(e)}")

    def save_markdown_content(self, content: MarkdownContent, output_path: str | Path) -> None:
        """
        Save extracted markdown content to a JSON file.

        Args:
            content: MarkdownContent to save
            output_path: Path where to save the JSON file

        Raises:
            IOError: If writing to file fails
        """
        try:
            output_path = Path(output_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(content.model_dump(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Failed to save markdown content: {str(e)}")

    def apply_translations(
        self, 
        translations: MarkdownContent, 
        output_path: str | Path
    ) -> None:
        """
        Apply translations back to a new notebook file.

        Args:
            translations: MarkdownContent with translated content
            output_path: Path where to save the new notebook

        Raises:
            ValueError: If translations don't match the notebook structure
            IOError: If writing the new notebook fails
        """
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)

            # Apply translations
            for idx, cell in enumerate(notebook.cells):
                if idx in translations.cells and cell.cell_type == 'markdown':
                    cell.source = translations.cells[idx]

            # Save the new notebook
            output_path = Path(output_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                nbformat.write(notebook, f)
        except Exception as e:
            raise IOError(f"Failed to apply translations: {str(e)}") 