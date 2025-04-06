FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
COPY uv.lock ./
RUN pip install --no-cache-dir gunicorn psycopg2-binary flask flask-sqlalchemy flask-cors email-validator

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV HOST=0.0.0.0
ENV PORT=5000

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reuse-port", "--reload", "main:app"]