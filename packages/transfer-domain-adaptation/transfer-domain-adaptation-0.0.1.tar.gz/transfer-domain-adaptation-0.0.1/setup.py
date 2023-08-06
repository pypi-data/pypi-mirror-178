from setuptools import setup

from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='transfer-domain-adaptation',
    version='0.0.1',
    license='MIT License',
    author='Pedro Henrique Conrado Ferreira de Oliveira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pedrohenriqueconrado@usp.br',
    keywords='transfer domain adaptation keras',
    description=u'ferramenta para adaptacao de dominio com transfer learning',
    packages=['domain_transfer'],
    install_requires=['tensorflow'],)