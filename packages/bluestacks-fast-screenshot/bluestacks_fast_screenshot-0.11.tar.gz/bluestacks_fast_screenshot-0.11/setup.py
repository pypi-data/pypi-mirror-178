from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "This module takes screenshots of BlueStacks using the win32 API, resizes and crops them to the same size of an ADB screenshot."

# Setting up
setup(
    name="bluestacks_fast_screenshot",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/bluestacks_fast_screenshot',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords=['bluestacks', 'adb', 'openCV', 'win32', 'screenshots', 'windows', 'bot', 'video', 'streaming'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'adb_screencap_streaming', 'keyboard', 'numpy', 'opencv_python', 'pandas', 'scikit_image',  'window_capture_streaming'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*