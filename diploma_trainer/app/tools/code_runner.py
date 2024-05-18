import os
import docker
from tempfile import gettempdir
from .base_images import python_images, golang_image

class CodeRunner():
    def __init__(self, language, code):
        super().__init__()
        self.language = language
        self.code = code

        match language:
            case "golang":
                self.dockerfile_content = golang_image
                self.file = "script.go"
            case "python":
                self.dockerfile_content = python_images
                self.file = "script.py"

    def run_container(self):
        client = docker.from_env()

        try:
            # Создаем временный файл Dockerfile и записываем в него содержимое
            dockerfile_path = os.path.join(gettempdir(), "Dockerfile")
            with open(dockerfile_path, "w") as dockerfile:
                dockerfile.write(self.dockerfile_content)
                
            script_path = os.path.join(gettempdir(), self.file)
            with open(script_path, "w") as script:
                script.write(self.code)
            
            print("Building Docker image...")
            image, build_logs = client.images.build(path=gettempdir(), tag="myimage", dockerfile=dockerfile_path)
            
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(chunk['stream'].strip())

            print("Running Docker container...")
            container = client.containers.run("myimage", detach=True)

            container.wait()

            result = container.logs().decode('utf-8')

            container.stop()
            container.remove()

            client.images.remove("myimage", force=True)

            return result

        except Exception as e:
            print("Error:", e)
