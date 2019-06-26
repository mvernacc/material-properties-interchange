#!/bin/sh

rm -rf ./docs/build

sphinx-apidoc ./materials/ -o ./docs/source/apidoc/ --implicit-namespaces -fMeT

cd docs

make html

cd ..
