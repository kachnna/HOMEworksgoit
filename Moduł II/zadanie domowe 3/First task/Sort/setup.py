from setuptools import setup

setup(name='clean_folder',
      version='1.0',
      description="Sorting program",
      packages=["clean_folder"],
      entry_points={'console_scripts': [
          "clean-folder = clean_folder.clean:main", ], },
      )
