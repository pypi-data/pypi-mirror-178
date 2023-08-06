# Welcome to the DAS Python package

The [Royal Netherlands Institute for Sea Research](https://www.nioz.nl) has its data management system to help scientists archive and access their data. This tool is called: **Data Archive System (DAS)** and this package is its Python client.

To install this package use the following command:

```powershell
    $ pip install daspython
```

The best way to see how each method is used is visiting out [automated test scripts](https://git.nioz.nl/ict-projects/das-python/-/tree/master/tests) page.

# Authentication

Use this class to authenticate and keep your token that will be needed to use with all other service classes.

##### Usage

```python
from daspython.auth.authenticate import DasAuth

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    
```