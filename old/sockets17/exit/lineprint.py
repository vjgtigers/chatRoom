import sys
import time
for i in range(10):
    print("Loading" + "." * i)
    sys.stdout.write("\033[F") # Cursor up one line
    sys.stdout.write("\033[K") # Clear to the end of line
    time.sleep(1)

#sys.stdout.write("\033[K") # Clear to the end of line
  