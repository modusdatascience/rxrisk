from setuptools import setup, find_packages
import versioneer
setup(name='rxrisk',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Matt Lewis',
      author_email='matt.lewis@modusdatascience.com',
      url='https://github.com/modusdatascience/rxrisk',
      package_data={'rxrisk': ['resources/*']},
      packages=find_packages(),
      requires=['pandas', 'xlrd', 'clinvoc']
     )