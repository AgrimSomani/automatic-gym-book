FROM python:3.11.4-slim-buster

WORKDIR /app

COPY ./requirements.txt ./requirements.txt


RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ENV SOLVER_KEY 

COPY . .

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

