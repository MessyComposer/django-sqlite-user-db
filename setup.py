from setuptools import setup, find_packages

setup(
    name="django-sqlite-user-db",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2.16",
        "asgiref>=3.8.1"
    ],
    test_requires=[
        "django>=4.2.16",
        "asgiref>=3.8.1"
    ],
    author="Messy Composer",
    author_email="",
    description="A Django package to create and manage user-specific SQLite databases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MessyComposer/django-sqlite-user-db",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
