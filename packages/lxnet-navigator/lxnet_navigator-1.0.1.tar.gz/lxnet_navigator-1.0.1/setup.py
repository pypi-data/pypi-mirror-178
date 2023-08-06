from setuptools import setup, find_packages

setup_args = dict(
    name='lxnet_navigator',
    version='1.0.1',
    description='For Private Use',
    license='Unlicensed',
    packages=find_packages(),
    author='Bruce W Lee',
    author_email='woongsung.lee@gmail.com',
    keywords=['WordNet'],
    url='',
    download_url='https://pypi.org/project/lxnet_navigator/'
)

if __name__ == '__main__':
    setup(**setup_args, install_requires=['pandas', 'numpy', 'ndjson', 'tqdm'])