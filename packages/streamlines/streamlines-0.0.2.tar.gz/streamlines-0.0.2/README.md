[![Build Status](https://travis-ci.org/jbn/streamlines.svg?branch=master)](https://travis-ci.org/jbn/streamlines)
[![Coverage Status](https://coveralls.io/repos/github/jbn/streamlines/badge.svg?branch=master)](https://coveralls.io/github/jbn/streamlines?branch=master)

# `streamlines`

Tools for working with files as line streams.

## Installation

```sh
pip install streamlines
```

## Usage

Right now, mostly...

```python
from streamlines import *

# Infer compression type from file extension, automagically. 
for line in source("your_file.txt.bz2"): 
    print(line)
```

