from distutils.core import setup
setup(
    name='struthon',
    version='0.4.5.2',
    description='structural engineering design python applications',
    long_description = open("README.txt").read(),
    author='Lukasz Laba',
    author_email='lukaszlab@o2.pl',
    url='https://www.struthon.org',
    packages=['struthon', 'struthon.ConcreteMonoSection', 'struthon.ConcretePanel', 'struthon.ConcretePanel.Example_data_files', 'struthon.SteelSectionBrowser', 'struthon.SteelMonoSection'],
    package_data = {'': ['*.xls', '*.csv']},
    license = 'GNU General Public License (GPL)',
    keywords = 'civil engineering ,structural engineering, concrete structures, steel structures',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    )
