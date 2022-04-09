import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pyperfmon",
	version="0.1",
	author="damies13",
	author_email="damies13+pyperfmon@gmail.com",
	description="pyperfmon",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/damies13/pyperfmon",
	packages=setuptools.find_packages(exclude=["build/*"]),
	install_requires=['wmi'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Topic :: System :: Monitoring",
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: Microsoft :: Windows ",
	],
	python_requires='>=3.6',
	project_urls={
		'Getting Help': 'https://github.com/damies13/pyperfmon',
		'Source': 'https://github.com/damies13/pyperfmon',
	},
)
