# Experquiz BI

Business Intelligence Proof Of Concept for Experquiz.

### Preparation

#### Gcloud
Create account ... 

This is meant to work on Python , but I need to check for Python 2 (@Pap)

#### Virtual env
In a terminal : 
```console
python3 -m venv xq-bi-venv
source xq-bi-venv/bin/activate
pip install -r requirements 
```

### Usage 
#### 1. GCloud authentification
```console
gcloud auth login your@email.com
gcloud auth application-default login
```
#### 2. Activate venv and launch app 
```console
source xq-bi-venv/bin/activate
python app.py
```
Then visit http://127.0.0.1:5000/experquiz 
