import setuptools

with open("readme.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req:
    requires = req.read().strip().split('\n')

setuptools.setup(
    name="drf_errors",
    version="0.1",
    author="Dmitry Kalinin",
    author_email="mitko.kalinin@gmail.com",
    description="Extension for Django REST framework error display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/null-none/drf-errors',
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/null-none/drf-errors',
    },
)