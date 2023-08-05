from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='serial-fingers-control',
    version='0.0.2',
    packages=['serial_fingers_control'],
    url='https://github.com/Adam-Software/Serial-fingers-control',
    license='MIT',
    author='vertigra',
    author_email='a@nesterof.com',
    description='Finger control for STM32 old Api',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['Adam-Serial-for-controller'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
