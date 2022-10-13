from setuptools import find_packages
from setuptools import setup

package_name = 'ros2_config_helper'

setup(
    name=package_name,
    version='1.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Ivan Santiago Paunovic',
    author_email='ivanpauno@ekumenlabs.com',
    maintainer='Ivan Santiago Paunovic',
    maintainer_email='ivanpauno@ekumenlabs.com',
    keywords=['ROS', 'ROS 2', 'ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Tool to generate a DDS profiles file based on the result of a questionnaire.',
    long_description=(
        'This package provides the ability to generate a DDS profiles file '
        'based on user preferences. '
        'It provides an API for that end, and also a command line tool.'),
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ros2_config_helper = ros2_config_helper.main:main',
        ],
    }
)
