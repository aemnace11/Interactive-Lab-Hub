# Ph-UI!!!

<details>
	<summary><strong>Instructions for Students (Click to Expand)</strong></summary>
  
	**Submission Cleanup Reminder:**
	- This README.md contains extra instructional text for guidance.
	- Before submitting, remove all instructional text and example prompts from this file.
	- You may delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
	- Your final submission should be neat, focused on your own work, and easy to read for grading.
  
	This helps ensure your README.md is clear, professional, and uniquely yours!
</details>

---

---

## Lab Overview
<<<<<<< HEAD
Team: <canvas group name>  
Members: Full Name (netid, github-handle), ...  
Project name: <name>
=======
Members: Achilles Emnace (aje77, aemnace11)
>>>>>>> 519de701552ea95d77ece886c4f4f2a8cee46249


For lab this week, we focus on both sensing and actuation, bringing new modes of input and output into your devices, while also prototyping the physical structure and overall look of the device. You will consider how the physical form supports sensing and actuation, and how these elements come together to shape the interaction and aesthetics of the device.

---

## Lab Structure

A) [Capacitive Sensing](#part-a)

B) [More Sensors](#part-b)

C) [Servo Actuation](#part-c)

D) [Physical Interaction Design: Feast Automata](#part-d)

E) [Build & Integrate](#part-e)

F) [Final Documentation](#part-f)

---

<<<<<<< HEAD
## Part 1 Lab Preparation

---

### Get the latest content:
As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 3 ways you can do so:


Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the personal access token for this.
```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2026
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab4 content"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

Option 3: (preferred) use the Github.com interface to update the changes.

---

### Quick Start: Python Environment Setup

1. **Create and activate a virtual environment in Lab 4:**
	```bash
	cd ~/Interactive-Lab-Hub/Lab\ 4
	python3 -m venv .venv
	source .venv/bin/activate
	```
2. **Install all Lab 4 requirements:**
	```bash
	pip install -r requirements2025.txt
	```
3. **Check CircuitPython Blinka installation:**
	```bash
	python blinkatest.py
	```
	If you see "Hello blinka!", your setup is correct. If not, follow the troubleshooting steps in the file or ask for help.

---

### Gathering materials for this lab:

* Cardboard (start collecting those shipping boxes!)
* Found objects and materials--like bananas and twigs.
* Cutting board
* Cutting tools
* Markers


(We do offer shared cutting board, cutting tools, and markers on the class cart during the lab, so do not worry if you don't have them!)

---

### Prototyping References 

* [What do prototypes prototype?](https://www.semanticscholar.org/paper/What-do-Prototypes-Prototype-Houde-Hill/30bc6125fab9d9b2d5854223aeea7900a218f149)
* [Paper prototyping](https://www.uxpin.com/studio/blog/paper-prototyping-the-practical-beginners-guide/) is used by UX designers to quickly develop interface ideas and run them by people before any programming occurs. 
* [Cardboard prototypes](https://www.youtube.com/watch?v=k_9Q-KDSb9o) help interactive product designers to work through additional issues, like how big something should be, how it could be carried, where it would sit. 
* [Tips to Cut, Fold, Mold and Papier-Mache Cardboard](https://makezine.com/2016/04/21/working-with-cardboard-tips-cut-fold-mold-papier-mache/) from Make Magazine.
* [Surprisingly complicated forms](https://www.pinterest.com/pin/50032245843343100/) can be built with paper, cardstock or cardboard.  The most advanced and challenging prototypes to prototype with paper are [cardboard mechanisms](https://www.pinterest.com/helgangchin/paper-mechanisms/) which move and change. 
* [Dyson Vacuum Cardboard Prototypes](http://media.dyson.com/downloads/JDF/JDF_Prim_poster05.pdf)
<p align="center"><img src="https://dysonthedesigner.weebly.com/uploads/2/6/3/9/26392736/427342_orig.jpg"  width="200" > </p>

### Feast Automata Inspirations

* [Simone Giertz - The Breakfast Machine](https://www.youtube.com/watch?v=E2evC2xTNWg) turns an everyday breakfast routine into a deliberately awkward robotic performance.
* [Pee-wee’s Big Adventure - Breakfast Machine](https://www.classhook.com/resources/1295-pee-wee-s-big-adventure-pee-wee-s-breakfast-machine?utm_source=chatgpt.com) An elaborate Rube Goldberg-style machine turns the ordinary routine of making breakfast into a playful mechanical performance.
* [Wallace & Gromit - The Autochef](https://www.google.com/search?sca_esv=66d2cd5ecf989ed9&sxsrf=APpeQnuwAWHrA3R0b1GeoQ4r-spKos3vUQ:1789367781228&udm=7&fbs=ABfTbFVyMZGZf1hfvX9uKjN_-G8cxpBkeIeqYwoCbfNVc4vKE7plZzta63Pe5DpJ3XFR9XzI_yj6fb6bfPt1x_5u3nRcG7tR9jg4Omd7-UnDuaw5i86wRQqe-045kPXObjb1eDS649ikhB0y_hSFYfNioDnA60A2i_oC1IzIZywb7ERnDQqnSx10JnfJEaAauzJXglx4123_vjf0_54bKrF6QjM9ne5i3g&q=Wallace+%26+Gromit+%E2%80%94+The+Autochef&sa=X&ved=2ahUKEwiI0OO3uu2WAxVHEFkFHQ3iAOEQtKgLegQIFRAB&biw=1197&bih=613&dpr=2.5#fpstate=ive&vld=cid:72c3eb07,vid:2igRcGxlshA,st:0)
* [Nik Ramage - Jelly Wobbler](http://www.youtube.com/watch?v=pj2t71q68sY#t=33) makes the simple act of wobbling jelly into a dedicated machine.
* [Zekun Chang - Blah Blah](https://zekunchang.com/portfolio/blah-blah/) is an alcohol machine that presents a playful commentary on drunken behavior.

### Mechanical Prototyping Resource

* [Gear Template Generator](https://woodgears.ca/gear_cutting/template.html) can help you prototype simple gear mechanisms for translating servo motion into physical movement.


---

### Part A
### Capacitive Sensing, a.k.a. Human-Twizzler Interaction 

We want to introduce you to the [capacitive sensor](https://learn.adafruit.com/adafruit-mpr121-gator) in your kit. It's one of the most flexible input devices we are able to provide. At boot, it measures the capacitance on each of the 12 contacts. Whenever that capacitance changes, it considers it a user touch. You can attach any conductive material. In your kit, you have copper tape that will work well, but don't limit yourself! In the example below, we use Twizzlers--you should pick your own objects.


<p float="left">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150" />
 
</p>

Plug in the capacitive sensor board with the QWIIC connector. Connect your Twizzlers with either the copper tape or the alligator clips (the clips work better). Install the latest requirements from your working virtual environment:

These Twizzlers are connected to pads 6 and 10. When you run the code and touch a Twizzler, the terminal will print out the following

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python cap_test.py 
Twizzler 10 touched!
Twizzler 6 touched!
```

---

### Part B
### More sensors

#### Light/Proximity/Gesture sensor (APDS-9960)

We here want you to get to know this awesome sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595). It is capable of sensing proximity, light (also RGB), and gesture! 
 
<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>
 

Connect it to your pi with Qwiic connector and try running the three example scripts individually to see what the sensor is capable of doing!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python proximity_test.py
...
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python gesture_test.py
...
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python color_test.py
...
```

You can go the the [Adafruit GitHub Page](https://github.com/adafruit/Adafruit_CircuitPython_APDS9960) to see more examples for this sensor!

#### Rotary Encoder 

A rotary encoder is an electro-mechanical device that converts the angular position to analog or digital output signals. The [Adafruit rotary encoder](https://www.adafruit.com/product/4991#technical-details) we ordered for you came pre-soldered, so you do NOT need to solder anything.
<p float="left">

   
<img src="https://cdn-shop.adafruit.com/970x728/377-02.jpg" height="200" />
<img src="https://cdn-shop.adafruit.com/970x728/4991-09.jpg" height="200">
</p>

Connect it to your pi with Qwiic connector and try running the example script, it comes with an additional button which might be useful for your design!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python encoder_test.py
```

You can go to the [Adafruit Learn Page](https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython) to learn more about the sensor! The sensor actually comes with an LED (neo pixel): Can you try lighting it up? 

#### Joystick 


A [joystick](https://www.sparkfun.com/products/15168) can be used to sense and report the input of the stick for it pivoting angle or direction. It also comes with a button input!

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/5/8/15168-SparkFun_Qwiic_Joystick-01.jpg" height="200" />
</p>

Connect it to your pi with Qwiic connector and try running the example script to see what it can do!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python joystick_test.py
```

You can go to the [SparkFun GitHub Page](https://github.com/sparkfun/Qwiic_Joystick_Py) to learn more about the sensor!

#### Distance Sensor


Earlier we have asked you to play with the proximity sensor, which is able to sense objects within a short distance. Here, we offer [Sparkfun Proximity Sensor Breakout](https://www.sparkfun.com/products/15177), With the ability to detect objects up to 20cm away.

<p float="left">
<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/9/2/15177-SparkFun_Proximity_Sensor_Breakout_-_20cm__VCNL4040__Qwiic_-01.jpg" height="200" />

</p>

Connect it to your pi with Qwiic connector and try running the example script to see how it works!

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 4 $ python qwiic_distance.py
```

You can go to the [SparkFun GitHub Page](https://github.com/sparkfun/Qwiic_Proximity_Py) to learn more about the sensor and see other examples

---

### Part C
### Servo Actuation

Now that you have explored several forms of sensing, add physical output by learning to control a servo motor. Complete the Servo pHAT setup and basic servo test before beginning your interaction design.

### Servo Control with SparkFun Servo pHAT
For this lab, you will use the **SparkFun Servo pHAT** to control a micro servo (such as the Miuzei MS18 or similar 9g servo). The Servo pHAT stacks directly on top of the Adafruit Mini PiTFT (135×240) display without pin conflicts:
- The Mini PiTFT uses SPI (GPIO22, 23, 24, 25) for display and buttons ([SPI pinout](https://pinout.xyz/pinout/spi)).
- The Servo pHAT uses I²C (GPIO2 & 3) for the PCA9685 servo driver ([I2C pinout](https://pinout.xyz/pinout/i2c)).
- Since SPI and I²C are separate buses, you can use both boards together.
**⚡ Power:**
- Plug a USB-C cable into the Servo pHAT to provide enough current for the servos. The Pi itself should still be powered by its own USB-C supply. Do NOT power servos from the Pi’s 5V rail.

<p align="center">
    <img src="Servo_pHAT.gif" alt="Servo pHAT Demo" width="400"/>
</p>

**Basic Python Example:**
We provide a simple example script: `Lab 4/pi_servo_hat_test.py` (requires the `pi_servo_hat` Python package).
Run the example:
```
python pi_servo_hat_test.py
```
For more details and advanced usage, see the [official SparkFun Servo pHAT documentation](https://learn.sparkfun.com/tutorials/pi-servo-phat-v2-hookup-guide/all#resources-and-going-further).
A servo motor is a rotary actuator that allows for precise control of angular position. The position is set by the width of an electrical pulse (PWM). You can read [this Adafruit guide](https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors/servo-motors) to learn more about how servos work.

---
=======
>>>>>>> 519de701552ea95d77ece886c4f4f2a8cee46249

### Part D
### Physical Interaction Design: Feast Automata

<img width="650" height="350" alt="Screenshot 2026-10-13 at 7 22 27 PM" src="https://github.com/user-attachments/assets/dbe97d58-4f67-4be2-8fe8-9baa79735889" />

Sketch #1: Questions raised about this are should the sensor sit in the base or ride on the figure, and if it does ride on the figure, will the cable twists every time it turns affect it? Also, will the figure’s own body shadow the sensor as it turns? That could set off a feedback loop where it turns, darkens its own sensor, and turns again. When physically prototyping, I have to see whether the height of the figure creates enough of a shadow regardless of the orientation of the light above. 

<img width="650" height="350" alt="Screenshot 2026-10-13 at 7 22 53 PM" src="https://github.com/user-attachments/assets/2614262e-6ba6-496e-a6af-51afb25c6982" />

Sketch #2: For this design, questions raised are how big does the torso have to be to hide a servo? And do the raised hands shade the hat sensor?

<img width="650" height="350" alt="Screenshot 2026-10-13 at 7 23 11 PM" src="https://github.com/user-attachments/assets/3fc2949d-1649-48b8-ba83-bc078ac5e1eb" />

Sketch #3: This design also makes me wonder about the shadow cast on the light sensor, especially if the raised menu blocks the sensor’s view of the ceiling. Ultimately, in the physical prototype of anything involved with a light sensor I have to see its sensitivity and if soft shadows will trigger it. 

<img width="650" height="350" alt="Screenshot 2026-10-13 at 7 23 41 PM" src="https://github.com/user-attachments/assets/da340d65-c161-4d20-a282-8f48e592c683" />

Sketch #4: Is there enough room for the arm with the curtain to swing up and not hit anything, how far does the curtain travel for a given arm length? Is the curtain too heavy for the arm connected to the servo? Would the vertical post be hollow inside? How will the servo motor stay up that high inside of the vertical post?

<img width="650" height="350" alt="Screenshot 2026-10-13 at 7 23 59 PM" src="https://github.com/user-attachments/assets/ef4f8463-a7e1-47cc-80d4-e59af9a722bd" />

Sketch #5: How tall does the wall have to be to be taller than the standard cup size? 

The design I choose to prototype is Sketch #1, named The Third Wheel 

The Third Wheel is a small figure who sits at the table during a romantic candlelit dinner and never got the hint that he wasn’t invited. Dimming the lights is one of the most familiar signals that a dinner has turned romantic, so I built the interaction around that moment. When the lights go down, he slowly turns his back on the couple, as if to say “I don't need to see this.” When the lights come back up, he turns around again and goes back to enjoying his meal / watching.

I chose this because I feel the interaction has good readability (since a whole-body turn is the clearest reaction from across a table), and because the sensor will stay still in the base while only the figure rotates, so the cable will never twist.


One thing I did observe in my rough prototype was that the figure does cast a shadow, so I attempted to place the sensor in the corner of the base so that it is not hit by the shadow in any part of the figure's rotation, since this 9g motor can only rotate 120 degrees max instead of the 180 my sketch imagined. 

<img width="3000" height="2250" alt="IMG_7104" src="https://github.com/user-attachments/assets/d9dc5b80-edd3-4859-8499-b9710f6394e7" />

<img width="1536" height="2048" alt="IMG_7105" src="https://github.com/user-attachments/assets/9c2d95bd-e536-4e6a-99ac-fc2bc664b4aa" />

<img width="1536" height="2048" alt="IMG_7103" src="https://github.com/user-attachments/assets/74d273af-15f1-4bed-a5f6-4eb3a1c61b13" />



Proof I was present in class for Part 1: I had to complete the 3d printer / laser cutter safety training with the TAs during part of lab time, and also received a servo motor which was only possible during lab period. 

---

## Part 2

Proof I was present in class for Part 2: I was able to get a new servo motor and materials from the cart, as well as the googly eyes that Professor provided. We didn't do anything in lab except for work on our labs. There was one group that developed a device that produced music (like a DJ) which they were playing around with in class. 


### Part E: Build and Integrate

The Third Wheel is a guy who shows up to your candlelit dinner and doesn't take the hint. He stands on a small base at the edge of the table. When the lights go down he turns his back on the couple, and he stays turned away until the lights are all the way back on. Every so often he can't help himself and slowly turns back around to look, then snaps away.

Hardware:

- APDS-9960 light sensor
- servo motor
- Raspberry Pi 5
- Separate USB-C power for the Pi and for the Servo pHAT

All code lives in [third_wheel](third_wheel/).

#### Interaction diagram



#### Photos and video



#### Iterations

1. Cardboard prototype. Out of my five sketches I went with the turntable. The figure stands directly on the servo horn and the sensor stays fixed in the base, so there's no linkage and nothing twists.
2. First version of the code. He turned away when the room got dark and turned back, with a pause halfway, once the light passed a middle threshold. I checked the logic against a simulated sensor before using the hardware to make sure a quick shadow or a light level sitting near the threshold wouldn't set him off.
3. Second version. I changed it so he stays turned away until the lights are fully back on and added the sneak peeks: a slow turn all the way around, a short stare, then a snap back. If the lights come back on during a peek he just stays facing the table.
4. Getting the servo running. The script ran but the servo didn't move. I went through three servos and two pHATs before realizing the servo was plugged into the Qwiic port instead of the channel 0 header, and the pHAT didn't have its own USB-C power. After fixing both it worked right away.
5. 3D printing. I replaced the cardboard with four printed parts (base, lid, turntable and figure), all printed flat without supports. The servo slot in the lid came out a little tight, so I shaved it down until the servo fit and its tabs sat on the ledge underneath. After that everything went together fine.

#### Reflection

The light sensor shaped the whole interaction. Room light changes for everyone at the table at once, so the response had to be slow and deliberate instead of twitchy. I average about 1.6 seconds of readings, so he reacts to the room changing and not to someone's hand passing over him.

Placement mattered more than I expected. The sensor sits on the lid behind the turntable, outside the area he sweeps through, so his body can't shade it while he turns. If it were under him, turning could drop the reading and trigger another turn. The servo's safe range is only 0 to 120 degrees, so I made the figure flat with a front and a back. Once he passes about 90 degrees you're looking at the back of his head, so 120 degrees reads as turned away. The candle also matters: putting it close to the sensor raises the dim reading and shrinks the gap between dim and bright, so I calibrate with the candle on.

For timing, there's a gap between the two thresholds. He turns away when the light drops about halfway from full to dim, and only turns back once it's 85% of the way back to full. That gap stops him from flipping back and forth. What makes it funny is the contrast in speed. He turns away fast, turns back slowly with a pause halfway, and on a sneak peek creeps around for about 5 seconds before snapping away instantly. The peeks happen at random times so you can't predict them. Speeding up the creep kills the suspense, and taking out the pause on the way back makes him look relieved instead of suspicious.

The hardest part was the hardware bring-up, which came down to the wrong connector and missing power. The printed slot being tight was the other lesson: printed holes come out smaller than designed, so next time I'd add more clearance. The most fun part was the sneak peek, since it turned a simple light trigger into something with a personality.

---

### Part F: Final Documentation

#### Looks like

A small pedestal that sits at the side of a dinner table. The base is a 100 x 100 mm rounded box with THE THIRD WHEEL engraved on the front like a nameplate. The figure is 106 mm tall, wearing a top hat, bow tie and buttoned jacket, with a shocked face engraved on the front. The back of his head is flat and drawn on, since that's what the couple sees when he turns away. The servo and wiring are hidden inside the base, the cables come out a notch in the back, and the light sensor sits in corner guides on the lid behind him.

3d-printed with glow-in-the-dark PLA at 0.2 mm layers, 15-20% infill, with no supports.

#### Works like

The sensor reads overall brightness every 0.2 seconds and the Pi averages the last 8 readings. When the average drops below the dark threshold, the servo turns him 120 degrees away, and he stays there until the average goes above the bright threshold. While he's turned away, a random 10 to 25 second timer triggers a sneak peek. During the peek he takes new readings; if the lights are fully on he stays facing the table, and if not he snaps back away. Every move is limited to the servo's safe range of 0 to 120 degrees.


#### Acts like

1. Dinner starts with the lights on. He faces the table and watches.
2. The couple dims the lights and lights the candle. About a second later he turns his back on them.
3. He stays turned away while they eat and talk.
4. Every 10 to 25 seconds he slowly turns all the way back around, stares for a second, and snaps away.
5. When the lights come all the way back up, he turns back slowly, pauses halfway, then faces the table again.
6. If the lights come back on in the middle of a peek, he doesn't snap away. He just stays there like nothing happened.

---

### User Testing

Setup: A couple's candelight dinner setting was simulated. The device sat at one end of a small dinner table with a candle in the middle and the testers sitting down. The room lights started on.

#### Tester 1

- Noticed the figure facing the table
- Turned the lights off with the candle still lit
- Figure turned away about a second later, tester laughed
- Kept watching and caught a full sneak peek, laughed again at the snap back
- Blew out the candle to see if the figure would react
- No change, figure stayed turned away

Feedback:

- Interaction was easy to follow and worked smoothly
- Blowing out the candle should do something
- Suggested the figure stop peeking and stay turned away until the lights come back on

#### Tester 2

- Didn't notice the figure at first
- Was looking at the candle when the lights dimmed, missed the first turn
- Caught a sneak peek halfway through about 15 seconds later
- Laughed at the snap back and said "wait, did he just look at us?"
- Raised the lights halfway to see what would happen, figure didn't turn back
- Assumed it was broken until the lights went all the way up and the figure turned around

Feedback:

- First turn away is easy to miss
- Raising the lights partway made it look broken
- Suggested a small plate with a fork and knife in front of the figure so it feels like he's eating with them, not just watching

#### Changes for the next version

- Lower threshold for the candle going out that stops the sneak peeks
- Small printed plate and utensils in front of the figure
- A reaction to the lights being raised partway
- A bit more clearance on the servo slot in the lid

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, into your lab 4 repository, and link them in your lab 4 readme.md.
* Link your Lab 4 readme.md in your main Interactive-Lab-Hub readme.md. 
* Labs are due on Mondays, make sure to submit your Lab 4 readme.md to Canvas.
