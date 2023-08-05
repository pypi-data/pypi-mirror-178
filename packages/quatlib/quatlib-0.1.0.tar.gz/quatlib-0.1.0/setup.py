from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='quatlib',
  version='0.1.0',
  description='A very basic quaternion library for transformation between quaternion, Rotation matrix, Euler angle and many more.',
  long_description_content_type="text/markdown",
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Subhadeep Paul',
  author_email='sp323511@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='quaternion', 
  packages=find_packages(),
  install_requires=['numpy','scipy'] 
)
