import setuptools
file0 = open("README.txt", 'r')
long_description = file0.read()


setuptools.setup(
    packages=setuptools.find_packages(),
    license="MIT",
    description=long_description,
    author="Hunter Mikesell",
    version="2.2",
    name="NET",
    long_description=long_description,
    long_description_content_type='text/markdown',
    script_name='NET',
    platforms=[],
    author_email='huntermikesell84@gmail.com',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
)