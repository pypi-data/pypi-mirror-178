from distutils.core import setup
setup(
    name='csa_nemo_layer',
    packages=['csa_nemo_layer'],
    version='0.0.4',
    license='MIT',
    description='Layer for CSA project Nemo',
    author='struk',
    author_email='andrii@struk.net.ua',
    url='https://github.com/struk77/csa_nemo_layer',
    download_url='https://github.com/struk77/csa_nemo_layer/archive/v_0.0.4.tar.gz',
    keywords=['AWS', 'AIOBOTO3'],
    install_requires=['aioboto3', 'simplejson', 'aws_lambda_powertools'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
