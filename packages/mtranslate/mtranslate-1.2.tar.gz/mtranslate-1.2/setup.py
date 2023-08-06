
from distutils.core import setup

setup(
    name = 'mtranslate',
    packages = ['mtranslate'],
    version = '1.2',
    description = 'Google translate console script with easy to use API',
    author = 'Arnaud Alies',
    author_email = 'arnaudalies.py@gmail.com',
    url = 'https://github.com/mouuff/Google-Translate-API',
    download_url = 'https://github.com/mouuff/Google-Translate-API/tarball/1.2',
    keywords = ['console', 'translate', 'translator', 'simple', 'google'],
    classifiers = [],
    entry_points={
          'console_scripts': [
              'mtranslate = mtranslate.__main__:main'
          ]
      },
)
