@echo off
pip install wheel
pip uninstall fxxkpy -y
python setup.py sdist bdist_wheel --universal
pip install dist\fxxkpy-2.4.0-py2.py3-none-any.whl