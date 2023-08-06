import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TANGO_Py",
    version="0.1",
    author="Jean Ollion",
    author_email="jean.ollion@polytechnique.org",
    description="Tools for Analysis of Nuclear Genome Organization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ARChE-MNHN/PyTANGO.git",
    download_url = 'https://github.com/ARChE-MNHN/PyTANGO/archive/v_01.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
    ],
    keywords = ['bacmman', 'pandas', 'data analysis', 'TANGO', 'micorscopy', 'nuclear organization'],
    python_requires='>=3',
    install_requires=['numpy', 'pandas', 'matplotlib', 'h5py']
)
