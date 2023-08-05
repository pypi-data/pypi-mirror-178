## `kfutils`: A tool for common data file operations.
[![Alt text](https://img.shields.io/pypi/v/kfutils.svg?logo=pypi)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/pyversions/kfutils.svg?logo=python)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/dm/kfutils.svg?)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/l/kfutils.svg?)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/status/kfutils.svg?)](https://pypi.org/project/kfutils/)


### ⚒ Instalation
Download and install the latest package from the [release section](https://github.com/Koushikphy/kfutils/releases/latest) or directly by pip
```bash
pip install kfutils
```
This installs the python module and a command line tool named `kfutils`.  



### ⚡ Usage 

 __✈ Using as a command line tool.__
```bash
kutils [-h] -i FILE [-o FILE] [-c COLS [COLS ...]] [-rd COLS [COLS ...]] [-dr COLS [COLS ...]] [-dc COLS [COLS ...]] [-int N [N ...]] [-mir N] [-rep N]
```

| Argument    |  Description|
| ----------- | ----------- 
|    `-i`     | Input file name <br>If no operations are given it will show the stats about the file. |
|    `-o`     | OOutput file name. (default: '_out' prefix to input file name) | 
|    `-c`     | Index(s) of grid columns. 2 columns for 2D file. | 
|    `-rd`    | Index(s) of columns to convert to degree from radian |
|    `-dr`    | Index(s) of columns to convert to radian from degree |
|    `-dc`    | Index(s) of columns to delete |
|    `-int`   | Number of grid to interpolate to. Can be 1D or 2D |  
|    `-mir`   | Number of times to mirror |  
|    `-rep`   | Number of times to repeat |  



 __🚀 Using as a python module__  
The toplevel python module `kfutils` exposes several functions/class.
