import speech_recognition as sr
import pyaudio


def listen_for_command():
    """
    returns 1 or 2 or 3 or 4
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        hypothesis = recognizer.recognize_sphinx(audio)
        print("Recognized:", hypothesis)

        if "one" in hypothesis.lower():
            return 1
        if "two" in hypothesis.lower():
            return 2
        if "three" in hypothesis.lower():
            return 3
        if "four" in hypothesis.lower():
            return 4

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
