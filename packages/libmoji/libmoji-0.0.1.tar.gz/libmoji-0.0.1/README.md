#libmoji
* Makes you hate variable character length
* Provides a list of emojis and their unicode values.
* Helps you distract how painstakingly slow your code is, with cool loading animations featuring emojis

###Example Usage
```python
import libmoji
from time import sleep
# Displays randomly chosen emojis along with a loading "animation" for ten seconds.
libmoji.load_moji(sleep,args=[10],frames=["LOADING.","LOADING..","LOADING..."])
```