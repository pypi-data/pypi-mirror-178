"""Django settings file interaction for determining Vanilla Framework middleware settings."""
from django.conf import settings


def get_version():
    """
    Get the version of Vanilla Framework to use.

    If no version is provided in settings, use the latest available.
    """
    return getattr(settings, "VANILLAFRAMEWORK_VERSION", "3.8.1")


def get_min_css_url(ver=None):
    """
    Get the min.css CDN URL for the provided version of Vanilla Framework.

    If a custom URL or version is provided, use that instead.
    """
    return getattr(settings, "VANILLAFRAMEWORK_MIN_CSS_URL",
                   f"https://assets.ubuntu.com/v1/vanilla-framework-version-{ver if ver else get_version()}.min.css")


def get_local_css_path(ver=None):
    """Get the static file path of the local copy of Vanilla Framework."""
    return getattr(settings, "VANILLAFRAMEWORK_CSS_PATH",
                   f"css/vanilla-framework-version-{ver if ver else get_version()}.min.css")


def get_local_sass_path():
    """Get the static file path of the custom sass file that includes Vanilla Framework."""
    return getattr(settings, "VANILLAFRAMEWORK_PATH", "vanillaframework.scss")
