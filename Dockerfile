FROM python:3.8 as base

WORKDIR /home/hwc_model

COPY requirements.txt requirements.txt

RUN pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base as production

WORKDIR /production

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apt update && chmod +x ./scripts/start.sh

ARG PORT=80
ARG HOST=0.0.0.0
ARG APP_MODULE=app.MHWC_app:app
ARG WORKERS_PER_CORE=2

ENV MODE=production
ENV CFG_KEY=AKIAYYSCAMR6MYPLQSE3
ENV CFG_SECRET=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
ENV APP_ACRONYM=MHWC
ENV APP_MODULE=${APP_MODULE}
ENV WORKERS_PER_CORE=${WORKERS_PER_CORE}
ENV HOST=${HOST}
ENV PORT=${PORT}

EXPOSE ${PORT}

# CMD ["uvicorn", "app.MLRD_app:app", "--host", "0.0.0.0", "--port", "80"]
ENTRYPOINT [ "./scripts/start.sh" ]

