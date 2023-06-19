try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from screen1 import *
from screen2 import *
from screen3 import *
from screen4 import *
from screen5 import *
################################## 
# main
##################################
def main(): #From CS Academy
    runAppWithScreens(initialScreen='screen1',width = 1512,height = 840)

main() 