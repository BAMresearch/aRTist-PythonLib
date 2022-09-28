from setuptools import setup
import versioneer

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='artistlib',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='aRTist Python library',
      url='https://github.com/BAMresearch/aRTist-PythonLib',
      author='Carsten Bellon',
      author_email='Carsten.Bellon@bam.de',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='Apache 2.0',
      packages=['artistlib'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Natural Language :: English",
            "Topic :: Multimedia :: Graphics :: Graphics Conversion"
      ],
      zip_safe=False)
      