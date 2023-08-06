import setuptools

setuptools.setup(
    name='pyzed',
    install_requires=[
        'durationpy',
        'python-dateutil',
        'requests',
    ],
    py_modules=['pyzed'],
    python_requires='>=3.3',
)
