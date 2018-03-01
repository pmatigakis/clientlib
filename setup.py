from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt") as f:
        requirements = [
            line.strip()
            for line in f
        ]

    return requirements


def get_test_requirements():
    with open("requirements-test.txt") as f:
        requirements = [
            line.strip()
            for line in f
        ]

    return requirements


setup(
    name='clientlib',
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="Client library for the topicaxis services",
    version='0.1.0',
    packages=find_packages(exclude=["tests"]),
    zip_safe=True,
    install_requires=get_requirements(),
    test_suite='nose.collector',
    tests_require=get_test_requirements(),
)
