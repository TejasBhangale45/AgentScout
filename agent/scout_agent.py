import json
import os
import pyttsx3
import speech_recognition as sr
from rich.console import Console

console = Console()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def load_agents():
    filename = os.path.join(os.path.dirname(__file__), "agents.json")
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        console.print("[red]❌ Missing file: agents.json[/red]")
        return []

def find_agents(agents, query):
    return [agent for agent in agents if query.lower() in agent["category"].lower() or query.lower() in agent["name"].lower()]

def display_agents(agent_list):
    if not agent_list:
        console.print("[yellow]⚠️ No matching agents found.[/yellow]")
        return
    for agent in agent_list:
        console.print(f"[bold cyan]🧠 Name:[/bold cyan] {agent['name']}")
        console.print(f"[green]📂 Category:[/green] {agent['category']}")
        console.print(f"[blue]📖 Description:[/blue] {agent['description']}")
        console.print(f"[magenta]🔧 Skills:[/magenta] {', '.join(agent['skills'])}")
        console.print("─" * 60)

def main():
    speak("Welcome to Agent Scout. What kind of agent are you looking for?")
    agents = load_agents()
    if not agents:
        return
    while True:
        query = input(">> ") or listen()
        if query.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            speak("Goodbye!")
            break
        matched_agents = find_agents(agents, query)
        display_agents(matched_agents)

if __name__ == "__main__":
    main()
