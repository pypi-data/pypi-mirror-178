import setuptools
setuptools.setup(
    name='ClosedPhotogrammetry',
    version='1.1',
    description='Given the external elements, focal length, and spatial point coordinates, pixel coordinates are generated, which we call reverse forward intersection.the least_square functon for similarity transformation, the Inv_Resection for computing pixel coordinates.',
    author='Zhang',
    author_email='',
    license='MIT',
    keywords='resection,transformation',
    packages=setuptools.find_packages(),
	include_package_data=True,
    install_requires=['numpy>=1.14'],
    python_requires='>=3.4'
   )