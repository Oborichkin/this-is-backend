import setuptools

setuptools.setup(
    name="theBackend",
    packages=setuptools.find_packages(),
    version="0.1.0",
    description="The backend for This is SIP project",
    author="Pavel Oborin",
    author_email="oborin.p@gmail.com",
    url="https://github.com/Oborichkin/this-is-backend",
    python_requires=">=3.6",
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "RfcParser @ git+https://github.com/Oborichkin/rfc-parser.git@ec534a0801ad3eb9edbcd0c4f7e11bf94372cdd1#egg=RfcParser",
        "aiohttp"
    ]
)
