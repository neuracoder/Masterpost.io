FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -u 1000 user

# Install system dependencies (including binutils for strip)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY --chown=user ./requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# CRITICAL: Strip the ONNX runtime binaries to remove the executable stack requirement
RUN find /home/user/.local -name "*.so" -type f -exec strip --remove-section=.note.gnu.property {} + 2>/dev/null || true

# Copy the application code
COPY --chown=user . /app

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]