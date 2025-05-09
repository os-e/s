import google.generativeai as genai
import os
import sys

# AIzaSyCnfcqkQpJjtBtdg1UJp2APyRkm997v9Rg
# AIzaSyBjbf1USyp_sRX1OmadWR6W48UdkjXm-ls

api_key = os.getenv("GOOGLE_API_KEY")

try:
    if not api_key:
        print("Google API key not found in environment variables.")
        api_key = input("Please enter your Google Gemini API key: ").strip()
        
    if not api_key:
        raise ValueError("No API key provided - please obtain one from https://ai.google.dev/ and try again")
    
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)


# MODEL_NAME = "gemini-2.0-flash" 
MODEL_NAME = "gemini-1.5-flash" 
# MODEL_NAME = "gemini-2.0-flash-lite" 

try:
    model = genai.GenerativeModel(MODEL_NAME)
                             # safety_settings=safety_settings) # Uncomment to use custom safety settings
except Exception as e:
    print(f"Error initializing the Generative Model: {e}")
    sys.exit(1)

# --- Main Interaction Loop ---
print(f"Connected to Gemini model: {MODEL_NAME}")
print("Enter your prompts below. Type 'quit', 'exit', or press Ctrl+C to end.")
print("-" * 20)

while True:
    try:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["quit", "exit"]:
            print("Exiting chat.")
            break

        if not user_prompt: # Handle empty input
            continue

        # --- Send Prompt to API ---
        print("Gemini: Thinking...", end="\r", flush=True) # Basic loading indicator
        # Use generate_content for single-turn conversation
        response = model.generate_content(user_prompt)

        # --- Display Response ---
        # Clear the "Thinking..." line
        print(" " * 20, end="\r")

        # Check if the response was blocked due to safety settings
        if not response.parts:
             if response.prompt_feedback and response.prompt_feedback.block_reason:
                 print(f"Gemini: [Blocked - {response.prompt_feedback.block_reason}]")
             else:
                 print("Gemini: [Response blocked or empty]")
        else:
             print(f"Gemini: {response.text}")

    except KeyboardInterrupt:
        print("\nExiting chat (Ctrl+C detected).")
        break
    except Exception as e:
        # Clear the "Thinking..." line on error too
        print(" " * 20, end="\r")
        print(f"\nAn error occurred: {e}")
        # Optional: break on error or continue
        # break

print("-" * 20)
print("Session ended.")
