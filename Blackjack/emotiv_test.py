print "test"
import emotiv
import gevent
import sys
import os

# import usb.core
# import usb.util
# import sys
# 
# 
import usb.core 
dev = usb.core.find(find_all=True, idVendor=0x21A1) 
print dev
#if dev is None: raise ValueError('Our device is not connected') 
#else: raise ValueError("It Works!")
# 
# import libusbx
# int libusb_init
# 
#    
# import platform 
# platform = platform.system() 
# print platform

#os.system('./Users/admin/SERVER2/BD_Scripts/GitLibrary.git/hidapi/hidtest/hidtest')


if __name__ == "__main__":
  headset = emotiv.Emotiv()    
  gevent.spawn(headset.setup)
  gevent.sleep(1)
  try:
    while True:
      packet = headset.dequeue()
      print packet.gyroX, packet.gyroY
      gevent.sleep(0)
  except KeyboardInterrupt:
    headset.close()
  finally:
    headset.close()