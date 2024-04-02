FROM azul/zulu-openjdk-alpine:17-jre-headless-latest


# RUN /bin/sh -c apk add --no-cache libgcc # buildkit

# RUN /bin/sh -c addgroup -g 322 -S lavalink && adduser -u 322 -S lavalink lavalink # buildkit

# RUN /bin/sh -c chown -R lavalink:lavalink /opt/Lavalink # buildkit

# USER lavalink

WORKDIR /usr/src/lavalink_server

COPY . .

RUN wget https://github.com/ZeyoYT/Lavalink/releases/download/Fixed/Lavalink.jar

# RUN mv /usr/src/lavalink_server

# RUN javac Lavalink.jar

CMD ["java" "-jar", "Lavalink.jar"]

# ENTRYPOINT ["java" "-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2" "-Xmx4G" "-jar" "Lavalink.jar"]