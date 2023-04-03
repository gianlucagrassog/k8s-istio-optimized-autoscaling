FROM python:3.11.1-slim@sha256:f5bb52ea4db7c29a8f4253efaeae6ba2e69e435c1509368d4a774076b82e8f86 as base

FROM base as builder

COPY requirements.txt .

RUN pip install --prefix="/install" -r requirements.txt

FROM base

WORKDIR /loadgen

COPY --from=builder /install /usr/local

# Add application code.
COPY locustfile.py .

# enable gevent support in debugger
ENV GEVENT_SUPPORT=True

ENTRYPOINT locust --host="http://${FRONTEND_ADDR}" -u "${USERS:-10}" -r "${RATE}" 2>&1
