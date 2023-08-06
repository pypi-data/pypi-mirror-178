export PATH := "./.venv/bin:" + env_var('PATH')

help:
    @just --list --unsorted

example ARG:
    go run {{ARG}}

run:
    go run main.go

bootstrap:
    pdm install

check:
    pyright

test:
    echo No unit tests yet

test-full: bootstrap check test
    #!/usr/bin/env bash -euxo pipefail
    for file in $(ls examples); do
        python3 "examples/$file"
    done

publish:
   FLIT_USERNAME="__token__" \
   FLIT_PASSWORD=$PYPI_API_TOKEN \
   flit publish

doc:
    # mkdir -p docs/
    # fd -e rst . docs/ -x rm
    # pandoc README.md -o docs/index.rst
    # sphinx-apidoc -o docs plaid2/ -e
    sphinx-build docs _build

open:
    open http://localhost:8000
    python3 -m http.server --directory _build

version level:
    VERSION=$(toml get -r pyproject.toml project.version) && \
        git commit -am "Bump version {{level}} to $VERSION" --allow-empty && \
        git tag v$VERSION && \
        git push origin v$VERSION
    git push

shell:
    pdm run ipython3 -i -c "from plaid2 import *"