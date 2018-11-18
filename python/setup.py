from setuptools import setup, find_packages

setup(
    name='haoc',
    version='0.0.1',
    description='Python 3 wrapper for headless Age of Empires 2',
    url='https://github.com/happyleavesaoc/aoc-headless/',
    license='MIT',
    author='happyleaves',
    author_email='happyleaves.tfr@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyAutoGUI==0.9.38',
        'pyscreenshot==0.4.2',
        'PyVirtualDisplay==0.2.1',
        'xlib==0.21'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
