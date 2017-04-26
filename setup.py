from distutils.core import setup
setup(
    name = 'pyphysicssandbox',
    packages = ['pyphysicssandbox', 'py2d', 'py2d.Math'],
    version = '1.4.1',
    description = 'A simple Python physics sandbox for intro programming students',
    author = 'Jay Shaffstall',
    author_email = 'jshaffstall@gmail.com',
    url = 'https://github.com/jshaffstall/PyPhysicsSandbox',
    download_url = 'https://github.com/jshaffstall/PyPhysicsSandbox/tarball/1.4.1',
    keywords = ['physics'],
    classifiers = [],
    install_requires = ['pygame','pymunk'],
)
