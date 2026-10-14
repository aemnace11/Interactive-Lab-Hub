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


### Part E

#### Build & Integrate: Sensing + Actuation

For Part 2, build the Feast Automata interaction you developed in Part D by connecting sensing/input to physical actuation.

**Your prototype should:**
- Use at least one sensing or input device.
- Use servo-based physical actuation.
- Connect sensing and actuation into a meaningful interaction around eating, drinking, cooking, serving, or sharing food.
- Additional inputs, displays, LEDs, buttons, or other outputs are optional extensions.

**Document your system with:**
- Code for your sensing + actuation prototype
- Photos and/or video of the working prototype in action
- A simple interaction diagram or sketch showing how sensing and actuation are connected
- Written reflection: What did you learn about connecting sensing, movement, and physical form? What was fun, surprising, or challenging?

**Questions to consider:**
- How does your chosen sensor or input shape the physical response?
- How does the physical arrangement of the sensor and actuator change the interaction?
- What thresholds, timing, or movement patterns make the interaction feel clear or playful?
- What changes when you adjust the sensor placement or servo motion?

Iterate on the sensing, movement, and physical form, and document what you discover.

### Part F

### Final Documentation

Document all the prototypes and iterations you have designed and worked on! Again, deliverables for this lab are writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do
* "Acts like": shows how a person would interact with the device

---

## Deliverables \& Submission for Lab 4

The deliverables for this lab are, writings, sketches, photos, and videos that show what your prototype:
* "Looks like": shows how the device should look, feel, sit, weigh, etc.
* "Works like": shows what the device can do.
* "Acts like": shows how a person would interact with the device.

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, into your lab 4 repository, and link them in your lab 4 readme.md.
* Link your Lab 4 readme.md in your main Interactive-Lab-Hub readme.md. 
* Labs are due on Mondays, make sure to submit your Lab 4 readme.md to Canvas.
