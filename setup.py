# setup for srt-convert
#te: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "textgrid-convert"
DESCRIPTION = "textgrid-convert converts audio transcripts such as sbv or srt files to Praat and DARLA compatible TextGrids."
URL ="https://github.com/patrickschu/textgrid-convert/"
EMAIL ="patrickschultz@utexas.edu"
AUTHOR = "Patrick Schultz, Lars Hinrichs"
REQUIRES_PYTHON = '>=3.0.0'
VERSION = '0.5.0'

# What packages are required for this module to be executed?
# FIXME is this needed
REQUIRED = [ 
 "astroid>=2.3.3",
 "attrs>=19.3.0",
 "et-xmlfile>=1.0.1",
 "importlib-metadata>=1.1.0",
 "isort>=4.3.21",
 "jdcal>=1.4.1",
 "lazy-object-proxy>=1.4.3",
 "mccabe>=0.6.1",
 "more-itertools>=8.0.0",
 "numpy>=1.16.4",
 "openpyxl>=2.6.2",
 "packaging>=19.2",
 "pandas>=0.24.2",
 "pluggy>=0.13.1",
 "py>=1.8.0",
 "pylint>=2.4.4",
 "pyparsing>=2.4.5",
 "pytest>=5.3.1",
 "python-dateutil>=2.8.0",
 "pytz>=2019.1",
 "six>=1.12.0",
 "typed-ast>=1.4.0",
 "virtualenv>=16.7.2",
 "wcwidth>=0.1.7",
 "wrapt>=1.11.2",
 "XlsxWriter>=1.1.8",

]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
#try:
#    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#        long_description = '\n' + f.read()
#except FileNotFoundError:
#    long_description = DESCRIPTION

long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    #long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)


