FROM python:3.15.1-slim-bookworm AS runtime

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

FROM runtime AS development

ENV DJANGO_DEBUG=true

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM runtime AS production

ENV DJANGO_DEBUG=false

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]
