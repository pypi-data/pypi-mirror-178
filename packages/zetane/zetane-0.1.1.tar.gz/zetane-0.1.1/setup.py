
from setuptools import setup, find_packages
import glob

setup(
    name = "zetane",
    author="Zetane Systems",
    author_email="info@zetane.com",
    description = "CLI version of Zetane API",
    long_description="Long description",
    long_description_content_type="text/markdown",
    version = "0.1.1",
    license="LICENSE.md",
    url="https://zetane.com",
    packages=find_packages(include=('protector.*','zetane')),
    entry_points = {
        'console_scripts': [
            'zetane = zetane.__main__:main'
        ]
    },
    python_requires='>=3.6',
    install_requires = ['python-dotenv', 'tqdm', 'requests', 'filetype'],
    include_package_data=True,
    package_data={'zetane': ['*.json']},)
