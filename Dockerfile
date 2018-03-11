FROM python:3

WORKDIR /var/cs176/p2p
RUN mkdir -p files && touch hosts
COPY . /var/cs176/p2p

ENTRYPOINT ["python"]
