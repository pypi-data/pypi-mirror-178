import setuptools
with open(r'C:\Users\zadvo\Desktop\My Library\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='PyQwidgets',
	version='3.0',
	author='Georg8528',
	author_email='zadvornow2908@gmail.com',
	description='Mini-framework ',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['My Library'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)