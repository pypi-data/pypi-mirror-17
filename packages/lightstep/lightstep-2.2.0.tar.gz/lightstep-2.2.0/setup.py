from setuptools import setup, find_packages

setup(
    name='lightstep',
    version='2.2.0',
    description='LightStep Python OpenTracing Implementation',
    long_description='',
    author='LightStep',
    license='',
    install_requires=['thrift==0.9.2',
                      'jsonpickle',
                      'pytest',
                      'basictracer>=2.2,<2.3',
                      'opentracing>=1.2,<1.3'],
    tests_require=['sphinx',
                   'sphinx-epytext'],

    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],

    keywords=[ 'opentracing', 'lightstep', 'traceguide', 'tracing', 'microservices', 'distributed' ],
    packages=find_packages(exclude=['docs*', 'tests*', 'sample*']),
)
