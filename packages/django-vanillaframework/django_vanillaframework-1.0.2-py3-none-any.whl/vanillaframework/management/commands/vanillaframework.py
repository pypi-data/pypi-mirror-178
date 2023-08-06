"""Vanilla Framework management command."""
import os.path
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import urllib.request
from vanillaframework import __version__, config


class Command(BaseCommand):
    """Vanilla Framework management command class."""

    help = "Manage Vanilla Framework install within the Django project."

    def add_arguments(self, parser):
        """Add -- args to the management command."""
        parser.add_argument("-i", "--install", action='store_true', help="Install Vanilla Framework locally")
        parser.add_argument("--css", action='store_true',
                            help="Use the min.css version of Vanilla Framework (no customization)")
        parser.add_argument("--use-version", type=str,
                            help="The version of Vanilla Framework to use, defaults to settings version or newest")
        parser.add_argument("--static-folder", type=str, help="The static folder to put Vanilla Framework in",
                            default=settings.STATIC_ROOT)

    def handle(self, *args, **options):
        """Handle Vanilla Framework management commands."""
        if options["install"]:
            self.handle_install(*args, **options)

    def handle_install(self, *args, **options):
        """Handle Vanilla Framework install command."""
        version_to_get = options["use_version"] if "use_version" in options and options[
            "use_version"] is not None else config.get_version()

        if "static_folder" not in options:
            print("Error: no static folder provided. Use --static-folder or add a STATIC_ROOT to settings.")
            return

        if options["css"]:
            Path(os.path.join(options["static_folder"], 'css')).mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(config.get_min_css_url(version_to_get), os.path.join(options["static_folder"],
                                                                                            config.get_local_css_path(
                                                                                                version_to_get)))
        else:
            Path(options["static_folder"]).mkdir(parents=True, exist_ok=True)
            npm_result = subprocess.run(
                ["npm", "install", "--prefix", options['static_folder'], f"vanilla-framework@{version_to_get}"])

            if npm_result.returncode != 0:
                print("Error: npm failed to download vanilla-framework. Make sure you have npm installed and in your")
                print("PATH (https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)")
                return

            vanilla_filename = os.path.join(options["static_folder"], config.get_local_sass_path())
            if Path(vanilla_filename).is_file():
                print(f"Note: {config.get_local_sass_path()} already exists, leaving it alone.")
                print()
            else:
                vanilla_file = open(vanilla_filename, "w")
                vanilla_file.write(
                    """// Override default Vanilla settings here,


                    // Import the framework
                    @import 'node_modules/vanilla-framework/scss/build.scss';

                    // Include Vanilla Framework
                    @include vanilla;
                    """.replace("                    ", ""))
                vanilla_file.close()

            if 'compressor' not in settings.INSTALLED_APPS:
                print("The sass version of vanilla-framework uses django-compressor. Add 'compressor' to your")
                print("INSTALLED_APPS list in your settings file, and make sure django-compressor is installed")
                print()

            scss_precomp_available = False
            if hasattr(settings, "COMPRESS_PRECOMPILERS"):
                for precompiler in settings.COMPRESS_PRECOMPILERS:
                    if precompiler[0] == 'text/x-scss':
                        scss_precomp_available = True
                        break

            if not scss_precomp_available:
                print("The sass version of vanilla-framework needs a sass precompiler to work with Django. Install")
                print("one, such as django-libsass, then add it to your COMPRESS_PRECOMPILERS list in settings.")
                print("For example, using django-libsass, add:")
                print("COMPRESS_PRECOMPILERS = (")
                print("    ('text/x-scss', 'django_libsass.SassCompiler'),")
                print(")")
                print()

        if "use_version" in options and options["use_version"] is not None:
            print("You have downloaded a specific version of Vanilla Framework. To use it, add:")
            print(f"VANILLAFRAMEWORK_VERSION = {version_to_get}")
            print("to your settings file.")

    def get_version(self):
        """Get the django-vanillaframework version."""
        return __version__
