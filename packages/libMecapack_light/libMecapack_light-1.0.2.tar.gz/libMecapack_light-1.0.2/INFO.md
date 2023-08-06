# Pulbier une nouvelle version sur Pypi

- Mettre à jour la version dans le fichier `src\libMecapack\__init__.py`

- Pour la version complete : `flit publish --pypirc .\.pypirc`
- Pour la version light :`flit publish --pypirc .\.pypirc -f pyproject_light.toml`