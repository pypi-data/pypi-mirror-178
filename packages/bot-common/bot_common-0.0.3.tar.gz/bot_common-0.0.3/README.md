# COMMON AISAC BOT LIBRARIES

DEPLOY:

conda install twine==4.0.1 --y
python setup.py sdist bdist_wheel
twine upload --skip-existing dist/* --username=cla.fragomeli_92 --password=Monocolo@888
