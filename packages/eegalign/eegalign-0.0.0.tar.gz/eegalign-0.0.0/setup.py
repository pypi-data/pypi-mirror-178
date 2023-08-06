from setuptools import setup, find_packages
import codecs
import os



DESCRIPTION = 'Data formater'
LONG_DESCRIPTION = 'A package that allows '

# Setting up
setup(
    name="eegalign",
    author="Rohit Kumar Mishra",
    author_email="<rohitm487@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="EEG data and marker stiching, interpolation and clipping",
    packages=find_packages(),
    install_requires=['mne', 'pandas', 'numpy','scipy'],
    keywords=['python', 'stream', 'preprocessing', 'eeg', 'data processing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
