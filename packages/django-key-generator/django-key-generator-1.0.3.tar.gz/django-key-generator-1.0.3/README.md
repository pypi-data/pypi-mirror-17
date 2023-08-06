# django-key-generator

Django management command to generate a new secret key

## Installation

```bash
pip install django-key-generator
```

Add `keygenerator` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
	...,
	'keygenerator',
]
```

## Usage

```bash
python manage.py generatekey
```