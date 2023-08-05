import setuptools

setuptools.setup(
    name='pub_sub_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "dynaconf",
        "txp[cloud]==0.2.94"
    ],
    packages=setuptools.find_packages()
)
