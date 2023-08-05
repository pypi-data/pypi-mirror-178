from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='ankimaker',
    version='0.0.4',
    description='Makes anki with files',
    url="https://git.lgoon.xyz/gabriel/ankimaker",
    license="BSD-3-Clause",
    license_files='LICENSE',
    packages=find_packages('src', include=['ankimaker*']),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'ankimaker=ankimaker.cli:main',
        ]
    },
    include_package_data=True,
    long_description=readme(),
    install_requirements=[
        "click",
        "genanki",
        "pandas",
        "pyyaml",
    ],
    long_description_content_type='text/markdown',
)
