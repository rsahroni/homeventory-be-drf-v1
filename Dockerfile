# Gunakan base image Python resmi
FROM python:3.11-slim-bookworm

# Set environment variables untuk mencegah Python membuat file .pyc
# dan agar output dari Python langsung tampil di terminal (unbuffered).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# Set direktori kerja di dalam container
WORKDIR /app

# Install dependensi sistem yang mungkin dibutuhkan
RUN apt-get update && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config default-mysql-client && rm -rf /var/lib/apt/lists/*

# Salin file requirements dan install dependensi Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode proyek ke dalam direktori kerja
COPY . /app

# Salin entrypoint script dan berikan izin eksekusi
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Buat user non-root untuk keamanan
RUN addgroup --system app && adduser --system --group app

# Ganti kepemilikan direktori aplikasi ke user baru
RUN chown -R app:app /app

# Ganti ke user non-root
USER app

# Expose port 8000 agar bisa diakses dari luar container
EXPOSE 8000

# Jalankan entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Perintah default untuk image. Akan ditimpa oleh 'command' di docker-compose.
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]