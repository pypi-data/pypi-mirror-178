from setuptools import setup, find_packages


setup_args = dict(
    name='python-ims',
    version='1.0',
    description='Israel Meteorological Service unofficial python api wrapper',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Tomer Klein',
    author_email='tomer.klein@gmail.com',
    keywords=['ims', 'py-ims', 'Israel Meteorological Service','Meteorological Service','weather'],
    url='https://github.com/t0mer/python-ims',
    download_url='https://pypi.org/project/python-ims/'
)

install_requires = [
    'Pillow',
    'pandas'
    
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)