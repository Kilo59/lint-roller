from setuptools import setup, find_packages


NAME = "lint-roller"
VERSION = "18.0a"
DESCRIPTION = "Audit linting errors and identify cost savings."
REQUIRMENTS = ["pylint", "invoke"]
EXTRAS = {"format": ["black"]}


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=None,
    # long_description_content_type="text/markdown"
    # author=None,
    # author_email=None,
    # python_requires=None,
    # url=None,
    # entry_points=None,
    install_requires=REQUIRMENTS,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifier=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 2 - Pre-Alpha",
    ],
)

