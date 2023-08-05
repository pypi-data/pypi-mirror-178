# https://medium.com/%E8%B3%87%E5%B7%A5%E7%AD%86%E8%A8%98/%E6%89%93%E5%8C%85python-module-%E5%88%B0pypi-%E4%B8%8A-aef1f73e1774
from setuptools import setup, find_packages

setup(
    name="PyWebPtt",
    version="0.1.2",
    license='MIT',
    author="Tomoaki Chen",
    author_email="tomoaki.nccu@gmail.com",
    # packages=find_packages('src'),
    # package_dir={'': 'src'},
    packages=find_packages(),
    url='https://github.com/TomoakiChenSinica/PyWebPtt',
    keywords='使用 python 抓取 Web PTT 資料',
    install_requires=[
    ]
)
