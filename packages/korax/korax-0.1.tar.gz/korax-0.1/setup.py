from setuptools import setup,  find_packages

setup(
    name='korax',
    packages=find_packages(),
    description='Useful tools which work with telegram bot mostly and provide veriety of service',
    version='0.1',
    url='https://github.com/Kora-Inc/Kora',
    author='Kittu',
    author_email='kushal.vstart@gmail.com',
    keywords=['chatbot','telegram','kora', 'python3'],

    license="MIT",
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=['requests'],
    )

