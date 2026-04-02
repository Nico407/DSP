# DSP Project

# Project work for "Desining Software as Product"

This Project contains a road map which may exceed the given time frame by the module.

For further insight open roadmap.md

## How to test:
requirements.txt <--

in terminal launch:
uvicorn main:app --reload

open browser with url:
http://127.0.0.1:8000/docs


![alt text](image.png)

click POST/ calculate
on the right hand side click: Try it out

![alt text](image-1.png)

adjust values
for activit level:
        "1"      #sedentary
        "2"      #light
        "3"      #moderate
        "4"      #active
        "5"      #extreme

for goal:
# gain          +0.5 kg / w
# mild gain     +0.25 kg / w
# maintain      
# mild loss     -0.25 kg / w
# loss          -0.5 kg / w