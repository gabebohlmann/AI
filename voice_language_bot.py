import openai
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
from google.cloud import texttospeech as tts 
import os

# should define as an env variable later
openai.api_key = "<OPENAI_API_KEY>" # replace with your API key

previousUserPrompt = ""
previousAgentResponse = ""

def listen():
    r = sr.Recognizer()

    # Set the energy threshold for recording to 4000
    r.energy_threshold = 4000

    # Set the length of silence that will register as the end of a phrase
    r.pause_threshold = 3.0  # Default value is 0.8
    with sr.Microphone() as source:
        print("Listening...")

        # Listen to the microphone, stop listening when silence is detected
        audio = r.listen(source, timeout=None)
        print("Finished listening.")
        with open("input.wav", "wb") as f:
            f.write(audio.get_wav_data())
            audio_file= open("input.wav", "rb")
    return audio_file

def ai_response(prompt, count): #, previousResponse):
    global previousUserPrompt
    global previousAgentResponse
    # if count == 0: # for future implementation, must seperate prompt 1 from the rest if you are using a prompt history
    messagesArray = [
                {"role": "system", "content": "You are having a conversation with an american user trying to learn spanish. The user's prompts will be in spanglish and your response should be in spanish and followed by an english translation. Any time the user uses english words, you should include a spanish translation of those words in your response."},
                {"role": "user", "content": "Hola, buenos dias. What is your name?"},
                {"role": "system", "content": "Hola, buenos dias. Me llamo assistant. ¿Como estas?| Hello, I'm good. My name is assistant. How are you? Correction: 'What is your name?' in spanish is '¿Como te llamas?'"},
                {"role": "user", "content": prompt},
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messagesArray
    )
    previousUserPrompt = prompt
    previousAgentResponse = completion["choices"][0]["message"]["content"]
    print(messagesArray)    
    return completion

def speak(text, filename):
    if text == None:
        return
    else:
        client = tts.TextToSpeechClient()
        synthesis_input = tts.SynthesisInput(text=text)
        if (filename == "spanish.mp3"):
            voice = tts.VoiceSelectionParams(
                language_code="es-US",
                name="es-US-Neural2-C", # this selects the voice
                ssml_gender=tts.SsmlVoiceGender.MALE,
            )
        elif (filename == "english.mp3"):
            voice = tts.VoiceSelectionParams(
                language_code="en-GB",
                name="en-GB-Neural2-D", # this selects the voice
                ssml_gender=tts.SsmlVoiceGender.MALE,
            )
        else:
            print("Error: filename must be either 'spanish.mp3' or 'english.mp3'")
            audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Write the response to the output file.
        with open(filename, "wb") as out:
            out.write(response.audio_content)

        # Convert mp3 file to wav                                                       
        audio = AudioSegment.from_mp3(filename)
        audio.export("temp.wav", format="wav")

        # Play the wav file
        wave_obj = sa.WaveObject.from_wave_file("temp.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing

        # Optional: remove temporary file
        os.remove("temp.wav")

def split_input(input_string):
    split_strings = input_string.split('|')
    return [s.strip() for s in split_strings]


def main():
    count = 0
    while True:
        audio_file = listen()
        print("Transcribing audio prompt...")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        prompt = transcription["text"]
        # prompt = "Hola, me llamo Gabriel. ¿Cómo te llamas?" #test, requires commenting out 119-122
        print("Prompt: " + prompt)
        print("Generating repsonse...")
        print("Count: " + str(count))
        full_response = ai_response(prompt, count)
        response_content = full_response["choices"][0]["message"]["content"]
        print(full_response)
        print(response_content)
        spanish, english = split_input(response_content)
        if spanish:
            speak(spanish, "spanish.mp3")
        if english:
            speak(english, "english.mp3")

        count += 1

if __name__ == "__main__":
    main()
