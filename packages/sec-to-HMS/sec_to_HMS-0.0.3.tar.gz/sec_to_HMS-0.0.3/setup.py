import setuptools 

with open('README.md',"r",encoding='utf-8') as f:
    full_description=f.read()

setuptools.setup(
    name="sec_to_HMS",
    version="0.0.3",
    author="junchen",
    author_email="rongjvzhou@outlook.com",
    description="将秒转换为时、分、秒格式",
    long_description=full_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
                 ],
    python_requires='>=3.6'
    )