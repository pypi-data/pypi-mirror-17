from setuptools import setup, find_packages

setup(
    name='PyAnimeList',
    version='1.1.0',
    packages=find_packages(),
    url='https://github.com/GetRektByMe/PyAnimeList',
    license='MIT',
    author='Recchan',
    author_email='',
    description='Python 3 bindings for the MyAnimeList API.',
    long_description='An async wrapper for the MyAnimeList api.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="aiohttp asyncio myanimelist xml parsing",
    install_requires=['aiohttp', 'bs4', 'lxml', 'dicttoxml'],
)
