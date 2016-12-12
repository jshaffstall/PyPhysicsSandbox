from distutils.core import setup
setup(
    name = 'pyphysicssandbox',
    packages = ['pyphysicssandbox', 'py2d'],
    version = '1.0',
    description = 'A simple Python physics sandbox for intro programming students',
    author = 'Jay Shaffstall',
    author_email = 'jshaffstall@gmail.com',
    url = 'https://github.com/jshaffstall/PyPhysicsSandbox',
    download_url = 'https://github.com/jshaffstall/PyPhysicsSandbox/tarball/0.1',
    keywords = ['physics'],
    classifiers = [],
    setup_requires=['wheel'],
    requires=['pygame','pymunk'],
)
