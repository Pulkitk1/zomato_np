"""
Phase 5: UI routes for the restaurant recommendation service.

This package defines a small HTML UI that can be mounted on top of the
existing FastAPI application from Phase 4.
"""

from .ui import router as ui_router

__all__ = ["ui_router"]

