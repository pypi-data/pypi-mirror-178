from distutils.core import setup

setup(name='building_energy_storage_simulation',
      version='0.3',
      description='A simulation of a building to optimize energy storage utilization.',
      author='Tobias Rohrer',
      author_email='tobias.rohrer@outlook.com',
      # Required to include profiles which are stored as .csv files
      include_package_data=True,
      package_data={
          "building_energy_storage_simulation": [
              "building_energy_storage_simulation/data/preprocessed/*.csv",
          ]
      },
      # Use `packages` argument to tell distutils where the python modules are located.
      # See https://docs.python.org/3/distutils/setupscript.html#listing-whole-packages for more details.
      packages=['building_energy_storage_simulation'],
      # Use `install_requires` to specify the dependencies which are required in order to run the package.
      # See https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/ for a differentiation
      # to the `requirements.txt`.
      install_requires=[
          "gymnasium",
          "pandas",
          "numpy"
      ],
      extras_require={
          "docs": [
              "sphinx"
          ],
          "tests": [
              "pytest"
          ],
          "example":
          [
              "stable-baselines3"
          ]
      }
      )
