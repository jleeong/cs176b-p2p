FROM python:3

WORKDIR /var/cs176/p2p
RUN mkdir -p files && touch hosts
COPY . /usr/src/app

CMD ["python", "/usr/src/app/runnode.py", "g"]
