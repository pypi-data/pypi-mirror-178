from setuptools import setup

with open('README.md', 'r') as f:
    LD = f.read()
VERSION = '0.5.3'

if __name__ == '__main__':
    setup(
    name='TPython',
    version=VERSION,
    description='A better python REPL',
    long_description=LD,
    long_description_content_type='text/markdown',
    url='https://github.com/Techlord210/TPython',
    author='Techlord210',
    author_email='techlord210@gmail.com',
    license='MIT',
    classifiers=[
            "Development Status :: 4 - Beta",
            'Environment :: Console',
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License"
        ],
    install_requires=[
        'colorama',
        'requests',
        ],
    entry_points={
        'console_scripts':[
            'tpy = main:main'
            ]
        }
    )