#!/bin/bash

docker run -d \
		   --name my_selenium \
		   -p 4444:4444 \
		   -v /dev/shm:/dev/shm \
		   -v $PWD/script:/script \
		   tg_selenium

