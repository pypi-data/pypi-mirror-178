import setuptools
with open(r'C:\Users\Nazar\Desktop\UploadToPypi\TGConvertor\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='TGConvertor',
	version='0.0.2',
	author='nazar220160',
	author_email='nazar.fedorowych@gmail.com',
	description='This module is small util for easy converting Telegram sessions',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/nazar220160/TGConvertor/',
	packages=['TGConvertor'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)