from setuptools import setup


setup(
    name='smsaero_api',
    version='2.1.1',
    description='Send SMS/FlashCalls via smsaero.ru gate',
    keywords=['sms', 'sendings', 'hlr', 'viber', 'calls', 'flashcalls'],
    # long_description=open('README.rst').read(),
    author='Apelt Dmitry',
    author_email='apelt.dmitry@gmail.com',
    url='https://smsaero.ru/integration/class/python',
    license='MIT',
    packages=['smsaero'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'requests',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
