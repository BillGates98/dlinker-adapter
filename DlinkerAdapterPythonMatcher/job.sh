mvn clean package

mvn clean compile assembly:single

mv ./target/dlinker-adapter-1.0-jar-with-dependencies.jar ./target/dlinker-adapter-1.0.jar

mvn install:install-file \
  -Dfile=./target/dlinker-adapter-1.0.jar \
  -DgroupId=org.ird \
  -DartifactId=dlinker-adapter \
  -Dversion=1.0.0 \
  -Dpackaging=jar \
  -DlocalRepositoryPath=repository

docker build -t git.project-hobbit.eu:4567/billhappi/dlinker-tool .

# docker push git.project-hobbit.eu:4567/billhappi/dlinker-tool

