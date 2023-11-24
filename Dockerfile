FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY . .

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 5000

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "5000", "midas_sales.main:app" ]

# TODO: Criar um Dockerignore para evitar vazar pasta git e arquivos de configuração