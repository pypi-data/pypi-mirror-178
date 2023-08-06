import setuptools

longdesc = """# CatApi

random_cat() -> img: random cat

## class img

img.download(filename: str, encoding: str): download img

img.as_bytes(): get bytes from img

img.as_file(): get file from img

img.url: url to img
"""

setuptools.setup(
	name="wcatapi",
	version="1.0.2",
	author="WiSpace",
	author_email="wiforumit@gmail.com",
	description="CatApi",
	long_description=longdesc,
	long_description_content_type="text/markdown",
	url="https://api.wispace.ru/cat",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.10"
	],
	python_requires='>=3.6',
)