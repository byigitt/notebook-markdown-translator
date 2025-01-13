"""Type definitions for notebook translation."""

from typing import Dict, List
from pydantic import BaseModel, Field


class MarkdownContent(BaseModel):
    """Collection of markdown cells from a notebook."""
    
    cells: Dict[int, str] = Field(
        default_factory=dict,
        description="Mapping of cell index to markdown content"
    ) 