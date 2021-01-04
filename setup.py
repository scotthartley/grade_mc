from setuptools import setup


def readme():
    with open("README.rst") as file:
        return file.read()


setup(name="grade_mc",
      version='1.1',
      description=("Process multiple choice grades."),
      long_description=readme(),
      author="Scott Hartley",
      author_email="scott.hartley@miamioh.edu",
      url="https://hartleygroup.org",
      license="MIT",
      packages=["grade_mc"],
      entry_points={
          'console_scripts': [
              'grade_mc = grade_mc:process_grades'
          ]
      },
      install_requires=["numpy"],
      python_requires=">=3",
      )
