# pt-gender-neutralizer
Module for gender neutralization of entities in portuguese

## Requirements

This project uses Python 3.8+

Create a virtual environment with:

```bash
git clone git@github.com:leonorv/pt-gender-neutralizer.git
python3 -m virtualenv venv
source venv/bin/activate
```

Install the requirements (inside the project folder):
```bash
(venv) pip3 install -r requirements.txt
```

Install the Portuguese lexicon required from the Multilingual Wordnet collection:
```bash
(venv) python3 -m wn download own-pt:1.0.0
```


## Execution
```python
(venv) python3 main.py -i [input file name] -o [output file name]
```
- where [input file name] contains the text to rewrite
- and [output file name] is the file where the output will be written

