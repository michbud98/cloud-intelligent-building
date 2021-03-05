from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

deps_required = [
	'requests>=2.25.1', 'apscheduler>=3.7.0'
]

deps_tests = []

setup(
    name='dummy_machines',
    version='0.0.0.1',
    description="""A script that automatically requests REST paths.""",
    long_description=long_description,
    keywords="michbud, web, requests",
    setup_requires=['pytest-runner'],
    install_requires=deps_required,
    tests_require=deps_tests,
    
    # Can then by installed by 'pip install ".[dev]"'
    extras_require={
        'dev':  (['sphinx>=3.4.3', 'notebook>=6.2.0'] + deps_tests)
    },
    python_requires='>=3.7',
    author='Michal Budik',
    author_email='swiftblade1982@gmail.com',
    license='Public Domain',
    url='',
    zip_safe=False,
	package_dir={'': 'src'},
    packages=find_packages(where='src'),

    # Entrypoint structure -> 'name = <module_name>:<function_or_class_name>'
    # entry_points={
    #     'masters_thesis_server.db_handlers': [
    #         'mongodb = scrapers.mongodb_handler:MongoDBHandler',
    #     ]
    # },
    # package_data={
    #     'ghia': ['templates/*.html', 'static/*.css']
    #     },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Framework :: FastAPI',
        'Environment :: Web Environment'
        ],
)