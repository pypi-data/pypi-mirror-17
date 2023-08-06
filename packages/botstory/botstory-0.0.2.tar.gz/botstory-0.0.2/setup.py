import os

from setuptools import setup, find_packages

longDesc = ""
if os.path.exists("README.md"):
    longDesc = open("README.md").read().strip()

setup(
    name='botstory',
    packages=find_packages(),
    version='0.0.2',
    description='Async framework for bot',
    license='MIT',
    long_description=longDesc,
    author='Eugene Krevenets',
    author_email='ievegenii.krevenets@gmail.com',
    url='https://github.com/hyzhak/bot-story',
    download_url='https://github.com/hyzhak/bot-story/tarball/0.0.1',
    keywords=['bot', 'ai', 'nlp', 'asyncio'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        # TODO: Should find right topic
        # 'Topic :: Software Development :: Bots',

        # Not later because of async/await
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
