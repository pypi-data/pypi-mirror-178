from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cpfValidationTool",
    version="0.0.2",
    author="Rodrigo Freitas",
    author_email="digofmf@gmail.com",
    description="Código que valida o CPF através da validação dos últimos dois dígitos",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodrigofmfreitas/dio-cursos/tree/main/Geracao-Tech-Unimed/Desafio2",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)