from setuptools import setup

setup(
    name='LiveStockPrice',
    version='1',
    packages=['StockPrices'],
    url='https://github.com/TheA12W/LiveStockPrice',
    license='MIT',
    author='adrianw',
    author_email='',
    description='A webscrapper to get live price of any stock',
    install_requries =[
        'beautifulsoup4'
        'requests'
        'html5lib'
    ]
)
