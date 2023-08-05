from setuptools import setup
setup(name="ASRscsvmv",
version="1.1.3",
description="This package recognizes and translates your words",
long_description="""
INSTALL THIS PACKAGE USING 
pip install ASRscsvmv
""",
author="SCSVMV 22-23 PROJECT 17",
packages=['ASRscsvmv'],
install_requires=['vosk','PySimpleGUI','argostranslate','streamlit','pyaudio'])