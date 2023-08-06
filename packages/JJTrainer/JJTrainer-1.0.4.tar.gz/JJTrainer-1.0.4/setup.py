from distutils.core import  setup
import setuptools
packages = ['JJTrainer']# 唯一的包名，自己取名
setup(name='JJTrainer',
    version='1.0.4',
    author='RenjieYu',
    author_email='770819952@qq.com',
    packages=packages,
    install_requires=[
        'numpy',
        'torch',
        'tqdm',
        'sklearn',
    ],
    package_dir={'requests': 'requests'})
