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

## Execution
```python
(venv) python3 main.py -i [input file name] -o [output file name]
```
- where [input file name] contains the text to rewrite
- and [output file name] is the file where the output will be written

## Datasets
- This model was used for creating parallel datasets containing binary-gendered and gender-neutral Portuguese sentences.
- Those datasets are hosted in the companion repository for this project: https://github.com/leonorv/pt-gn-datasets

