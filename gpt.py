import requests
import json
import time
import sys
import os

def clear_screen():
    """Clear screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_color_text(text, color_code):
    """Print colored text"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    }
    return f"{colors.get(color_code, '')}{text}{colors['end']}"

def animate_text(text, delay=0.05):
    """Animate text printing"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_logo():
    """Print animated logo with colors"""
    clear_screen()
    
    # Colorful border animation
    border_colors = ['cyan', 'magenta', 'yellow', 'green', 'blue']
    
    for i in range(3):
        for color in border_colors:
            print(print_color_text("╔══════════════════════════════════════════════╗", color))
            print(print_color_text("║                                              ║", color))
            print(print_color_text("║         ", color), end="")
            
            # Animate main text
            main_text = "⏤‌‌‌‌𝐂𝐨𝐝𝐞𝐗_𝐍𝐞𝐭𝐰𝐨𝐫𝐤"
            for char in main_text:
                print(print_color_text(char, 'cyan' if i == 0 else 'magenta' if i == 1 else 'yellow'), end="")
                sys.stdout.flush()
                time.sleep(0.03)
            
            print(print_color_text("         ║", color))
            print(print_color_text("║                                              ║", color))
            print(print_color_text("╚══════════════════════════════════════════════╝", color))
            time.sleep(0.2)
            if i < 2:
                clear_screen()

def print_final_logo():
    """Print final static logo"""
    clear_screen()
    print(print_color_text("╔══════════════════════════════════════════════╗", "cyan"))
    print(print_color_text("║                                              ║", "cyan"))
    print(print_color_text("║         ", "cyan"), end="")
    
    # Colorful gradient effect for each character
    gradient_colors = ['cyan', 'blue', 'magenta', 'white', 'yellow', 'green']
    main_text = "⏤‌‌‌‌𝐂𝐨𝐝𝐞𝐗_𝐍𝐞𝐭𝐰𝐨𝐫𝐤"
    
    for i, char in enumerate(main_text):
        color_idx = i % len(gradient_colors)
        print(print_color_text(char, gradient_colors[color_idx]), end="")
    
    print(print_color_text("         ║", "cyan"))
    print(print_color_text("║                                              ║", "cyan"))
    print(print_color_text("╚══════════════════════════════════════════════╝", "cyan"))
    
    # Glowing effect dots
    print("\n" + print_color_text(" " * 15 + "• " * 10, "magenta"))
    print(print_color_text(" " * 10 + "⚡ AI Chatbot System Activated ⚡", "yellow"))
    print(print_color_text(" " * 15 + "• " * 10, "magenta"))

def get_chatbot_response(question):
    """Function to get response from chatbot API with English language"""
    
    # Add English language instruction to the question
    english_instruction = "Please respond in English. "
    enhanced_question = english_instruction + question
    
    payload = {
        'messages': [
            {
                'role': 'assistant',
                'content': 'Hello! How can I help you today?'
            },
            {
                'role': 'user',
                'content': enhanced_question
            }
        ]
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Location': 'https://seoschmiede.at/en/aitools/chatgpt-tool/',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    url = 'https://chatbot-ji1z.onrender.com/chatbot-ji1z'

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            api_response = response.json()
            return api_response['choices'][0]['message']['content']
        else:
            return f"Failed. Status code: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"
    except json.JSONDecodeError as e:
        return f"JSON parsing failed: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def loading_animation(text="Loading", duration=2):
    """Show loading animation"""
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    
    print(print_color_text(f"\n{text} ", "cyan"), end="")
    
    while time.time() < end_time:
        for symbol in symbols:
            print(print_color_text(f"\r{text} {symbol}", "cyan"), end="")
            time.sleep(0.1)

def main():
    """Main console interface"""
    # Show animated logo
    print_logo()
    time.sleep(0.5)
    print_final_logo()
    time.sleep(1)
    
    print("\n" + print_color_text("=" * 50, "green"))
    print(print_color_text("        🤖 ENGLISH CHATBOT INTERFACE", "bold"))
    print(print_color_text("=" * 50, "green"))
    
    print(print_color_text("\nInstructions:", "yellow"))
    print(print_color_text("1. Type your question", "cyan"))
    print(print_color_text("2. Type 'quit' to exit", "cyan"))
    print(print_color_text("3. Type 'clear' to clear screen", "cyan"))
    
    print(print_color_text("\n" + "─" * 50, "magenta"))
    
    while True:
        try:
            question = input(print_color_text("\n🔷 Your Question: ", "green")).strip()
            
            if question.lower() == 'quit':
                print(print_color_text("\n" + "✨" * 25, "yellow"))
                print(print_color_text("        Thank you for using CodeX_Network!", "bold"))
                print(print_color_text("                 Goodbye! 👋", "cyan"))
                print(print_color_text("✨" * 25 + "\n", "yellow"))
                break
                
            elif question.lower() == 'clear':
                clear_screen()
                print_final_logo()
                continue
                
            elif not question:
                print(print_color_text("⚠️  Please enter a valid question.", "red"))
                continue
            
            # Show loading animation
            loading_animation("Processing your request", 1.5)
            
            # Get response
            response = get_chatbot_response(question)
            
            # Display response with animation
            print(print_color_text("\n" + "═" * 50, "blue"))
            print(print_color_text("🤖 CHATBOT RESPONSE:", "bold"))
            print(print_color_text("─" * 50, "blue"))
            
            # Animate response printing
            animate_text(print_color_text(response, "white"), 0.005)
            
            print(print_color_text("═" * 50, "blue"))
            
            # Show prompt for next question
            print(print_color_text("\n💡 Ready for next question...", "magenta"))
            
        except KeyboardInterrupt:
            print(print_color_text("\n\n⚠️  Interrupted by user", "red"))
            break
        except Exception as e:
            print(print_color_text(f"\n❌ Error: {str(e)}", "red"))

if __name__ == "__main__":
    main()