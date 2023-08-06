import setuptools
import subprocess
import os

print("[setup.py][001]")

cf_remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

print(f"[setup.py][002][cf_remote_version][{cf_remote_version}]")

if "-" in cf_remote_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = cf_remote_version.split("-")
    cf_remote_version = v + "+" + i + ".git." + s

assert "-" not in cf_remote_version
assert "." in cf_remote_version

assert os.path.isfile("cf_remote_x/version.py")
with open("cf_remote_x/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % cf_remote_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cf-remote-x",
    version=cf_remote_version,
    author="Northern.tech, Inc.",
    author_email="contact@northern.tech",
    description="Tooling to deploy CFEngine (and much more)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JosephInsoundz/cf-remote",
    packages=setuptools.find_packages(),
    package_data={"cf_remote_x": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["cf-remote = cf_remote_x.main:main"]},
    install_requires=[
        "requests >= 2.25.1",
        "apache-libcloud >= 3.3.1",
    ],
)

print(f"[setup.py][003][cf_remote_version][{cf_remote_version}]")
