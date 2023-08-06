from skbuild import setup

setup(
    name="nudisxs",
    version="1.0.2",
    author = "K.Kuzmin",
    maintainer = "Dmitry V.Naumov",
    maintainer_email = "dmitryvnaumov@gmail.com",
    description="A python interface to fortran code developed by K.Kuzmin, calculating neutrino-nucleon deep inelastic charged/neutral current cross-sections.",
    long_description_content_type="text/markdown",
    long_description="README.md",
    license="MIT",
    classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"],
    url = "https://git.jinr.ru/dnaumov/nudisxs",
    packages=['nudisxs','nudisxs/tests'],
    cmake_args=['-DSKBUILD=ON']
)
