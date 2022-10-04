# FROM openjdk:8-jre-alpine python:3.8.10-alpine3.12
# 1
# FROM openjdk:8-jre-alpine
# COPY --from=python:3.9.10-alpine / /

# 2 : rappdw/docker-java-python:openjdk1.8.0_171-python3.6.6
FROM rappdw/docker-java-python:latest 
RUN java -version && python --version

# 3 
# FROM python:3.9-slim
# COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
# ENV JAVA_HOME /usr/local/openjdk-8
# RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r requirements.txt
# RUN apk update
# RUN apk upgrade
# RUN apk add --no-cache --virtual=build_deps g++ gfortran
# RUN pip install --no-cache-dir spacy
# RUN python -m spacy download en_core_web_md
# RUN pip install pandas
# RUN apk del build_deps
# RUN apk add openjdk8-jre-lib
# RUN apk add openjdk8-jre

# RUN mkdir /system
WORKDIR /system
ADD target/dlinker-adapter-1.0.jar /system/dlinker-adapter-1.0.jar
RUN mkdir -p /system/oaei-resources/ \ 
mkdir -p /system/datasets/SourceDatasets/ \
mkdir -p /system/datasets/TargetDatasets/

ADD oaei-resources/ /system/oaei-resources/

# RUN python /system/oaei-resources/pythonMatcher.py
# CMD java -cp dlinker-adapter-1.0.jar org.hobbit.core.run.ComponentStarter org.ird.DLinkerAdapter

ENTRYPOINT [ "java", "-cp", "dlinker-adapter-1.0.jar", "org.hobbit.core.run.ComponentStarter", "org.ird.DLinkerAdapter" ]
