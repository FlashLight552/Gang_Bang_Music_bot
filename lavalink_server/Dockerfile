FROM openjdk:17-jdk-alpine

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/lavalink-devs/Lavalink/releases/download/4.0.7/Lavalink.jar

# ENTRYPOINT ["java", "-jar", "Lavalink.jar"]

ENTRYPOINT ["java" "-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2" "-jar" "Lavalink.jar"]

