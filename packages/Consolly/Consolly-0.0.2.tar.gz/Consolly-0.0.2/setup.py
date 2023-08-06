from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
    name='Consolly',
    version='0.0.2',
    url='',  
    author='Beete',
    author_email='beete@protonmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='console', 
    packages=find_packages(),
    install_requires=['colorama'] 
)