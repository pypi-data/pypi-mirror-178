import setuptools
file0 = open("README.txt", 'r')
long_description = file0.read()
setuptools.setup(
    packages=setuptools.find_packages(),
    license="MIT",
    description="A Python Package For Networking Such As Servers/LocalHost ETC",
    author="Hunter Mikesell",
    version="1",
    name="NET",
    long_description=long_description,
    script_name='NET',
    platforms=[],
    author_email='huntermikesell84@gmail.com',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
)