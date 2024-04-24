import tkinter as tk
from tkinter import ttk, messagebox
import threading
import speech_recognition as sr

class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Speech Recognition")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Set the theme (change as desired)

        self.text = tk.Text(self.root, wrap=tk.WORD, height=10, width=50, font=("Helvetica", 12))
        self.text.pack(pady=20)

        self.status_label = ttk.Label(self.root, text="Hazır", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.start_button = ttk.Button(self.root, text="Başlat", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Durdur", command=self.stop_listening, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.save_button = ttk.Button(self.root, text="Kaydet", command=self.save_transcription, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.transcription = ""
        self.output_file = "transcription.txt"
        self.saved_length = 0  # To track the length of the transcription last saved

    def start_listening(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.status_label.config(text="Dinleniyor...", foreground="blue")

        # Start a new thread for continuous speech recognition
        threading.Thread(target=self.listen_and_update).start()

    def stop_listening(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.text.get("1.0", tk.END).strip():
            self.save_button.config(state=tk.NORMAL)
        self.status_label.config(text="Durduruldu", foreground="red")

    def listen_and_update(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=20)
                    recognized_text = self.recognizer.recognize_google(audio, language="tr-TR")
                    self.transcription += recognized_text + "\n"  # Add new transcription as a new line
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, self.transcription)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    messagebox.showerror("Hata", f"Ses tanıma hatası: {e}")
                    break

    def save_transcription(self):
        try:
            current_text = self.text.get("1.0", tk.END).strip()
            if current_text:
                with open(self.output_file, "a", encoding="utf-8") as file:
                    file.write(current_text + "\n")  # Append current transcription with a newline
                self.transcription = ""  # Reset transcription after saving
                self.saved_length = len(current_text)  # Update saved length
                messagebox.showinfo("Başarı", "Transkripsiyon başarıyla kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()

    # After the main loop exits (i.e., when the window is closed)
    if app.transcription:
        with open(app.output_file, "a", encoding="utf-8") as file:
            file.write(app.transcription + "\n")
