import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="stern",
    version="1.3",
    author="saivan",
    author_email="vasilsalkou@gmail.com",
    description="Python module by developer saivan",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VasilSalkov/stern",
    packages=['stern'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)