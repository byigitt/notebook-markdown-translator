"""Command-line interface for notebook translation."""

from pathlib import Path
from typing import Optional
import typer
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress

from .markdown_extractor import MarkdownExtractor
from .types import MarkdownContent

app = typer.Typer(help="Notebook markdown translation tool")
console = Console()


@app.command()
def extract(
    notebook_path: Path = typer.Argument(
        ..., 
        help="Path to the input notebook",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Path to save the extracted markdown JSON"
    )
) -> None:
    """Extract markdown cells from a Jupyter notebook."""
    try:
        with Progress() as progress:
            task = progress.add_task("Extracting markdown...", total=100)
            
            extractor = MarkdownExtractor(notebook_path)
            progress.update(task, advance=50)
            
            content = extractor.extract_markdown()
            progress.update(task, advance=25)
            
            if output_path is None:
                output_path = notebook_path.with_suffix('.md.json')
            
            extractor.save_markdown_content(content, output_path)
            progress.update(task, advance=25)
        
        rprint(f"[green]Successfully extracted markdown to:[/] {output_path}")
        rprint(f"[blue]Total markdown cells:[/] {len(content.cells)}")
    
    except Exception as e:
        rprint(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(1)


@app.command()
def apply(
    markdown_path: Path = typer.Argument(
        ...,
        help="Path to the markdown JSON file",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    notebook_path: Path = typer.Argument(
        ...,
        help="Path to the original notebook",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Path to save the translated notebook"
    )
) -> None:
    """Apply translated markdown back to a notebook."""
    try:
        with Progress() as progress:
            task = progress.add_task("Applying translations...", total=100)
            
            # Load translations
            with open(markdown_path, 'r', encoding='utf-8') as f:
                import json
                translations = MarkdownContent.model_validate(json.load(f))
            progress.update(task, advance=30)
            
            # Setup output path
            if output_path is None:
                stem = notebook_path.stem
                output_path = notebook_path.with_stem(f"{stem}_translated")
            
            # Apply translations
            extractor = MarkdownExtractor(notebook_path)
            progress.update(task, advance=35)
            
            extractor.apply_translations(translations, output_path)
            progress.update(task, advance=35)
        
        rprint(f"[green]Successfully applied translations to:[/] {output_path}")
    
    except Exception as e:
        rprint(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(1)


def main() -> None:
    """Entry point for the CLI."""
    app() 