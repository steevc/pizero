import scrollphat
import time
import sys

scrollphat.write_string(sys.argv[1] + "  ")
scrollphat.set_brightness(15)

while True:
  try:
    scrollphat.scroll()
    time.sleep(0.1)
  except KeyboardInterrupt:
    scrollphat.clear()
    sys.exit(-1)
