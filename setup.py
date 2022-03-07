from setuptools import setup

setup(
    name             = 'interpolate-surface-with-sphere',
    version          = '0.1.1',
    description      = 'Resample a surface mesh to have 81,920 triangles.',
    author           = 'Jennings Zhang',
    author_email     = 'Jennings.Zhang@childrens.harvard.edu',
    url              = 'https://github.com/FNNDSC/ep-interpolate-surface-with-sphere',
    py_modules       = ['isws'],
    install_requires = ['chris_plugin', 'pycivet', 'loguru'],
    license          = 'MIT',
    python_requires  = '>=3.10.2',
    entry_points     = {
        'console_scripts': [
            'isws = isws:main'
        ]
    },
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
