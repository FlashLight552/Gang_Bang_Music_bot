FROM openjdk:17-jdk-alpine

WORKDIR /usr/src/lavalink_server

COPY . .

RUN apk upgrade --no-cache && \
    apk add --no-cache postgresql-client bash openssl libgcc libstdc++ ncurses-libs
RUN wget https://github.com/lavalink-devs/Lavalink/releases/download/4.0.7/Lavalink.jar

ENTRYPOINT ["java", "-jar", "Lavalink.jar"]


