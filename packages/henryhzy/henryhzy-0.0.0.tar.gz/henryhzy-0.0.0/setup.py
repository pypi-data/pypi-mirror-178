from setuptools import setup, find_packages

str_version = '0.0.0'

setup(
    name='henryhzy',
    version=str_version,
    description='Just for testing.',
    url='https://henryhzy.github.io/',
    author='henryhzy',
    author_email='henryhuzy@gmail.com',
    license='MIT',
    packages=['henryhzy'],
    entry_points={ # [可以直接在命令行输入henryhzy]
        'console_scripts': [
            'henryhzy=henryhzy:henryhzy',
        ]
    }
    # packages=find_packages()
)