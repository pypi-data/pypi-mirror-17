from setuptools import setup

def readme():
    try:
        import pypandoc
    except ImportError:
        return ''

    return pypandoc.convert('README.md', 'rst')

setup(
    name='python-ta',
    version='0.1.6',
    description='Code checking tool for teaching Python',
    long_description=readme(),
    url='http://github.com/pyta-uoft/pyta',
    author='David Liu',
    author_email='david@cs.toronto.edu',
    license='MIT',
    packages=['pyta', 'pyta.reporters', 'pyta.checkers'],
    install_requires=[
        'pylint',
        'colorama',
        'six',
        'jinja2'
    ],
    include_package_data=True,
    zip_safe=False)
