import time

session = f"{time.time()}"

DATABASE_PATH = f"/tmp/dbl.data-test-session-{session}"
COMPACT_PATH = f"/tmp/dbl.compact-test-session-{session}"
END_RECORD = "\n"
END_RECORD_B = b"\n"
KEY_VALUE_SEPARATOR = ","
KEY_VALUE_SEPARATOR_B = b","
DEBUG = False
PROFILE = True
ENCODING = "utf-8"