from setuptools import find_packages, setup

package_data = [
    'lib/libtag_c.dll',
    'lib/libtag_c.so',
    'tests',
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytag",
    version="0.0.1",
    author="Hussein Sarea",
    author_email="zzzsssx0@gmal.com",
    description="cross-platform, Python 3.x audio metadata (tagging) library based on TagLib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ho011/pytag",
    project_urls={
        "Bug Tracker": "https://github.com/Ho011/pytag/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(
        include=["pytag", "pytag.*", 'pytag.lib', "pytag.lib.*"],
        exclude=[],
    ),
    include_package_data=True,
    package_data={
        'pytag':package_data
    },
    python_requires=">=3.6",
)