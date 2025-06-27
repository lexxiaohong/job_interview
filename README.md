## install libraries
for development, run the following command to install the required libraries:
```
pipenv install --dev
```

for production, run the following command to install the required libraries:
```
pipenv install
```

## access virtualenv
```
pipenv shell
```

## run API server
```
uvicorn src.main:app --reload
```

## run test
```
python -m pytest
python -m pytest tests/ -vv -s
```

## Swagger UI
You can access the Swagger UI at `http://localhost:8000/docs` after starting the API server.
