# Use a specific Python version for reproducibility
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/home/user/.local/bin:$PATH" \
    U2NET_HOME="/app/models" \
    DEBIAN_FRONTEND=noninteractive

# Create a non-root user and set permissions
RUN useradd -m -u 1000 user && \
    mkdir -p /app && \
    chown -R user:user /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 libgl1 binutils \
    && rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER user
WORKDIR /app

# Copy worker-specific files from the hf-worker directory
COPY --chown=user:user hf-worker/requirements.txt ./
COPY --chown=user:user hf-worker/server.py ./
COPY --chown=user:user hf-worker/app ./app/

# Install Python dependencies for the user
RUN pip install --no-cache-dir --user -r requirements.txt

# CRITICAL: Strip ONNX runtime binaries to fix executable stack issue
RUN find /home/user/.local -name "*.so" -type f -exec strip --remove-section=.note.gnu.property {} + 2>/dev/null || true

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Command to run the application
CMD ["python", "server.py"]
