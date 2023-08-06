from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Processador-de-Imagens",
    version="0.0.1",
    author="Leonardo Santana",
    author_email="leonardoalvs12@gmail.com",
    description="Pacote de processamento de imagem usando Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leoalvessantana/BootCamp-Dio-Geracao-Tech-Unimed-BH-ciencia-de-dados/tree/main/1.Python%20para%20Cientista%20de%20Dados",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
