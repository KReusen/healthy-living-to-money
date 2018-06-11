FROM lambci/lambda:build-python3.6


ADD Makefile .
ADD requirements.txt .
RUN make clean build

ADD src ./src

ADD cloudformation ./cloudformation