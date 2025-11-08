FROM python:3.11-slim

# Crear usuario no-root
RUN useradd -m -u 1000 user

# Instalar dependencias del sistema (CON binutils para strip)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# Cambiar a usuario no-root
USER user

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY --chown=user:user requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --user -r requirements.txt

# CRÍTICO: Limpiar binarios de ONNX Runtime con strip
# Esto remueve la sección .note.gnu.property que causa el problema de executable stack
RUN find /home/user/.local -name "*.so" -type f -exec strip --remove-section=.note.gnu.property {} + 2>/dev/null || true

# Copiar código de la aplicación
COPY --chown=user:user . /app

# Exponer puerto requerido por HF Spaces
EXPOSE 7860

# Variables de entorno
ENV PATH="/home/user/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV U2NET_HOME=/tmp/.u2net

# Comando de inicio
CMD ["python", "server.py"]