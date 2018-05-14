from distutils.core import setup

setup(
    name='spatialkdtree',
    version='0.0.1',
    description='Create a kd-tree for spatiotemporal data, can retrieve fixed radius neighbors',
    long_description=open('README.txt').read(),
    author='Sudeep Basnet',
    author_email=['sbasnet@huskers.unl.com'],
    url='https://github.com/sudbasnet/spatiotemporal-kdTree',
    packages=['spatialkdtree'],
    license=['MIT'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
)
