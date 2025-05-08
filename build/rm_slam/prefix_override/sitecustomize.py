import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jprl/APS1/APS1/jota_ws1/install/rm_slam'
