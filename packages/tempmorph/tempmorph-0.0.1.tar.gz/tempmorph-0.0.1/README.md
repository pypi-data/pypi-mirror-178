# TempMorph
![20221127_112246](https://user-images.githubusercontent.com/117014887/204119117-fa9f791f-705f-4c70-897d-7b468c95f6cc.png)
TempMorph is a Python package that helps you convert a temperature from one scale to another. This version currently works on Celcius, Fahrenheit, Kelvin, Reaumur, and Rankine.

# Usage

***Things to Note:***  
1 = Celcius  
2 = Fahrenheit  
3 = Kelvin  
4 = Reaumur  
5 = Rankine 

**Output = Float:**
```python
from tempmorph.conv import TempConv

# 30 is the value, 1 is Celcius (scale)
temp = TempConv(30, 1)

# Returns 87.6 (30 Celcius in Fahrenheit)
temp.fahrenheit()
```
  
  
**Output = String + Symbol:**  
```python
from tempmorph.conv import TempConv

temp_str = TempConv(373, 3)

temp_str.celcius(1)
#                ^
# By adding one as an argument, output will be '99.85 °C'
```
