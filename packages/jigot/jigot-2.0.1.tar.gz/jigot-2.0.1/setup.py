import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jigot",
    version="2.0.1",
    author="JiGOT-Dev",
    author_email="meoawlove.bam@gmail.com",
    description="easy to make / discord bot with template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://discord.gg/UKYKatXGVJ",
    project_urls={
        "Bug Tracker": "https://github.com/JiGOT-Dev/jigot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    entry_points={
                        'console_scripts': [
                                'jgdcmd=jgd.jgd:template',
                        ]
                }
)
