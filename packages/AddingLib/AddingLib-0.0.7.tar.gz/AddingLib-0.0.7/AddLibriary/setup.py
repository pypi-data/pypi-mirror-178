import setuptools

setuptools.setup(
    name='resources',
    version='0.0.7',
    package_dir={'fonts': 'fonts','images':'images','js':'js','maps':'maps','qml':'qml','sounds':'sounds','tr':'tr'},
    packages=['fonts','images','js','maps','qml','sounds','tr'],
    include_package_data=True
)
