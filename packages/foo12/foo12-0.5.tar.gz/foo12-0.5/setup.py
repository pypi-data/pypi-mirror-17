from distutils.core import setup
setup(
  name = 'foo12',
  packages = ['foo12'], # this must be the same as the name above
  version = '0.5',
  description = 'A random test lib 0.3',
  author = 'Fengyi',
  author_email = 'fengyisn@gmail.com',
  url = 'https://github.com/fengsongAWS/foo', # use the URL to the github repo
  download_url = 'https://github.com/fengsongAWS/foo/archive/0.5.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
