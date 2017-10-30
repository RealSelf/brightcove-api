from setuptools import setup

setup(name="brightcove_api",
    version=1.0,
    description="SDK for the Brightcove Analytics API",
    url="https://github.com/nickymikail/brightcove-api",
    download_url = 'https://github.com/nickymikail/brightcove-api/archive/1.0.tar.gz',
    author="Nicholas Hassell",
    author_email="hasselln@gmail.com",
    license="MIT",
    install_requires=[
        'requests'
    ],
    packages=['brightcove_api'],
    keywords = ['business intelligence','bi','brightcove'])