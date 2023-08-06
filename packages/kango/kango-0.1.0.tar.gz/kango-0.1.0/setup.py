import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()

VERSION = "0.1.0"
setuptools.setup(
    name='kango',
    version=VERSION,
    author='Mardix',
    author_email='mardix@blackdevhub.io',
    description='kango ',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/mardix/kango',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    python_requires='>=3.8.0',
    install_requires = [
        "flask",
        "slugify",
        "arrow",
        "ulid",
        "python-arango"
    ],
    packages=['kango'],
    package_dir={'':'src'}
)
