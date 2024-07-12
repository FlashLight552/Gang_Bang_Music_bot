FROM openjdk:17-jdk-alpine

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/lavalink-devs/Lavalink/releases/download/4.0.5/Lavalink.jar

ENTRYPOINT ["java", "-jar", "Lavalink.jar"]

