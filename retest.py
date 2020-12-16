import re

string='(代)健喬 氯絲菌素眼藥水0.25% 10ML/瓶(冷藏)<br>CHLORAMPHENICOL OPHTHALMIC SOLUTION 0.25% "SYNMOSA"  <font color="blue">冷藏貨件(不含常溫)滿3000元免運費 </font>&lt;'
after=re.sub('<br>.*','',string)
print(after)