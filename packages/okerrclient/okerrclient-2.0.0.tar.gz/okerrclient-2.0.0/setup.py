from setuptools import setup

setup(name='okerrclient',
    version='2.0.0',
    description='client for okerr cloud monitoring system',
    url='http://okerr.com/',
    author='Yaroslav Polyakov',
    author_email='xenon@sysattack.com',
    license='MIT',
    packages=['okerrclient'],
    scripts=['scripts/okerrclient'],
    data_files = [
        ('okerrclient',['data/oc', 'data/default'])
    ], 
    install_requires=['six', 'requests', 'psutil', 'evalidate', 'python-daemon'],
    include_package_data = True,
    zip_safe=False
)    

