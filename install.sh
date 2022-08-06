python setup.py sdist bdist_wheel
pip uninstall fxxkpy -y
sleep 3
pip install dist/fxxkpy-1.0.0-py3-none-any.whl