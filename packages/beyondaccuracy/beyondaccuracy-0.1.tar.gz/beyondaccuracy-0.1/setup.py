from setuptools import setup, find_packages

setup(
    name="beyondaccuracy",
    version="0.1",
    license="MIT",
    author="Johannes Kruse",
    author_email="johannes-kruse@hotmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/gabriben/metrecs",
    keywords="Recommender Systems",
    install_requires=[
        "numpy",
    ],
)
