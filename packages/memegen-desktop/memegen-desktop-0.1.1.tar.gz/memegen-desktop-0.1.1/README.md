Unix: [![Unix Build Status](http://img.shields.io/travis/jacebrowning/memegen-desktop/master.svg)](https://travis-ci.org/jacebrowning/memegen-desktop) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/memegen-desktop/master.svg)](https://ci.appveyor.com/project/jacebrowning/memegen-desktop)<br>Metrics: [![Coverage Status](http://img.shields.io/coveralls/jacebrowning/memegen-desktop/master.svg)](https://coveralls.io/r/jacebrowning/memegen-desktop) [![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/memegen-desktop.svg)](https://scrutinizer-ci.com/g/jacebrowning/memegen-desktop/?branch=master)<br>Usage: [![PyPI Version](http://img.shields.io/pypi/v/memegen-desktop.svg)](https://pypi.python.org/pypi/memegen-desktop) [![PyPI Downloads](http://img.shields.io/pypi/dm/memegen-desktop.svg)](https://pypi.python.org/pypi/memegen-desktop)

# Overview

Desktop client for https://memegen.link.

# Setup

## Requirements

* Python 3.3+
* SpeechRecognition requirements: https://github.com/Uberi/speech_recognition#requirements
  * macOS: `$ brew install flac portaudio swig`

## Installation

Install the client with pip:

```sh
$ pip install memegen-desktop
```

or directly from the source code:

```sh
$ git clone https://github.com/jacebrowning/memegen-desktop.git
$ cd memegen-desktop
$ python setup.py install
```

# Usage

Launch the GUI from the command-line:

```sh
$ memegen
```
