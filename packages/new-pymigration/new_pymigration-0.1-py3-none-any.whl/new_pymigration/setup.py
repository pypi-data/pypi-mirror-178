from setuptools import setup, find_packages

setup(
    name='new_pymigration',
    version='0.1',  # PyPI에 올릴 version
    description='pymicration whl test',  # 짦은 소개
    author='haneul.park',  # 이름
    author_email='haneul.park@aurostech.com',  # 메일
    py_modules=["pymigration", "pyConverterUI", "cleasing", "Auros"],  # 패키지 사용시 필요한 모듈
    packages=['new_pymigration'],
    python_requires='>=3.6',  # python 필요 버전
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)