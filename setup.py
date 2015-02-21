from setuptools import setup

setup(
	name='FFS',
	version='0.1',
	description='Free and For Sale',
	url='http://github.com/skxu/FFS',
	author='Sam Xu',
	author_email='skx@berkeley.edu',
	license='MIT',
	packages=[],
	install_requires=[
		'flask',
		'flask-restful',
		'Flask-ZODB',
		'oauth2',
		'apscheduler',
		'facebook-sdk'
	],
	zip_safe=False)