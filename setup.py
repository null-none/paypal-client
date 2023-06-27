from setuptools import setup

setup(
    name="paypal_client",
    version="0.2.1",
    keywords="python, pay pal, rest api, paypal",
    description="The PayPal API provides simple client for RESTful APIs",
    long_description="Simple client for PayPal RESTful APIs",
    author="Dmitry Kalinin",
    url="https://github.com/null-none/paypal-client",
    license="MIT",
    packages=["paypal_client"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "requests",
    ],
)
