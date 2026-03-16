pycall() {
    python3.14 -m "$@"
}

cd .
pycall pip install .
pycall pytest -s