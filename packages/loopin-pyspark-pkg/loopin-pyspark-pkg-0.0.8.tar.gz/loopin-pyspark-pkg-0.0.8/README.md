##before upload
 python -m pip install --upgrade build


python -m pip install --upgrade twine



## Build
docker build -t pyspark-docker .

## Stop
docker stop $(docker ps -a -q)   


## bash
docker exec -it  9028a97a8889 /bin/bash

