from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()
except FileNotFoundError:
    long_description = 'README.md not found.'

version = __import__('vbe_decoder').__version__

setup(
    name="vbe_decoder",
    version=version,
    url='http://www.github.com/williamgibb/vbe_decoder/',
    author='William Gibb',
    author_email='williamgibb@gmail.com',
    description='Encoded Visual Basic script decoder',
    long_description=long_description,
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
