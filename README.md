# House monitoring project

This projects aims to collect and to monitor a few datas in the house.
In the future, I would like to see if I can predict some value. For instance, I could predict the electricity cost given the temperature.

main.py:
- Measure and collect the temperature in 3 places (2 indoor, 1 outdoor) through Raspberry Pi
- Collect electricity consumption through ConsoAPI, a public API that allow to access ENEDIS datas (French electricity distributors)

app.py
- Monitor the temperature for a given date range with dash an plotly librairies


Miscallenous:
Personnal datas are not shared on my GitHub, only the code I use and/or wrote.

![Alt text](view/Capture d’écran app.py 1.png?raw=true "Screensht from app.py")
![Alt text](view/Capture d’écran app.py 2.png?raw=true "Screensht from app.py")