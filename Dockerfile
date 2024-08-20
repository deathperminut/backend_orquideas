# Usa una imagen base oficial de Python
FROM python:3.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Dockerfile


# Copia el archivo de credenciales al contenedor
COPY credenciales/orquideas-432422-e8f2f67257bb.json /app/credenciales/orquideas-432422-e8f2f67257bb.json

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación escuchará
EXPOSE 8080

# Establece el comando para iniciar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]