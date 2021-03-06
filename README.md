# Chess tournament manager

This program is a chess tournament manager, used to create new tournaments, create new players, automaticaly generate
pairs, saves closed and ongoing tournaments and displays rapports

## Download

Download https://github.com/alyxben/RazPrjct4 to the repository of your choice

## Installation

Make sure you already have python3 install on your computer. If not, please go to this
link: https://www.python.org/downloads/ and follow the instructions. Open your Cmd and proceed as indicated:
Go to your repository:

```bash
cd your\repo
```

Create a virtual environment:

```bash
python3 -m venv env
```

Activate it:

for windows

```bash
env\Scripts\activate
```

for mac/linux

```bash
source env/bin/activate
```

Install depedencies:

```bash
pip install -r requirements.txt
```

Run the programm:

```bash
python3 main.py
```

Follow the instruction on screen

## Flake8 Repport

To generate a flake8 repport

```bash
flake8 --format=html --htmldir=flake-report --exclude=venv --max-line-length 119
```
