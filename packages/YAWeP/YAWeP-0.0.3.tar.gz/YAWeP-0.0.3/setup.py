import setuptools

setuptools.setup(
    name = "YAWeP",
    packages = ['YAWeP'],
    version = "0.0.3",
    author = "Leihaorambam Abhijit Singh",
    author_email = "labhijitsingh13@gmail.com",
    description = "Yet another weather package api",
    url="https://gitlab.com/AbhijitL/yawp",
    keywords=['weather','forecast','openwatherapi'],
    install_requires=[
        'requests',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6"
)