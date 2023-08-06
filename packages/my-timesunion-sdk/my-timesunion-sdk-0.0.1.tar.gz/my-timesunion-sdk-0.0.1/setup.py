from setuptools import setup, find_packages

setup(
    name='my-timesunion-sdk',
    version='0.0.1',
    # keywords = ('chinesename',),  
    description='get a chinesename by random',
    license='MIT License',
    install_requires=[],
    packages=['my-timesunion-sdk'],  # 要打包的项目文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    author='mr.xhh',
    author_email='380472213@qq.com',
    # url='https://github.com/mouday/chinesename',
    # packages = find_packages(include=("*"),),  
)  