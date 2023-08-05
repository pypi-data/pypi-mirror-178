from setuptools import setup, find_packages
import codecs
import os
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0.6.8'

DESCRIPTION = 'Highlander project'
LONG_DESCRIPTION = 'Highlander project for hig data usage'



# Setting up
setup(
    name="HighlanderML",
    version=VERSION,
    author="Pixpit (Giovanni Vignali)",
    author_email="<giovanni.vignali@outlook.it>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,


    packages=find_packages(include=['highlander_script','highlander_script.*']),
    #install_requires=['multiprocessing>=2.6.2.1', 'pandas>=1.3.4', 'numpy>=1.21.2', 'scikit-learn>=1.0'],
    install_requires=['pandas>=1.3.4', 'numpy>=1.21.2', 'scikit-learn>=1.0', ],
  
    keywords=['python', 'machine learning', 'Weather forecasting', 'Milk', 'Climat change'],
    
    classifiers=["Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"]
)

# Reference: 
# https://github.com/NeuralNine/vidstream
# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
