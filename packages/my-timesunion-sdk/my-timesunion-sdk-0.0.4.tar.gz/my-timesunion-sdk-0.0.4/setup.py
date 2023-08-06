import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-timesunion-sdk",
    version="0.0.4",
    author="xhh",
    author_email="380472213@qq.com",
    description="A commonly used tool library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/my-timesunion-sdk/",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords=['my', 'times', 'union', 'sdk'],
    install_requires=[
        "requests",
        "arrow"
    ]
)