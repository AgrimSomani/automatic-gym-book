ARG PYTHON_VERSION=3.11.0

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY ./requirements.txt ./requirements.txt


RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ENV SOLVER_KEY=aced54bd168c720622d17081f2379317

COPY . .

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


