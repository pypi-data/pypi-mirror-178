import setuptools


required = [
    'confuse',
]

setuptools.setup(
    name="qrconfig",
    version="1.0.5",
    author="Kurush",
    author_email="ze17@ya.ru",
    description="Config wrapper for object-style usage",
    long_description_content_type="text/markdown",
    url="https://github.com/Kurush7/qr_server",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description='''
# qrconfig

Can access dictionary items both as dictionary (like config['field']) and as an attribute (config.field),
recursively: config.field.subfield.subsubfield...
Also supports item assignment to update the configuration in runtime.

### Usage example:
```python
from qrconfig import QRYamlConfig

config = QRYamlConfig('config.yaml')
a = config.a
b = config['b']
config.a = 4
```
'''
)
