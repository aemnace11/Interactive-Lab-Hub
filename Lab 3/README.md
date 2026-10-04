# Chatterboxes

Achilles Emnace 


# Part 1

## A. Text to Speech

My own shell file is in greeting_demo.sh.

The greeting is not the same in different voices. In my file, I have a monotone American male (en_US-joe-medium) greeting vs a bright British female (en_GB-semaine-medium) greeting, and the way that I receive the two are completely different even though it is the same sentence. I feel much more welcomed by the tone and utterance of the female greeting, while the American male makes me feel as if he is greeting me indifferently. 

## B. Speech to Text

Sentence I said: "Who is the best soccer player ever, Messi or Ronaldo?"

tiny.en: 0.22x, transcription: "Who is the best soccer player ever, Messi or Ronaldo?" 

base.en: 0.45x, transcription: "Who is the best soccer player ever? Messi Orinaldo?"

small.en: 1.21x, transcription: "Who is the best soccer player ever, Messi or Ronaldo?"

medium.en: 3.28x, transcription: "Who is the best soccer player ever, Messi or Ronaldo?"

Accuracy can't be judged here, because a single sentence where tiny.en was already perfect and base.en did worse than tiny.en is too inconsistent to show any trend. On latency, though, the cutoff is clear: small.en and medium.en run slower than real time (real-time factor > 1), so for a system that has to answer you, extra accuracy stops being worth it past base.en, and tiny.en is the practical pick.

My own code for testing numerical input is in ask_zipcode.py.

## C. Turn-taking: knowing when someone has stopped talking

At 0.2s, if you take any pause to think of a word, or saying a sentence with small break(s) between such as a phone number or list of things, then your speech will get cut off. If feels as if you are talking to someone who interrupts you whenever you pause when talking. At 1.5s however, the pause is too long and it feels like you are talking to a robot or someone who's on the end of a bad phone connection line. I felt like I could feel the compute and comprehend time for the listener to process what I had said. Trying 0.8s which was in the middle of the 2 extremes seemed to fit the best for a normal conversation flow and not cut me off too harshly. 

## D. Storyboard

<img width="1206" height="497" alt="corporate_translator" src="https://github.com/user-attachments/assets/368721c0-581f-4f0c-a6bc-1b206edcc8b3" />
Script included in this storyboard diagram of an example interaction.


## E. Acting out the dialogue

https://github.com/user-attachments/assets/2ffc9c35-733b-40de-a3df-c807988ec33c

The dialogue went pretty much how I imagined, because the questions were framed in a way that there are only a few possible answer choices. The device is forcing the user down 1 out of 3 interaction paths through the question format. However, when the test interaction was acted out, there was a moment when the user was a bit confused or delayed in processing the first instance of "Would you like to hear that again, try another, or are you done?", which may not have been caught by the listening duration that was established. This may cause me to extend the listening length in the final implementation. 

---

# Lab 3 Part 2

## Prep for Part 2

**1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings.**

- **Timing:** In Part 1, the tester hesitated at the first "hear it again, try another, or are you done?" question, and a fixed listening window could miss that. I'll give users up to 10 seconds to start talking, and end their turn after 1.2s of silence instead of recording for a set length. Part 1 showed 0.8s worked best for normal conversation. Translation needs full sentences, though, and people pause while figuring out what to say, so I'm going a little longer.
- **Wording:** I'll keep the follow-up question listing exactly three options so users know what they can say. The device should also accept natural variations like "repeat that," "next one," "that's all," or "I'm not done."
- **Misunderstandings:** If the device doesn't recognize a response, it will say "Sorry I didn't understand that, please say it again." and listen again, instead of repeating the whole question. It should also catch common transcription mistakes, like "here it again" or "try and other."
- **Switching personas:** In Part 1, there was no way to change persona mid-session. Users should be able to switch at any time. If they switch and then say "hear it again," they'll hear the same sentence in the new persona.

**2. What are other modes of interaction beyond speech that you might also use to clarify how to interact? In particular: how does someone know when the device is listening, and when it is thinking? You have a screen and an LED.**

- **Listening:** The green LED turns on only while the device is listening, and turns off as soon as the user is done talking.
- **Thinking:** The screen shows the current persona in large text, with a small status line underneath ("Listening...", "Transcribing...", "Translating...") so users know the device is working and not frozen.
- **Persona:** A small hint at the top of the screen ("press button to switch") tells users how to change personas without the device having to explain it out loud.

**3. Make a new storyboard, diagram and/or script based on these reflections.**

*[Screen: white background, "Corporate" in the middle, "press button to switch" at the top]*

- **Device:** "Please say what you would like to be translated." *[LED on, screen: "Listening..."]*
- **User:** "I didn't read your email and I'm not going to."
- *[1.2s of silence → LED off, screen: "Transcribing..." → "Translating..."]*
- **Device:** "I haven't had the bandwidth to review your email yet, so I'll need to deprioritize it for now."
- **Device:** "Want to hear that again, try another, or are you done?" *[LED on]*
- **User:** "Um... what?"
- **Device:** "Sorry I didn't understand that, please say it again." *[LED on]*
- **User:** *[presses button, screen switches to "Yoda"]* "Hear it again."
- **Device:** "Read your email, I did not. Going to, I am not."
- **Device:** "Want to hear that again, try another, or are you done?"
- **User:** "Try another."
- **Device:** "Please say what you would like to be translated."
- **User:** "I ate the whole pizza by myself and I regret nothing."
- **Device:** "The whole pizza, eaten by myself I have. Regret nothing, I do. Hmm."
- **Device:** "Want to hear that again, try another, or are you done?"
- **User:** "I'm done."
- **Device:** "Goodbye!" *[LED off, screen off]*

**4. (optional) Integrate input devices in the system**

I am going to integrate a joystick or button as an input device to allow the user to switch between personas.


## Prototype your system

The Corporate Translator takes a plain English sentence and says it back in one of two personas: **Corporate** (sugar-coated business jargon) or **Yoda** (Yoda's backwards sentence structure). Everything runs locally on the Pi.

**Hardware:** Raspberry Pi 5, USB mic, USB speaker, Adafruit Mini PiTFT, SparkFun Qwiic Button (green LED)

**How it works:**
1. The screen shows the current persona. Pressing the button switches personas at any time.
2. The device asks "Please say what you would like to be translated." and the button's green LED turns on to show it's listening.
3. After 1.2s of silence, the LED turns off and the screen shows "Transcribing..." then "Translating..."
4. The device says the translation, then asks "Want to hear that again, try another, or are you done?"
5. "Hear it again" replays the translation (in the new persona if you switched), "try another" starts over, and "done" ends the session. Anything else gets "Sorry I didn't understand that, please say it again."

**Under the hood:**
- Silero VAD detects when the user stops talking (same setup as `echo_bot.py`)
- faster-whisper (`tiny.en`) transcribes speech
- Ollama (`qwen2.5:1.5b`) translates using a short prompt and examples for each persona
- Piper (`en_US-joe-medium`) speaks the response
- The follow-up command matching also catches common mishearings (e.g. "try and other" → try another)

**Changes from Part 1:**
- Added the LED and on-screen status so users can tell when the device is listening vs. thinking
- Extended the listening window to 10s, since a tester hesitated at the follow-up question in Part 1
- Accepts variations of the commands ("repeat that", "next one", "that's all")
- Originally planned to use a joystick to switch personas, but the board wasn't detected over I2C, so I switched to the button

**Running it:**
```
python corporate_translator.py
```

Interaction Video: 


https://github.com/user-attachments/assets/6d90e352-41f6-40d1-b1ee-4ccff86e23a0



Controller Video: 

https://github.com/user-attachments/assets/d6a95aaa-3581-44a8-a632-67360d52b635


## Test the system

My system is fully autonomous, so I didn't need a wizard during testing. The interaction was designed to be predictable from the start, and an LLM running locally through Ollama could handle the translation, so there was nothing a human needed to fake. Two people tested the device without any instructions besides "talk to it."

### What worked well about the system and what didn't?

**Worked well:**
- The LED and on-screen status made it clear when to talk and when to wait. Nobody tried to talk while the device was translating.
- The 1.2s silence cutoff felt natural, and testers weren't cut off mid-sentence.
- Switching personas with the button was easy, and hearing the same sentence in both personas got the best reactions.
- The "Sorry I didn't understand that" recovery kept the conversation going instead of breaking it.

**Didn't work well:**
- There was a noticeable wait while the LLM generated the translation, which made the device feel slow at times.
- Both personas use the same Piper voice, so Corporate and Yoda don't sound as different as they could.
- Transcription and translation accuracy were the biggest problems (see below).

### What worked well about the controller and what didn't?

Since there was no wizard, my "controller" was the terminal running the script, which logged what the device heard, the persona, the translation, and which command it matched.

**Worked well:** The log made it easy to see exactly where an interaction went wrong, whether it was the speech recognition, the translation, or the command matching.

**Didn't work well:** The transcriptions weren't accurate most of the time. Whisper `tiny.en` often misheard words, especially with fast speech or background noise, and a wrong transcription meant a wrong translation. The translations themselves were also often inaccurate. The small model (`qwen2.5:1.5b`) sometimes changed the meaning of the sentence, and the Yoda translations didn't always flip the word order. I picked both models for speed on the Pi, but the trade-off was accuracy.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

In Part 1, when I acted as the device, I understood every sentence perfectly and could translate it however I wanted. The autonomous version showed that the hardest part of replacing the wizard isn't the dialogue flow, it's the understanding. Things I'd change:
- Use a bigger speech model like `base.en`, even though it's slower
- Show the transcription on screen so users can see what the device heard and retry if it's wrong
- Use a larger LLM, or give it more examples per persona, to keep translations closer to the original meaning

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

The device could log every interaction: the audio, the transcription, the persona, the translation, the command chosen, and timing data like how long users took to start talking. Saying "hear it again" or getting a "Sorry" would be useful signals of where things went wrong. I could also have users press the button to rate translations they liked.

For other sensing modalities, a proximity sensor could detect when someone walks up and start the interaction automatically instead of needing the user to start the script manually. 

## Proof I attended lab

During the lab period, I picked up the additional USB microphone that wasn't included in my kit. I also had a brief conversation with Professor Wendy about the Talking Angela app, and whether a speech-enabled interaction should be started by the user or by the device.

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
