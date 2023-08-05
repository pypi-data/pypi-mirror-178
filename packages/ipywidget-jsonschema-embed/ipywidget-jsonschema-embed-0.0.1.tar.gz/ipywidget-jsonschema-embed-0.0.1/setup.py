import setuptools
import glob
import glob
import os

from ipywidget_jsonschema_embed import __version__
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipywidget-jsonschema-embed", # Replace with your own username
    version=__version__,
    author="hp027",
    author_email="hp027@foxmail.com",
    description="ipywidget_jsonschema_embed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hp027/ipywidget_jsonschema_embed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=open("./requirements.txt", "r").read().strip().split("\n"),
    data_files = [
        ('web', list(filter(os.path.isfile, glob.glob('ipywidget_jsonschema_embed/build/**/*', recursive=True))))
    ]
)
