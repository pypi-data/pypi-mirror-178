from distutils.core import setup
setup(
  name = 'jani',
  packages = ['jani'],
  version = '0.2',
  license='MIT',
  description = 'This Scheduling Algorithm works on Data Frames',
  author = 'HARSH JANI',
  author_email = 'harshjani034699@gmail.com',
  url = 'https://github.com/harshjani53/schedulingAlgorithm',
  download_url = 'https://github.com/harshjani53/schedulingAlgorithm/archive/refs/tags/0.2.tar.gz',   
  install_requires=[
        'pandas','openpyxl'
      ])