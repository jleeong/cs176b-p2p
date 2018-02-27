FROM python:3

WORKDIR /var/cs176/p2p
RUN mkdir -p files && touch hosts
COPY . /var/cs176/p2p

CMD ["python", "/var/cs176/p2p/runnode.py", "g", "daemon"]
