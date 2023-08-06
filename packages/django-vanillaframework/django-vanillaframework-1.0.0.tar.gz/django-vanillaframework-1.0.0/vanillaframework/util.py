"""Utility functions for handling Vanilla Framework in Django."""
import os.path
from pathlib import Path
from django.conf import settings
from .config import get_local_css_path


def has_local_css():
    """Check if there is a local copy of Vanilla Framework in the correct location and return True if so."""
    css = os.path.join(settings.STATIC_ROOT, get_local_css_path()) if hasattr(settings,
                                                                              "STATIC_ROOT") else get_local_css_path()
    return Path(css).is_file()
