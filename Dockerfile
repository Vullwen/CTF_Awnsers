FROM python:3.12-slim
WORKDIR /app
COPY ./* ./
RUN chmod +x ./init.sh

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
CMD ["./init.sh"]
