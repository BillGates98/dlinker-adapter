# FROM openjdk:8-jre-alpine python:3.8.10-alpine3.12

FROM openjdk:8-jdk-alpine3.9

COPY --from=python:3.8.10-alpine3.12 / /

RUN python -m pip install --upgrade pip
RUN pip install rdflib
RUN pip install validators
RUN pip install xlwt
RUN pip install pybase64
RUN pip install argparse
RUN apk update
RUN apk upgrade
RUN apk add --no-cache --virtual=build_deps g++ gfortran
RUN pip install --no-cache-dir spacy
RUN python -m spacy download en_core_web_md
RUN pip install pandas
RUN apk del build_deps
RUN apk add openjdk8-jre-lib
RUN apk add openjdk8-jre

RUN mkdir /system

ADD target/dlinker-adapter-1.0.jar /system/dlinker-adapter-1.0.jar

RUN mkdir -p /system/oaei-resources/
ADD oaei-resources/ /system/oaei-resources/

WORKDIR /system

RUN mkdir -p /system/datasets/SourceDatasets/
RUN mkdir /system/datasets/TargetDatasets/

CMD java -cp dlinker-adapter-1.0.jar org.hobbit.core.run.ComponentStarter org.ird.DLinkerAdapter

