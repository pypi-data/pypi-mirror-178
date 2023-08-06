from setuptools import setup, find_packages

setup(
    name='SWTK',
    version='1.4',
    description='Sort txt file from weirdest line to last. Meant to be used for Logs.An experimental Unsupervised Learning Log Anomaly Detection toolkit. YOU ARE BEAUTIFUL! This will sort the input based on weirdness',
    url='https://github.com/nileshkhetrapal/SWTK',
    author='Nilesh Khetrapal',
    packages=find_packages(),
    scripts=['bin/SWTK'],
)

