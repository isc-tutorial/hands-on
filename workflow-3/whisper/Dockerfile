FROM python:3.11-slim

# Install system dependencies (git, build tools, libs, utilities)
RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    cmake \
    libcurl4-openssl-dev \
    libsdl2-dev \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Clone whisper.cpp repo
RUN git clone https://github.com/ggml-org/whisper.cpp.git

WORKDIR whisper.cpp

# Build whisper-stream binary
RUN cmake -B build -DWHISPER_SDL2=ON
RUN cmake --build build --config Release

# Copy the binary to /usr/local/bin
RUN cp build/bin/whisper-stream /usr/local/bin

# Download the model
RUN apt update && apt install -y --no-install-recommends wget
WORKDIR /models
RUN wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin -O /models/ggml-base.bin

WORKDIR /

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy your Python script
COPY publish.py /app/publish.py

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]
CMD ["/app/publish.py"]
