from setuptools import setup

setup(name='darkskylib',
      version='0.2.2',
      description='The Dark Sky API wrapper',
      url='https://github.com/lukaskubis/forepycast',
      author='Lukas Kubis',
      author_email='contact@lukaskubis.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='weather forecast',
      packages=['darksky'],
      install_requires=[
          'requests',
          'future'
      ],
      zip_safe=False
      )
