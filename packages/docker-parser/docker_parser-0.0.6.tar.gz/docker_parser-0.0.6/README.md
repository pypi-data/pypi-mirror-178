# Docker parser

Docker attempts to simplify machine processing of dockerfiles. This moduel is not intended to extend docker SDK or build images, instead it attempts to parse instructions into simply manipulatable python objects, deduce state of environment in which commands are executed and allow modification of resulting dockerfile.

# Instalation

```
pip3 install docker-parser
```


# Usage


Print all executed RUN commands
```python
from docker_parser import parser

with open("dockerfile") as src:
    dockerfile = parser.Parser.loads(src.read())

for cmd in dockerfile.run():
    print(cmd.arg)
```

dockerfile:
```
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y gcc make
COPY ./src /var/tmp/
WORKDIR /var/tmp/src
RUN make
```

output:
```
apt update
apt install -y gcc make
make
```

for more examples refer to [examples](examples/)


# Contributing

To contribute:
1. Increment version in [pyproject.toml](pyproject.toml)
2. Create merge request to `preprod` branch
3. Once your changes are reviewed and merged, pipeline publishes new version to testpypi
4. After verifying that changes don't break rest of the code and don't justify major release, changes will be pushed to `main` branch and pushed to production pypi 