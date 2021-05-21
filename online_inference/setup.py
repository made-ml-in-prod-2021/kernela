from setuptools import setup
from setuptools import find_packages

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    reqs = list(map(str.strip, req_file.readlines()))

setup(name="hear_diss_app",
      description="Simple web app on FastAPI.",
      version="0.0.1",
      url="https://github.com/made-ml-in-prod-2021/kernela",
      author="KernelA",
      author_email="None",
      license="MIT",
      packages=find_packages(),
      python_requires=">=3.7",
      install_requires=reqs
      )
