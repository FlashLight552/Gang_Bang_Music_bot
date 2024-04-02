FROM openjdk:23-slim-bullseye

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/ZeyoYT/Lavalink/releases/download/Fixed/Lavalink.jar

# RUN mv /usr/src/lavalink_server

ENTRYPOINT ["java" "-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2" "-Xmx4G" "-jar" "Lavalink.jar"]