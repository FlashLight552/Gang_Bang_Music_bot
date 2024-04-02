FROM openjdk:17-jdk-alpine

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/ZeyoYT/Lavalink/releases/download/Fixed/Lavalink.jar

ENTRYPOINT ["java", "-jar", "Lavalink.jar"]
