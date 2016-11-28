import getpass
import os

LOG_DIR='logs'
SECRET_KEY=os.urandom(24)

# Images created by this application are given this tag
IMAGE_TAG='bigjobbies:{}'.format(getpass.getuser())

# Images are taged based on their container name and given this prefix.
IMAGE_PREFIX='bigjobbiesworker'
