import os
from distutils.core import Command
from distutils.errors import DistutilsOptionError

class UploadSource(Command):
    """ Upload the resulting files from previous commands to s3. """

    description = ("Upload the resulting files from previous commands to s3. "
                   "This command uses two env variables: "
                   "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")

    user_options = [
        ("bucket=", "b", "S3 bucket"),
        ("folder=", "b", "folder in previously specified S3 bucket"),
        ("replace", None, "Replace existing files"),
    ]

    boolean_options = ["replace"]
	
    def initialize_options(self):
        self.bucket = None
        self.folder = None
        self.replace = False

    def finalize_options(self):
        if not self.bucket:
            raise DistutilsOptionError("No bucket provided.")
        self.replace = bool(self.replace)


    def run(self):
        # Importing boto at the module level will fail to install
        # this package and its dependencies corectly.
        import boto

        if not self.distribution.dist_files:
            raise DistutilsOptionError("No dist file created "
                                       "in earlier command.")
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(self.bucket, validate=False)
        for command, pyversion, filename in self.distribution.dist_files:
            base_filename = os.path.basename(filename)
            if self.folder:
                base_filename = '%s/%s' % (self.folder, base_filename)
            print 'Uploading %s to S3 %s' % (base_filename, self.bucket)
            key = bucket.new_key(base_filename)
            key.set_contents_from_filename(filename, replace=self.replace)
