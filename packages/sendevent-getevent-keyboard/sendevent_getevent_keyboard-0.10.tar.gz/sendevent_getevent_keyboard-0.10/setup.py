from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "ADB sendevent - press multiple keys at the same time, control the duration of each event!"

# Setting up
setup(
    name="sendevent_getevent_keyboard",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/sendevent_getevent_keyboard',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['flatten_everything', 'flexible_partial', 'keyboard', 'kthread', 'more_itertools', 'numpy', 'pandas', 'psutil', 'regex', 'requests', 'touchtouch'],
    keywords=['bluestacks', 'adb', 'keystrokes', 'keys', 'getevent', 'sendevent'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['flatten_everything', 'flexible_partial', 'keyboard', 'kthread', 'more_itertools', 'numpy', 'pandas', 'psutil', 'regex', 'requests', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*