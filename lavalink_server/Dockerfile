FROM openjdk:17-jdk-alpine

WORKDIR /usr/src/lavalink_server

COPY . .

# RUN wget https://github.com/ZeyoYT/Lavalink/releases/download/Fixed/Lavalink.jar
# RUN wget https://repo.lavalink.dev/artifacts/lavalink/96e65bfe/Lavalink.jar
RUN wget https://github.com/lavalink-devs/Lavalink/releases/download/4.0.5/Lavalink.jar

ENTRYPOINT ["java", "-jar", "Lavalink.jar"]

