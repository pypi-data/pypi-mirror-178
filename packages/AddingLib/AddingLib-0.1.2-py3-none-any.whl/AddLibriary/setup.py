import setuptools

setuptools.setup(
    name='resources',
    version='0.1.2',
    package_dir={'fonts': 'fonts','images':'images','js':'js','maps':'maps','qml':'qml','sounds':'sounds','tr':'tr'},
    packages=['fonts','images','js','js/desktop','maps','qml','sounds','sounds/chimes','tr'],
    
)
