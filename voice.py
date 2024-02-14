import speech_recognition as sr
import pyaudio


def listen_for_command():
    """
    returns 1 or 2 or 3 or 4
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for a command...")
        audio = recognizer.listen(source)

    try:
        hypothesis = recognizer.recognize_sphinx(audio)
        print("Recognized:", hypothesis)

        # Check for the specific word
        if "one" in hypothesis.lower():
            print("Output: 1")

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
