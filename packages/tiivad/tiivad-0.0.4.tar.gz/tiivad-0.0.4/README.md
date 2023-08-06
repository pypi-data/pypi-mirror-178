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
```
python setup.py sdist
```

python -m twine upload dist/* 


https://pypi.org/project/tiivad/



# Anname talle -t käsuga uue nime.
docker build --no-cache -f tiivad-base -t emuuli/local .

# Buildime teise image koos accessment koodiga:
docker build --no-cache -f dockerfile-evaluate .

docker run -it 6da0f2c92b5c /bin/bash
docker logs container_ID