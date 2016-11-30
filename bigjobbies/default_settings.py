import os
import platform
import socket

from bigjobbies.pin import generate_pin

# Relative to instance_path
LOG_DIR='logs'

SECRET_KEY=os.urandom(24)

# PIN to authenticate user
AUTH_PIN=generate_pin()
print("*** AUTHORISATION PIN: {} ***".format(AUTH_PIN))

# URL and filesystem-safe prefix for temporary files, etc.
APP_PREFIX='bigjobbies'

SITE_NAME=platform.uname()[1]

# "Namespace" which container labels used by this application live in. This
# should be a "reverse DNS" style name WHICH ENDS IN A FULL STOP
LABEL_NS='.'.join(socket.getfqdn().split('.')[::-1] + [APP_PREFIX])+'.'
