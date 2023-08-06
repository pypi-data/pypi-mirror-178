from setuptools import find_packages, setup

setup(
    name="tomclient",
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="TOMClient is a client library for TOM",
    version="0.0.18",
    scripts=["tomclient/tom"],
    package_dir={"tomclient": "tomclient"},
    packages=find_packages(),
    install_requires=[
        "typer",
        "jsonrpc-websocket",
        "netifaces",
        "nvidia-ml-py",
        "requests",
        "loguru",
        "rich",
        "humanize",
        "pyyaml",
        "bkm",
    ],
)
