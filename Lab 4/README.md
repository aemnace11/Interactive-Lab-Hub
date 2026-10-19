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
Members: Achilles Emnace (aje77, aemnace11)


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

All code and stl files live in [third_wheel](third_wheel/).

#### Interaction diagram



#### Photos and video

<img width="4284" height="5712" alt="IMG_7147" src="https://github.com/user-attachments/assets/ee136fea-3412-44cc-83d6-ea9895006b1a" />

<img width="4284" height="5712" alt="IMG_7143" src="https://github.com/user-attachments/assets/301be6f7-a2fd-47ad-b3b1-d82214c5e887" />

#### Iterations

1. Cardboard prototype. Out of my five sketches I went with the turntable. The figure stands directly on the servo horn and the sensor stays fixed in the base, so there's no linkage and nothing twists.
2. First version of the code. He turned away when the room got dark and turned back, with a pause halfway, once the light passed a middle threshold. I checked the logic against a simulated sensor before using the hardware to make sure a quick shadow or a light level sitting near the threshold wouldn't set him off.
3. Second version. I changed it so he stays turned away until the lights are fully back on and added the sneak peeks: a slow turn all the way around, a short stare, then a snap back. If the lights come back on during a peek he just stays facing the table.
4. Getting the servo running. The script ran but the servo didn't move. I went through three servos and two pHATs before realizing the servo was plugged into the Qwiic port instead of the channel 0 header, and the pHAT didn't have its own USB-C power. After fixing both it worked right away.
5. 3D printing. I replaced the cardboard with four printed parts (base, lid, turntable and figure), all printed flat without supports. The servo slot in the lid came out a little tight, so I shaved it down until the servo fit and its tabs sat on the ledge underneath. After that everything went together fine.
   
   BONUS TIP: I made the 3d-printed prototype using glow-in-the-dark material!

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

- Was looking at the candle when the lights were dimmed, and missed the first sneak peek
- Caught the next sneak peek halfway through about 15 seconds later
- Laughed at the snap back and said "wait, did he just look at us?"
- Raised the lights halfway to see what would happen, figure didn't turn back
- Assumed it was broken until the lights went all the way up and the figure turned around

Feedback:

- First sneak peek is easy to miss, maybe add a sound during
- Raising the lights partway made it look broken
- Suggested a small plate with a fork and knife in front of the figure so it feels like he's eating with them, not just watching

#### Changes for the next version

- Lower threshold for the candle going out that stops the sneak peeks
- Small printed plate and utensils in front of the figure
- A reaction to the lights being raised partway
- A bit more clearance on the servo slot in the lid


