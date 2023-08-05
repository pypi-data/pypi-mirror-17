cd toalaska
python setup.py sdist
cp ~/.pypirc  ~/.pypirc.bak
cp ~/.pypirc.toalaska  ~/.pypirc
python setup.py register sdist upload
cp  ~/.pypirc.bak  ~/.pypirc
