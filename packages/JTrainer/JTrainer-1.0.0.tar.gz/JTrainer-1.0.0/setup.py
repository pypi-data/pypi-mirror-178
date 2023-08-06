from distutils.core import  setup
import setuptools
packages = ['JTrainer']# 唯一的包名，自己取名
setup(name='JTrainer',
    version='1.0.0',
    author='RenjieYu',
    author_email='770819952@qq.com',
    packages=packages,
    install_requires=[
        'numpy',
        'torch',
        'tqdm',
        'sklearn',
        'json',
    ],
    package_dir={'requests': 'requests'})
