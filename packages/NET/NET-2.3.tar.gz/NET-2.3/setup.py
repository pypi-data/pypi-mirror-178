import setuptools
file0 = open("README.txt", 'r')
long_description = file0.read()

"""

NET Package! :)

Run: py -3.10 pip install NET

Enjoy The Pkg/Lib!

"""



setuptools.setup(
    packages=setuptools.find_packages(),
    license="MIT",
    description="A Powerfull Networking Package For Servers/LocalHosts ETC",
    author="Hunter Mikesell & Ben",
    version="2.3",
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