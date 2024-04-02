FROM openjdk:23-slim

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/ZeyoYT/Lavalink/releases/download/Fixed/Lavalink.jar

# RUN mv /usr/src/lavalink_server

# RUN javac Lavalink.jar

CMD ["java", "-jar" "Lavalink.jar"]

# ENTRYPOINT ["java" "-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2" "-Xmx4G" "-jar" "Lavalink.jar"]