from setuptools import find_packages
from setuptools import setup


setup(
    name="gobre.recipe.template",
    version='2.0',
    author="gocept",
    author_email="mail@gocept.com",
    url="https://github.com/gocept/gobre.recipe.template",
    description="Buildout recipe for making files out of Jinja2 templates",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Buildout",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Pre-processors",
    ],
    keywords="zc.buildout recipe template Jinja2",
    license="BSD",
    packages=find_packages(),
    namespace_packages=("gobre", "gobre.recipe"),
    python_requires='>=3.7',
    install_requires=(
        "setuptools",
        "zc.recipe.egg",
        "Jinja2",
        "zope.dottedname",
    ),
    zip_safe=True,
    entry_points="""
        [zc.buildout]
        default = gobre.recipe.template:Recipe
    """,
)
