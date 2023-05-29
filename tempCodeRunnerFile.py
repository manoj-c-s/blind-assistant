# def speak(command, langinp=LANGUAGE):
#     """
#     Text to Speech using GTTS

#     Args:
#         command (str): Text to speak
#         langinp (str, optional): Output language. Defaults to "en".
#     """
#     if langinp == "": langinp = "en"
#     tts = gTTS(text=command, lang=langinp)
#     tts.save("~tempfile01.mp3")
#     playsound("~tempfile01.mp3")
#     print(command)
#     os.remove("~tempfile01.mp3")