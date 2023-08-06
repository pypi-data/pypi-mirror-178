from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'PY LAB'


# Setting up
setup(
    name="ditekmax",
    version=VERSION,
    author="DITEK",
    author_email="<maks.ditkovskiy.05@mail.ru>",
    description=DESCRIPTION,
  
    packages=['ditekmax'],
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)