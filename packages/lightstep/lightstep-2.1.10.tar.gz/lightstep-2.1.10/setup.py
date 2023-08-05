from setuptools import setup, find_packages

setup(
    name='lightstep',
    version='2.1.10',
    description='LightStep Python OpenTracing Implementation',
    long_description='',
    author='LightStep',
    license='',
    install_requires=['thrift==0.9.2',
                      'jsonpickle',
                      'pytest',
                      'basictracer>=2.1,<2.2',
                      'opentracing>=1.1,<1.2'],
    tests_require=['sphinx',
                   'sphinx-epytext'],

    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 3',
    ],

    keywords=[ 'opentracing', 'lightstep', 'traceguide', 'tracing', 'microservices', 'distributed' ],
    packages=find_packages(exclude=['docs*', 'tests*', 'sample*']),
)
