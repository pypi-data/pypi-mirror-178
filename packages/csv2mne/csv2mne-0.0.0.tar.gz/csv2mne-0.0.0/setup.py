from setuptools import setup, find_packages




DESCRIPTION = 'Data formater'
LONG_DESCRIPTION = 'A package that allows '

# Setting up
setup(
    name="csv2mne",
    version="0.0.0",
    author="Rohit Kumar Mishra",
    author_email="<rohitm487@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="EEG data and marker stiching\n, interpolation and clipping\n, export in raw mne array\n,export Epoched data",
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
