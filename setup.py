from setuptools import setup, find_packages

setup(
    name="paypal_client",
    version="0.2.1",
    packages=find_packages(),
    description="The PayPal API provides simple client for RESTful APIs",
    long_description="Simple client for PayPal RESTful APIs",
    author="Dmitry Kalinin",
    url="https://github.com/null-none/paypal-client",
    install_requires=[
        "requests",
    ],
)
