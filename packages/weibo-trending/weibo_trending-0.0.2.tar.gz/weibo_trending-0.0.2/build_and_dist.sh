#!/usr/bin/env bash
source venv/bin/activate
rm -r dist
python -m build
python -m twine upload --repository pypi dist/*