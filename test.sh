#!/bin/bash
for py_file in $(find . -name '*_test.py')
do
	python $py_file
done