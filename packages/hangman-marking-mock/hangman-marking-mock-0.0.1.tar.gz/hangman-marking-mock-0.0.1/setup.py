import setuptools

setuptools.setup(
    name="hangman-marking-mock",
    version="0.0.1",
    author="Ivan Ying",
    author_email="ivan@theaicore.com",
    description="An automated marking system for the hangman project (test)",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['requests', 'timeout-decorator']
)