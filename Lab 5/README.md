# Observant Systems: Overnight Sensation

**Achilles Emnace**

For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

**New this year: the AI runs on the Pi.** Your Pi 5 can run an object detector ([YOLO](https://docs.ultralytics.com/)) and a small language model ([Qwen](https://ollama.com/library/qwen3.5) through [Ollama](https://ollama.com)) completely offline. In Part 1 you get both running and connect them: YOLO *sees*, Qwen *reasons* about what was seen. These models are slow, but they have all night. In Part 2 you use them to design a **night-time interaction**: what you tell the device before bed, what it does while you sleep, and what it shows you when you wake up.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Overview

**Part 1: the tools**

A) [Set up your Pi for on-device AI](#part-a)

B) [See: recognize people in real time with YOLO](#part-b)

C) [See more: hands and pose with MediaPipe](#part-c)

D) [Reason: run Qwen on the Pi with Ollama](#part-d)

E) [Connect: from YOLO readings to Qwen reasoning](#part-e)

**Part 2: Overnight Sensation**

F) [Read Part 2 and storyboard your night-time interaction](#part-f)

G) [Design the interaction before bed](#part-g)

H) [Incorporate the observant system during sleep](#part-h)

I) [Design the interaction when awake](#part-i)

The tools from earlier versions of this lab (MobileNet, Teachable Machine, Moondream, audio analysis, classic OpenCV) live in the [legacy folder](legacy/README.md). They are optional, but any of them can be the sensor in your Part 2 system.


## Prep for Part 1

Please check the instructions in [prep.md](prep.md) and complete them before lab. The installs in Part A take a while, so prep.md also tells you how to get a head start.

## The Report

This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

---

# Part 1

## Part A. 

\*\*\***Include a screenshot of `ollama list` showing your models, and the `bus.jpg` result and your own photo with their boxes.**\*\*\*

<img width="570" height="60" alt="Screenshot 2026-10-24 at 12 28 26 PM" src="https://github.com/user-attachments/assets/bbd19581-a532-4876-b957-fe678d0e6c61" />

<img width="544" height="516" alt="Screenshot 2026-10-24 at 12 02 19 PM" src="https://github.com/user-attachments/assets/071a7b0d-fc76-4270-b583-78fee46960d5" />

<img width="450" height="709" alt="Screenshot 2026-10-24 at 12 02 40 PM" src="https://github.com/user-attachments/assets/bbac649c-a977-4822-aa7e-23dbe8fa44ba" />



## Part B. 

\*\*\***Include a short video or screenshots of the person detection. Write down three situations where it did not see you, or saw a person who was not there, and what you think the cause was.**\*\*\*

Normal: 

<img width="548" height="481" alt="Screenshot 2026-10-25 at 12 21 05 PM" src="https://github.com/user-attachments/assets/66ce7b55-902b-4713-a822-7f2ab33f9bfd" />

<img width="550" height="479" alt="Screenshot 2026-10-25 at 12 20 25 PM" src="https://github.com/user-attachments/assets/98a126c9-3417-40b3-b1c0-7f4491a18675" />

<img width="549" height="477" alt="Screenshot 2026-10-25 at 12 19 54 PM" src="https://github.com/user-attachments/assets/af0c0f36-5dee-44ca-9970-3a6e016df92b" />

20% confidence:

<img width="548" height="481" alt="Screenshot 2026-10-25 at 12 23 29 PM" src="https://github.com/user-attachments/assets/65a30284-cdd8-4602-888b-56e65a51d35f" />

<img width="548" height="483" alt="Screenshot 2026-10-25 at 12 22 42 PM" src="https://github.com/user-attachments/assets/b6d0e28a-cf69-4fa3-98d0-f5bc99c27c1c" />

70% confidence: 

<img width="546" height="479" alt="Screenshot 2026-10-25 at 12 25 45 PM" src="https://github.com/user-attachments/assets/86ed3beb-61bc-4ce0-9356-c3f6c7ce43f9" />

<img width="545" height="480" alt="Screenshot 2026-10-25 at 12 26 11 PM" src="https://github.com/user-attachments/assets/25091b4f-6f79-45f1-9bb9-eb64dde71393" />

All classes: 

<img width="546" height="479" alt="Screenshot 2026-10-25 at 12 26 48 PM" src="https://github.com/user-attachments/assets/80a73235-e47a-46f0-b029-783303a59921" />

<img width="548" height="479" alt="Screenshot 2026-10-25 at 12 27 32 PM" src="https://github.com/user-attachments/assets/7d59958b-2f81-48c4-afa9-721571cff778" />

Headless: 

<img width="550" height="411" alt="Screenshot 2026-10-25 at 12 28 44 PM" src="https://github.com/user-attachments/assets/ee05abb0-68cd-4b1f-adbf-5ca02dd42936" />

The three runs where YOLO saw a person who wasn’t there (the default run, the --conf 0.2 run and the --headless run), the mistake was the same. It detected a person at about 30% confidence in a small corner of my light brown couch where a pillow was sitting. In the headless run it showed up as a printed “person” reading instead of a box, so the false positive doesn’t depend on the display. My guess is that the couch’s color is close to skin tone and the pillow’s rounded shape reads like a head or shoulder, so a small patch of the frame looks enough like part of a person sitting on the couch. Couches also show up next to people constantly in the COCO training images, so the model has probably learned to expect a person around couch-shaped objects. The detection never got much above 40%, so raising the threshold (like the --conf 0.7 run) filters it out, but at the cost of missing real people in harder poses or lighting.

## Part C. 

\*\*\***Include a screenshot or short video of the hand pose demo, and write how you might use face, hand or body pose tracking in your observant system.**\*\*\*

<img width="546" height="482" alt="Screenshot 2026-10-25 at 12 57 12 PM" src="https://github.com/user-attachments/assets/d57b4a8f-06c9-4f8f-8c84-f8706ac53cf2" />

<img width="544" height="479" alt="Screenshot 2026-10-25 at 12 57 32 PM" src="https://github.com/user-attachments/assets/d6526e66-011b-4531-b4a6-c97df7d07dd1" />

<img width="544" height="478" alt="Screenshot 2026-10-25 at 12 57 22 PM" src="https://github.com/user-attachments/assets/1c53d038-c771-46cb-8fa6-d4d4a545b3bc" />

For an observant system, I’d use hand tracking for the interaction with the device and body pose for the observation itself. A simple gesture like the Quiet Coyote or a thumbs up could work as a hands-free command, like telling the device to start or stop watching, which is useful when you don’t want to touch anything or talk to it. Body pose could go further than YOLO’s “a person is here” by describing what the person is doing, like whether they’re sitting, standing, lying down or reaching for something, by comparing the positions of the shoulders, hips and knees. Face tracking could tell whether someone is looking at the device, so it only responds when you’re actually paying attention to it. 

## Part D. 

\*\*\***Ask Qwen three questions a bedside device might need to answer. Paste the questions, the answers and how long each took. Try one of them with `qwen3:0.6b` and compare.**\*\*\*

Q: Here is a log from a bedside device: 23:40 person in bed. 02:15 nobody. 02:22 person in bed. 07:05 nobody. How long was the person out of bed during the night?
A: The person was out of bed for four hours, from 02:15 to 06:45.
Time it took: 26.3 s

Q: Here is a log from a bedside device: 00:10 person in bed. 03:30 nobody. 03:45 person in bed. 05:00 nobody. 05:20 person in bed. 08:00 nobody. How many times did the person get up during the night?
A: The person got up three times, once at 03:45 and again at 05:20.
Time it took: 4.1 s

Q: Here is a log from a bedside device: 22:50 person in bed. 06:30 nobody. What time did the person go to bed and what time did they wake up?
A: The person went to bed at 22:50 and woke up at 06:30.
Time it took: 3.4 s

Comparison with qwen3:0.6b (same as second question):
Q: Here is a log from a bedside device: 00:10 person in bed. 03:30 nobody. 03:45 person in bed. 05:00 nobody. 05:20 person in bed. 08:00 nobody. How many times did the person get up during the night?
A: The person got up 0 times during the night.
Time it took: 9.6 s

## Part E. 

\*\*\***Document the pipeline: at least three runs with the log, the question, Qwen's answer, and whether it was right. Include one case where Qwen got it wrong, and say what you changed in the interpreter and why.**\*\*\*

Run 1: walking through the frame

13:19:04 1 person(s) at center/close
13:19:06 nobody
13:19:13 1 person(s) at right/far
13:19:13 1 person(s) at center/far
13:19:14 1 person(s) at left/close
13:19:15 nobody
13:19:22 1 person(s) at left/far
13:19:23 1 person(s) at left/close
13:19:24 1 person(s) at center/close

Qwen (22.0 s): “There were four distinct individuals present throughout the 26-second observation period. They moved around the room: one person remained stationary on the left side, while others shifted between the center and right areas of the room...”

What actually happened: I started in the frame, left, walked across from right to left, then came back in. The log captured this well. You can follow me leaving, crossing and returning from the readings alone. The mistake was Qwen’s. It treated each change in reading as a different person and reported four people when there was only one. The interpreter only says “1 person(s)” per reading and never says it’s the same person as before, so the model filled that gap with a wrong guess.

Run 2: an empty room

13:21:32 nobody

Qwen (8.9 s): “The log indicates that no one was present in the room during this 15-second observation period. There were no people visible or recorded, and no activity occurred to change the reading...”

This was correct. I stayed out of frame the whole time, the log had a single nobody line, and Qwen didn’t invent any events. For an overnight device, it matters that it can report a night where nothing happened without making something up.

Run 3: trying to confuse it

13:23:46 nobody
13:23:54 1 person(s) at left/far
13:24:00 nobody
13:24:00 1 person(s) at left/far
13:24:02 nobody
13:24:07 1 person(s) at left/close
13:24:08 1 person(s) at center/close
13:24:08 nobody
13:24:09 1 person(s) at right/close
13:24:10 1 person(s) at center/close
13:24:10 1 person(s) at center/far
13:24:11 1 person(s) at center/close
13:24:11 1 person(s) at left/close
13:24:13 1 person(s) at left/far

Qwen (12.2 s): “There are 4 distinct people visible in the room throughout the 30-second period. They are all located near the edges of the room (left or right) and appear to be standing still...”

Both stages failed here. When I sat down in a chair and turned my back to the camera, YOLO lost me and logged nobody even though I was still in the room. When I put a water bottle in the frame, YOLO detected it as a person. The readings also flickered, sometimes switching between nobody and a person within the same second. Qwen again counted four people and described them as standing still, which matched neither the log nor reality.

---

# Lab 5 Part 2: Overnight Sensation

For Part 2, you will use the observant system from Part 1 to design a night-time interaction. On-device AI is slow, so let it work while you sleep. The person meets the device twice: **before bed**, when they hand the night over, and **when awake**, when the device gives something back. In between, the pipeline from Part E runs on its own.

Two flavors, pick one or mix them:

* **Sense all night.** The Pi watches, listens or measures from bedtime until morning and keeps a log.
* **Process all night.** You already have the data (a day of phone photos, a long recording) and the Pi needs hours to get through it.

Two house rules. Sample rather than stream: one look every 5 to 30 seconds is plenty, and it keeps the Pi cool. And keep everything on the Pi: tell the people you live with, point the camera at things rather than at beds, and delete the snapshots after the demo.

## Part F. 
### Read Part 2 and storyboard your night-time interaction

Storyboard a night-time interaction built on your observant system, in three panels:

1. **Before bed.** How does the person hand the night over, and how does the device acknowledge it?
2. **While asleep.** What does the device watch or work through?
3. **When awake.** What is the one thing the person learns, and in what medium?

Stuck? A kitchen that tells you who raided the fridge. A desk that reports whether you actually went to bed. A window that names the quietest hour. A plant that describes its night. Find something better.

Use storyboards and/or [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf).

\*\*\***Insert ideas, sketches, Verplank diagrams and storyboards for your night-time interaction here.**\*\*\*

## Prep for Part 2

1. Look at and give feedback on the Part F storyboards.
   **Put the feedback for your ideas here.**
2. [Update your Lab Hub](prep.md#get-the-latest-content) to get the latest content for Part 2.
3. Decide where the device will spend the night and who else lives there. Get their OK before the first run.
4. Revise your storyboard with the feedback and with what you learned in Part E about where the pipeline breaks.

\*\*\***Post your revised storyboard here.**\*\*\*

## Part G. 
### Design the interaction before bed

The hand-off: the person tells the device what to watch tonight, and the device acknowledges it. Keep it to a thirty-second ritual. A button or a touch (Lab 4), a spoken sentence (Lab 3), a wave or a Quiet Coyote at the camera (Part C). The acknowledgement can be a line on the display, a tone, or an LED that dims rather than lights up. At its simplest, the hand-off just sets the question that the morning will answer.

\*\*\***Describe the bedtime interaction and include a short video of someone handing the night over to the device.**\*\*\*

## Part H. 
### Incorporate the observant system during sleep

The Part E pipeline becomes the night shift. `overnight.py` runs your `interpret()` from `yolo_to_qwen.py` every few seconds, people only unless you pass `--all`, and writes the readings to `night_log.jsonl`; the reasoning waits for the morning. Start it inside `tmux` so it keeps running after you close your laptop, and stop it with Ctrl-C in the morning:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ tmux new -s night
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python overnight.py
```

Fake a night first: run it for thirty seconds while you walk around, stop it, and run `morning.py` from Part I. When that looks right, run a real night. If your storyboard needs a sensor rather than the camera, swap in the Lab 4 example code and log its reading the same way.

\*\*\***Run the system for at least one real night. Include the log (or an excerpt) and a few sentences on what broke or surprised you.**\*\*\*

## Part I. 
### Design the interaction when awake

The reveal. The night produced a log; the morning turns it into something a half-awake person can take in. `morning.py` is the smallest version: it asks Qwen for a three-sentence report.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python morning.py
```

Make it yours: show the report on the Mini PiTFT, read it aloud with Piper from Lab 3, plot the night as a timeline, or ask for JSON (`--json`, Part D) and move a servo. Whatever you pick, make sure it is honest about a night in which nothing happened.

## Final documentation

Document all the prototypes and iterations you have designed and worked on. The deliverables for this lab are writings, sketches, photos, and videos that show what your system:

* "Looks like": how the device sits in the room at night, and what it looks like at bedtime and in the morning.
* "Works like": the pipeline from detector to interpreter to log to reasoner, with a real night's data.
* "Acts like": how a person hands the night over and what they get back.

\*\*\***Include a short video of the whole system: the bedtime hand-off, a log excerpt or timelapse of the night, and the morning reveal from a real overnight run.**\*\*\*

As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page.

## Deliverables & Submission for Lab 5

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, including your code and night log, into your Lab 5 repository, and link them in your Lab 5 readme.md.
* Link your Lab 5 readme.md in your main Interactive-Lab-Hub readme.md.
* Labs are due on Mondays, make sure to submit your Lab 5 readme.md to Canvas.

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
