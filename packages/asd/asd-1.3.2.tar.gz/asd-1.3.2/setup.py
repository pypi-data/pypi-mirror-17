from setuptools import setup, find_packages

setup(
    name = "asd",
    description = "Various command line helper scripts`",
    version = "1.3.2",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/asd.git',
    install_requires = [
        "argcomplete==1.0.0",
        "voidpp-tools==1.8.1",
    ],
    scripts = [
        'bin/asd',
    ],
    include_package_data = True,
    packages = find_packages(),
)
