from setuptools import setup, find_packages

with open ("README.md", "r") as f:
  readme = f.read()

  
setup(
    name='pyomgclient',
    version='1.0.0',
    description='python omegle client',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Team XProjects',
    url='https://github.com/TheXProjects/pyomgclient',
    packages=find_packages(exclude=('tests', 'docs'))
)
