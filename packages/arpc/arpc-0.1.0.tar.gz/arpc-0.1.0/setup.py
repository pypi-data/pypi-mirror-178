import setuptools

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arpc",
    version="0.1.0",
    author="ahriknow",
    author_email="ahriknow@ahriknow.com",
    description="A framework of remote procedure call.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahrirpc/arpc-python",
    packages=setuptools.find_packages(),
    py_modules=['main'],
    entry_points = {
        "console_scripts": [
            "arpc = arpc.utils:main"
        ]
    },
    extras_require={
        "async": ["nest_asyncio>=1.5.6"]
    },
    license="Apache License 2.0",
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
