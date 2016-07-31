from setuptools import setup


version = __import__('vbe_decoder').__version__

setup(
    name="vbe_decoder",
    version=version,
    url='http://www.github.com/williamgibb/vbe_decoder/',
    author='William Gibb',
    author_email='williamgibb@gmail.com',
    description=('Encoded Visual Basic script decoder'),
    license='MIT',
    packages=['vbe_decoder',
              ],
    entry_points={'console_scripts': [
        'vbe_decoder=vbe_decoder.__main__:_main',
    ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
        'Topic :: System :: Recovery Tools',
    ],
    zip_safe=True
)