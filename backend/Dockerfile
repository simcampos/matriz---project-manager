FROM python:3.15.1-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && addgroup --system app \
    && adduser --system --ingroup app --no-create-home app

COPY --chown=app:app . /app/

USER app
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
