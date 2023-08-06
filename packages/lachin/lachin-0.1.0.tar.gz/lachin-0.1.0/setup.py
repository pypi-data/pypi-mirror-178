from setuptools import setup


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='lachin',
      version='0.1.0',
      description='A Python Toolkit for Simulation of the UAVs.',
      long_description=long_description,
      long_description_content_type='text/markdown', 
      url='https://github.com/Haghrah/Lachin',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='MIT',
      packages=['lachin'],
      install_requires=['numpy', 'scipy', 'matplotlib', ],
      python_requires='>=3.6',
      zip_safe=False)