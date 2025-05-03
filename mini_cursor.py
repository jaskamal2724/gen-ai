import argparse
import os
import subprocess
import google.generativeai as genai
from typing import Optional
import sys

# Configure Gemini API (replace with your API key setup)
def configure_gemini(api_key: str) -> genai.GenerativeModel:
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Function to interact with Gemini API
def get_gemini_response(model: genai.GenerativeModel, prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"

# Function to create a Python file with specified content
def create_python_file(file_name: str, content: str) -> None:
    try:
        with open(file_name, 'w') as f:
            f.write(content)
        print(f"Created Python file: {file_name}")
    except Exception as e:
        print(f"Error creating Python file: {str(e)}")

# Function to set up a Next.js app
def create_nextjs_app(app_name: Optional[str], model: genai.GenerativeModel) -> None:
    # If no app name provided, ask Gemini for a default
    if not app_name:
        prompt = "Suggest a default name for a Next.js application."
        app_name = get_gemini_response(model, prompt).replace(" ", "-").lower()
        print(f"No app name provided. Using default: {app_name}")
    else:
        print(f"Using app name: {app_name}")

    # Create Next.js app using npx
    try:
        command = f"npx create-next-app@latest {app_name} --typescript --eslint --tailwind --src-dir --app --import-alias '@/*'"
        print("Running Next.js setup...")
        subprocess.run(command, shell=True, check=True)
        print(f"Next.js app '{app_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Next.js app: {str(e)}")

# Main CLI function
def main():
    parser = argparse.ArgumentParser(description="AI Agent CLI Tool")
    parser.add_argument("command", nargs="*", help="Command to execute (e.g., 'create python file', 'create nextjs app')")
    parser.add_argument("--api-key", required=True, help="Gemini API key")
    parser.add_argument("--app-name", help="Optional name for Next.js app")

    args = parser.parse_args()
    command = " ".join(args.command).lower() if args.command else ""
    api_key = ""
    app_name = "mini_cursor"

    # Initialize Gemini model
    model = configure_gemini(api_key)

    if not command:
        print("No command provided. Example: 'create python file' or 'create nextjs app'")
        sys.exit(1)

    # Handle Python file creation
    if "create python file" in command:
        # Ask Gemini to generate Python code based on command
        prompt = f"Generate Python code based on this instruction: {command}. Provide only the code, no explanations."
        code = get_gemini_response(model, prompt)
        file_name = "generated_script.py"
        create_python_file(file_name, code)

    # Handle Next.js app creation
    elif "create nextjs app" in command:
        create_nextjs_app(app_name, model)

    else:
        # Generic command handling
        prompt = f"Interpret and provide a solution for this command: {command}"
        response = get_gemini_response(model, prompt)
        print(response)

if __name__ == "__main__":
    main()