import wikipediaapi
import os
import time
import shutil
import sys
import pygame  # For background sound
from colorama import Fore, Style, init
import pyttsx3  # For Text-to-Speech functionality

# Initialize colorama
init(autoreset=True)

# Initialize pygame for background sound
pygame.mixer.init()

# Initialize pyttsx3 for text-to-speech functionality
engine = pyttsx3.init()

# Function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to dynamically adjust text size based on terminal window width
def get_terminal_width():
    try:
        size = shutil.get_terminal_size(fallback=(80, 20))  # Fallback to 80 columns if terminal size is unknown
        return size.columns
    except:
        return 80  # Fallback to 80 columns

# Function to play background sound
def play_background_sound(sound_path):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(0.5)  # Set volume (optional)
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

# Fun loading animation
def loading_animation():
    loading_symbols = ['|', '/', '-', '\\']
    print(Fore.CYAN + "Loading...", end="")
    for i in range(6):
        print(loading_symbols[i % 4], end="\r", flush=True)
        time.sleep(0.5)
    print(" " * 10, end="\r")  # Clear the loading symbol

# Function to fetch Wikipedia content with wrapping and section-based interaction
def fetch_wikipedia_content(title):
    # Create a Wikipedia API object with a user agent
    user_agent = "MyWikipediaBrowser/1.0 (https://example.com; myemail@example.com)"
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')

    # Fetch the page
    page = wiki_wiki.page(title)
    loading_animation()

    # Check if the page exists
    if not page.exists():
        print(Fore.RED + f"The page '{title}' does not exist on Wikipedia.")
        return

    # Get terminal width and calculate line length for wrapping
    terminal_width = get_terminal_width()

    # Display the sections (subheadings)
    print(Fore.YELLOW + f"\nSections in '{title}':")
    sections = list(page.sections)
    
    if not sections:
        print(Fore.RED + "No sections found for this page.")
        return

    for i, section in enumerate(sections, 1):
        print(Fore.GREEN + f"{i}. {section.title}")

    while True:
        # User selects a section
        section_choice = input("\nEnter the section number to view or 'quit' to exit: ").strip()
        
        if section_choice.lower() == 'quit':
            return

        try:
            section_num = int(section_choice)
            selected_section = sections[section_num - 1]

            print(Fore.CYAN + f"\nYou selected section: {selected_section.title}\n")

            # Wrap text content for readability
            if not selected_section.text.strip():  # Check if content is empty
                print(Fore.RED + "This section is empty or contains no readable content.")
                continue

            wrapped_text = text_wrap(selected_section.text, terminal_width)
            print(Style.BRIGHT + Fore.WHITE + wrapped_text)
            
            # Read the section out loud using TTS
            read_aloud(selected_section.text)

            # Wait for user input before returning to the main loop
            input("\nPress Enter to continue or 'quit' to exit...")

            break  # Exit the loop after displaying the selected section content

        except (ValueError, IndexError):
            print(Fore.RED + "Invalid section number. Please try again.")

# Function to wrap text according to terminal window size
def text_wrap(text, width):
    lines = []
    words = text.split(' ')
    line = ""
    for word in words:
        if len(line + word) + 1 > width:
            lines.append(line)
            line = word
        else:
            if line:
                line += " "
            line += word
    if line:
        lines.append(line)
    return '\n'.join(lines)

# Function to read the section text aloud
def read_aloud(text):
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (range: 0.0 to 1.0)
    
    # Adjust voice properties for a more natural sound (select a voice)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose a more human-like voice (usually index 1)
    
    engine.say(text)
    engine.runAndWait()

# Display ASCII art or image in the terminal (simulating background)
def display_background_image():
    print(Fore.BLACK + Style.BRIGHT + "Welcome to the RU-WIKISearch a CLI based Wikipedia Browser!\n")
    print(Fore.YELLOW + "We're loading the page...")

# Function to display the "About" section
def about_info():
    print(Fore.CYAN + Style.BRIGHT + "\nAbout Ru-Wiki_SEARCH\n")
    time.sleep(1)
    print(Fore.GREEN + Style.BRIGHT + "Name of the Application: " + Fore.YELLOW + "Ru-Wiki_SEARCH")
    print(Fore.GREEN + Style.BRIGHT + "Creator: " + Fore.YELLOW + "Rudransh Kumar")
    print(Fore.GREEN + Style.BRIGHT + "Email ID: " + Fore.YELLOW + "rudranshkumar9936@gmail.com")
    print(Fore.GREEN + Style.BRIGHT + "GitHub: " + Fore.YELLOW + "https://github.com/RuverseR")
    print(Fore.GREEN + Style.BRIGHT + "Program Version: " + Fore.YELLOW + "1.1R")
    print(Fore.GREEN + Style.BRIGHT + "Made in India\n")
    print(Fore.RED + "Copyright (c) 2025, Rudransh Kumar. All rights reserved.\n")

# Main program to interact with the user
def main():
    clear_screen()
    display_background_image()
    time.sleep(1)

    print(Fore.GREEN + "Welcome to the Command Line Wikipedia Browser!")
    time.sleep(1)

    while True:
        # Prompt the user for a Wikipedia page title
        title = input("\nEnter the title of the Wikipedia page you want to view (or 'quit' to exit, 'cls' to clear, 'about' to know more): ").strip()

        # Clear the screen if the user types 'cls'
        if title.lower() == 'cls':
            clear_screen()
            display_background_image()
            continue

        # Display "About" information if the user types 'about'
        if title.lower() == 'about':
            about_info()
            continue

        # Exit the loop if the user types 'quit'
        if title.lower() == 'quit':
            print(Fore.GREEN + "Exiting the Wikipedia Browser. Goodbye!")
            pygame.mixer.music.stop()  # Stop music when exiting
            break

        # Play background sound when starting a new search
        play_background_sound("0e54f62adb7b298ba00a8442dad37607.mp3")

        # Fetch and display the Wikipedia content with sections
        fetch_wikipedia_content(title)

if __name__ == "__main__":
    main()





