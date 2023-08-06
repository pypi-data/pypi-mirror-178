from os import path
from setuptools import setup, find_packages
from find_palindroms import __about__


try:
    current_path = path.abspath(path.dirname(__file__))
except NameError:
    current_path = None


try:
    with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''


setup(
    name=__about__.__title__,
    version=__about__.__version__,
    license='MIT License',
    author=__about__.__author__,
    author_email=__about__.__email__,
    description='find palindroms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(), # packages=['test_package'],
    python_requires='>=3.5', # pip проверит версии на совпадение
    install_requires=[], # внешние зависимости, будут установлены pip при установке этого пакета
    entry_points={
        'console_scripts': [
            'main=find_palindroms:main',
            'do_iterations=find_palindroms.find_palindrom:do_iterations',
        ],
    },
)
