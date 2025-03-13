FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update

RUN apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    python3 \
    python3-pip \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    libsdl2-mixer-dev \
    libsdl2-gfx-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libjpeg-dev \
    libfreetype6-dev \
    pkg-config \
    libboost-all-dev \
    libboost-python-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

# Instalar módulos esenciales antes de gfootball
RUN pip install psutil==6.1.1 absl-py==2.1.0

# Instalación completa
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
