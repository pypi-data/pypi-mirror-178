from setuptools import find_packages, setup


setup(
    name='kiki_utils_ssh',
    classifiers=[
        'License :: Freely Distributable'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    version='1.0.0',
    description='Utils ssh functions',
    author='kiki-kanri',
    author_email='a470666@gmail.com',
    keywords=['Utils'],
    install_requires=[
        'asyncssh'
    ],
    python_requires=">=3.6"
)
