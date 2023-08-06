from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="instareset",
    version="2.0.0",
    author="Khaled Mahmoud",
    author_email="KhalidYBel@gmail.com",
    description="Send password reset requests to Instagram accounts without reCaptcha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/Kh4lidMD/InstaReset",
    packages=find_packages(),
    install_requires=['requests', 'rich'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License'
    ]
)
