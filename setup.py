from setuptools import setup

setup(
    name='noisecut',
    version='0.0.1',
    author='Zahra Zali',
    license='AGPLv3',
    package_dir={
        'noisecut': 'src'
    },
    packages=[
        'noisecut'],
    install_requires=[
        'numpy<=1.21',
        'matplotlib',
        'obspy',
        'librosa',
    ],
)
