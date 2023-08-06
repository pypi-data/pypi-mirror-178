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

# Packaging:
```
python setup.py sdist
```

https://pypi.org/project/tiivad/



# Anname talle -t käsuga uue nime.
docker build -f tiivad-base -t emuuli/local .

# Buildime teise image koos accessment koodiga:
docker build -f dockerfile-evaluate .

docker run -it 64b3d5614f48 /bin/bash
docker logs container_ID