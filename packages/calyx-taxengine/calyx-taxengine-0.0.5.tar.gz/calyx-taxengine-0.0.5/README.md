# Tax Engine Shared module

## crear entorno virtual
```bash
python -m venv venv
```

## activar entorno virtual
```bash
.\venv\Scripts\activate
```

## instalar dependencias
```bash
pip install -r requirements.txt
```

## aumentar el nro de versión
### en el archivo setup.py

## crear package
```bash
python .\setup.py sdist bdist_wheel
```

## subir a pypi
```bash
twine upload dist/*
```
