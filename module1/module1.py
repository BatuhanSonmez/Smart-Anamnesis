import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def convert_audio_to_text(audio_file):
    # Load audio file
    try:
        sound = AudioSegment.from_file(audio_file)
    except CouldntDecodeError:
        return "Error: Audio file format not supported"

    # Export audio data to raw PCM format (signed 16-bit PCM format)
    raw_audio_data = sound.raw_data
    sample_width = sound.sample_width
    frame_rate = sound.frame_rate
    channels = sound.channels

    # Use SpeechRecognition library to perform speech-to-text
    recognizer = sr.Recognizer()

    # Create an AudioData object from raw audio data
    audio_data = sr.AudioData(raw_audio_data, sample_width=sample_width, sample_rate=frame_rate)

    try:
        # Recognize the speech using Google Speech Recognition with Turkish language
        transcript = recognizer.recognize_google(audio_data, language="tr-TR")
        return transcript
    except sr.UnknownValueError:
        return "Anlaşılamadı"
    except sr.RequestError:
        return "API'ye erişim hatası"

# Example usage:
audio_file = "../dataset/dataset_module1/input_audio2.opus"
transcript = convert_audio_to_text(audio_file)
print("Anamnez:", transcript)
