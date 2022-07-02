1. build using `docker build .`
2. run using `docker run --net=host <build number>`

notice net=host is used so that host machine can make call to docker container. I don't fully understand this though