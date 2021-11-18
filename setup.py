from setuptools import setup

setup(
    name='soccminer',
    version='0.0.23a1',
    packages=['soccminer'],
    scripts=['bin/main.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
    platforms='Linux',
    url='https://github.com/M3SOulu/SoCC-Miner',
    license='MIT',
    author='da_enthusiast',
    author_email='dataapproximation.enthusiast@gmail.com',
    description='Source Code Comments Miner Tool',
    install_requires=['lxml', 'numpy', 'python-dateutil', 'six', 'pytz', 'requests', 'certifi', 'charset-normalizer', 'idna', 'urllib3', 'ujson'],
    zip_safe=False
)
