FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /machine
ADD . /machine
RUN pip install -e .
ENTRYPOINT [ "python", "-m", "dummy_machines" ]
CMD [ "-h" ]
# docker run --rm --network="host" michbud98/dummy-machines -s 5 -url http://localhost:8000 Thermometer 1