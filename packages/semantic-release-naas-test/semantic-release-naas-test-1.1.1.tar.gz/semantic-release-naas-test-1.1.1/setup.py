from setuptools import setup, find_packages

setup(
	name='semantic-release-naas-test',
    description="Test semantic release",
    long_description="Simply test semantic release with pypi",
    long_description_content_type="text/x-rst",
    author="Maxime Jublou",
    author_email="maxime@naas.ai",
    maintainer="Maxime Jublou",
    maintainer_email="maxime@naas.ai",
    url="",
    keywords=["test", "semantic-release"],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "naas-proxy-manager==1.3.0"
    ],
    extras_require={
        'deploy': [
            "twine~=4.0"
        ]
    }
)