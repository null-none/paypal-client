from setuptools import setup, find_packages

setup(
    name="paypal_client",
    version="0.1.2",
    packages=find_packages(),
    author="Dmitry Kalinin",
    url="https://github.com/null-none/paypal-client",
    install_requires=[
        "requests",
    ],
)
