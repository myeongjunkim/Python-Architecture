FROM python:3.10-slim as base
ENV PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    WORKDIR=/code 
ENV PATH="$POETRY_HOME/bin:$PATH" 
WORKDIR $WORKDIR

FROM base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential
ENV POETRY_VERSION=1.2.1
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --without dev 

FROM base as prod
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./app ./app
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --no-access-log


