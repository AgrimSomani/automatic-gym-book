FROM python:3.11.4-slim-buster

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Use the environment variable within the container
ENV SOLVER_KEY=${BUILD_TIME_VAR}

COPY . .

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

