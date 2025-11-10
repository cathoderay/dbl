import time

session = f"{time.time()}"

DATABASE_PATH = f"/tmp/dbl.data-test-session-{session}"
COMPACT_PATH = f"/tmp/dbl.data.compact-test-session-{session}"
END_RECORD = "\x1E" # ASCII Record Separator
KEY_VALUE_SEPARATOR = "\x1D" # ASCII Group Separator
DEBUG = False
PROFILE = True
ENCODING = "utf-8"
DELETE_VALUE = "�"