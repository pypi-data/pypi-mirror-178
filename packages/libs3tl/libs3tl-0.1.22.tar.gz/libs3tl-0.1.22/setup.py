from setuptools import setup

setup(
    name='libs3tl',
    version='0.1.22',
    description='This is a 3TL module for pipeline creation',
    long_description_content_type=open('README.txt').read(),
    url='https://3tl.dev',
    author='Thinkartha',
    author_email='navin.naik@thinkartha.com',
    license='BSD 2-clause',
    packages=['libs3tl'],
    install_requires=[
                      'jproperties==2.1.1',
                      'redis==4.3.4',
                      'requests==2.28.1',
                      'toolz==0.12.0',
                      'urllib3==1.26.10',
                      'urllib3==1.26.10',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)