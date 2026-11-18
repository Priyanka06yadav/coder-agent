FROM python:3.12-slim

WORKDIR / app

RUN useradd --create-home --shell /usr/sbin/nologin coder

USER coder

CMD ["python", "--version"]