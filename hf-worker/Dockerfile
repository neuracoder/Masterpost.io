# Hugging Face Spaces Dockerfile
# Python 3.11 slim base
FROM python:3.11-slim

# Environment variables for HF Spaces
ENV PORT=7860
ENV PYTHONUNBUFFERED=1
ENV HOME=/tmp

# Install system dependencies (as root before creating user)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (HF Spaces requirement)
RUN useradd -m -u 1000 user

# Switch to non-root user
USER user

# Set working directory
WORKDIR /app

# Copy requirements
COPY --chown=user:user backend/requirements.txt .

# Install Python packages in user space
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy entire backend
COPY --chown=user:user ./backend /app

# Configure model cache in /tmp (only writable directory on HF Spaces)
ENV U2NET_HOME=/tmp/.u2net
ENV TORCH_HOME=/tmp/.torch

# Expose port 7860 (HF Spaces requirement)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:7860/health')" || exit 1

# Start server
CMD ["python", "server.py"]
