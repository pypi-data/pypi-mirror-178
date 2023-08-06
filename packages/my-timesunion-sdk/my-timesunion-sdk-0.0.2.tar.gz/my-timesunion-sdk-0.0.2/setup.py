from setuptools import setup, find_packages

setup(
    name='my-timesunion-sdk',
    version='0.0.2',
    # keywords = ('chinesename',),  
    description='Self-use SKD test package',
    license='MIT License',
    install_requires=[],
    packages=['my-timesunion-sdk'],  # 要打包的项目文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    author='mr.xhh',
    author_email='380472213@qq.com',
    # url='https://github.com/mouday/chinesename',
    # packages = find_packages(include=("*"),),  
)  