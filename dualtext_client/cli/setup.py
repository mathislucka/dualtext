from setuptools import setup


setup (
        name='DualtextCli',
        version='1.0',
        py_modules=['dualtext'],
        install_requires=[
            'Click',
        ],
        entry_points='''
            [console_scripts]
            dualtext=dualtext:cli
        '''
)
