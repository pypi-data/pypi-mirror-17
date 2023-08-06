from distutils.core import setup


setup(
  name = 'pyfmm',
  packages = ['pyfmm'], # this must be the same as the name above
  version = '0.3',
  description = 'Python module implementing the Fast Marching Method.',
  #long_description=open('README.md', 'rt').read(),
  author = 'Vegard Kvernelv',
  author_email = 'vkvernelv@gmail.com',
  url = 'https://github.com/vegardkv/pyfmm', # use the URL to the github repo
  download_url = 'https://github.com/vegardkv/pyfmm/tarball/0.2.1', # I'll explain this in a second
  keywords = ['fast marching method', 'eikonal', 'fmm', 'distance'], # arbitrary keywords
  license='MIT',
  classifiers=[],
)