from setuptools import setup

setup(name='citytour',
      version='0.1',
      description='Find constrained best path in city between two points',
      long_description='Given a city map with connected traffic light nodes, and certain constraints on movement, \
      find the fastest path between two nodes.',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Constrained Path Finding :: Algorithm',
      ],      
      url='http://github.com/run2/citytour',
      author='Run2',
      author_email='b.debanjan@gmail.com',
      license='MIT',
      packages=['citytour'],
      install_requires=[], # add your requirements here
      zip_safe=False
      )