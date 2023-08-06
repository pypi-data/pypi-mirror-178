import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AddingLib",
    version="0.0.9",
    author="Yegor",
    author_email="maystrenko.yegor.my@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yegormaystrenko/AddLibriary.git",
 #  package_dir={
# 'fonts': 'resources/fonts',
# 'images': 'resources/images',
# 'js': 'resources/js',
# 'maps': 'resources/maps',
# 'qml': 'resources/qml',
# 'sounds': 'resources/sounds',
# 'tr': 'resources/tr',
# },
    packages=setuptools.find_packages(),
    include_package_data=True,
    #packages=['fonts','images','js','maps','qml','sounds','tr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
