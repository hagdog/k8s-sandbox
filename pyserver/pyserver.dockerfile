FROM python:3

# Set up the simple server.
RUN mkdir /pyserver
COPY src/ /pyserver
ENV PYTHONPATH /pyserver

# Start the simple server on startup.
ENTRYPOINT ["python", "-m", "pyserver.pyserver"]