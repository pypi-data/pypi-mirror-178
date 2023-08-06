import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='El_Exelio',
	version="0.0.0.3",
	author="Nikita_Khalitov",
	author_email="nik1020031.nik@gmail.com",
	description="A simple module will allow you to create Excel spreadsheets.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/TheYoungEngineers/SulfTaper",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.8'
)
