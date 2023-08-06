from setuptools import setup

setup(
    name='scrapy-fake-useragent',
    version='0.0.2',
    description='Use a random User-Agent provided by fake-useragent every request',
    long_description=open('README.rst').read(),
    keywords='scrapy proxy web-scraping',
    license='New BSD License',
    author="Alexander Afanasyev",
    author_email='afanasieffav@gmail.com',
    url='https://github.com/alecxe/scrapy-fake-useragent',
    classifiers=[
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'scrapy_fake_useragent',
    ],
    install_requires=[
        'fake-useragent'
    ],
)
