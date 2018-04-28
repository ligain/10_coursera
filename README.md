  
# Coursera Dump
This tool fetches info from Coursera
[feed](https://www.coursera.org/sitemap~www~courses.xml) and saves result in `xlsx`  file.
It takes such course properties: `Url`, `Title`, `Languages`, `Start date`,  
  `Weeks`, `Average user's rating`
# Installation
**Python 3 should be already installed.**

0) Get source code
```bash
$ git clone https://github.com/ligain/10_coursera.git
```

1) Create virtual environment in the directory where you want to place project.
```bash
$ cd 10_coursera/
python3 -m venv .env
```

2) Activate virtual environment
```bash
$ . .env/bin/activate
```

3) Install all dependencies via pip
```bash  
pip install -r requirements.txt # alternatively try pip3  
```  
# Usage
You could start the script without params:
```bash
$ python3 coursera.py
```
In this case outcome will be save in the directory where the script is and a name of `xlsx`  file will be `courses.xlsx`

If you want to specify directory and filename of outcome, just run like so:
```bash
$ python3 coursera.py -p path/where/to/save -f filename.xlsx
```
  
# Project Goals  
  
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)