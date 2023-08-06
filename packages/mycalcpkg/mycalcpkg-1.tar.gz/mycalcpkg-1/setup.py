import setuptools

f = open('README.txt', 'r')
r = f.read()

setuptools.setup(
    name="mycalcpkg", # Name Of Package
    author="<name>", # Your Name
    packages=setuptools.find_packages(),
    description="A Super Fun Package For Adding & Subtracting.",
    long_description=r,
    script_name="mycalcpkg",
    version='1' # almost forgot
)

# now we wait (again..)
