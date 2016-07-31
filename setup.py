import setuptools.command.test
from setuptools import find_packages, setup


# http://stackoverflow.com/questions/17001010/how-to-run-unittest-discover-from-python-setup-py-test
# http://stackoverflow.com/a/23443087
class TestCommand(setuptools.command.test.test):
    """ Setuptools test command explicitly using test discovery. """
    def _test_args(self):
        yield 'discover'


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
    zip_safe=True,
    cmdclass={
        'test': TestCommand,
    },
)