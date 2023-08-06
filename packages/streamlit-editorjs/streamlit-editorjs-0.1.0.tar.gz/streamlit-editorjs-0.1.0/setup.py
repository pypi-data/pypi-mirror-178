from pathlib import Path
import setuptools


setuptools.setup(
    name="streamlit-editorjs",
    version="0.1.0",
    author="caviri",
    author_email="",
    description="EDITORJS component for Streamlit",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/caviri/streamlit-editorjs",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
