from setuptools import setup

setup(
    name='s3sourceuploader',
    version='0.1.1',
    description=('Add an upload to s3 command to setuptools.'),
    keywords='setuptools s3 upload',
    author='Sever Banesiu',
    author_email='banesiu.sever@gmail.com',
    url='http://github.com/pbs/s3sourceuploader',
    license='BSD',
    py_modules=['s3sourceuploader'],
    install_requires = [ "boto", ],
    entry_points = {
        "distutils.commands": [ "s3upload = s3sourceuploader:UploadSource" ]
    }
)
