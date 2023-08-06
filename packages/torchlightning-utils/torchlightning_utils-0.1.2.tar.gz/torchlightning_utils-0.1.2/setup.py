from setuptools import setup, find_packages

setup(
    name="torchlightning_utils",
    version="0.1.2",
    author_email="shuhang0chen@gmail.com",
    maintainer_email="shuhang0chen@gmail.com",
    packages=find_packages(),
    install_requires=["pytorch-lightning", "omegaconf"],
)
