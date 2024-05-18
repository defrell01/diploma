python_images = f"""
            FROM python:3.8-slim
            WORKDIR /app
            COPY script.py /app/script.py
            CMD ["python", "/app/script.py"]
            """

golang_image = f"""
            FROM golang:latest
            WORKDIR /app
            COPY script.go /app/script.go
            CMD ["go", "run", "/app/script.go"]
            """
