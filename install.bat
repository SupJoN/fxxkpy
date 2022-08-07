@echo off
pip uninstall fxxkpy -y
python setup.py sdist bdist_wheel
pip install dist\fxxkpy-2.0.0-py3-none-any.whl