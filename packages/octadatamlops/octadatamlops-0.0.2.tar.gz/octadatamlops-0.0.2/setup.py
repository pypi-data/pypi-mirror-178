from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='octadatamlops',
  version='0.0.2',
  description='A controller to model pipeline',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Diego Marcello',
  author_email='diego.marcello.sp@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mlops', 
  packages=find_packages(),
  install_requires=[''] 
)