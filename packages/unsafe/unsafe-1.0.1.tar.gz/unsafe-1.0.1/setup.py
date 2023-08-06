import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "unsafe",
    version = "1.0.1",
    author = "ahura",
    author_email = "ahur4.rahmani@gmail.com",
    description = "Pentesting Module",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ahur4/unsafe",
    project_urls = {
        "Telegram": "https://t.me/ahur4",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "unsafe"},
    packages = setuptools.find_packages(where="unsafe"),
    python_requires = ">=3.6"
)