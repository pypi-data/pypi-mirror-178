# Setup
* Use Python 3.10
* Install requirements from requirements.txt

# Run validation
```

```

# Running tests:
```
# All tests
python -m pytest
# For one file
python -m pytest test/test_file.py
```

# Packaging - change the version in setup.py and run:
## Enne mõistlik vana versioon dist kaustast ära kustutada
```
python setup.py sdist
```

# Laeme uue versiooni üles:
python -m twine upload dist/* 

# PyPi repo asukoht:
https://pypi.org/project/tiivad/



# Anname talle -t käsuga uue nime.
cd docker
docker build --no-cache -f tiivad-base -t emuuli/local .

# Buildime teise image koos accessment koodiga:
cd docker
docker build --no-cache -f dockerfile-evaluate .

docker run -it 64813273b626 /bin/bash
docker logs container_ID