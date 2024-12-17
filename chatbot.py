import requests
import json

class Chatbot:
    def __init__(self, url="http://localhost:11434/api/chat"):
        """
        Initializes the Chatbot with the API endpoint URL.
        """
        self.url = url
        self.headers = {"Content-Type": "application/json"}
        self.session_messages = []  # To maintain conversation context
        
        # Check if Ollama server is running
        if not self.is_server_running():
            raise ConnectionError("Ollama server is not running. Please start the server and try again.")

    def is_server_running(self):
        """
        Checks if the Ollama server is running by sending a request to the /api/status endpoint.
        
        Returns:
        - bool: True if the server is running, False otherwise.
        """
        try:
            status_url = self.url.replace("/api/chat", "/api/status")
            response = requests.get(status_url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def send_message(self, prompt):
        """
        Sends a prompt to the chatbot and returns the response.
        Parameters:
        - prompt (str): User input to the chatbot.
        
        Returns:
        - response (str): Chatbot's reply or error message if something goes wrong.
        """
        # Append user's message to session for context
        self.session_messages.append({"role": "user", "content": prompt})
        
        # Payload for the API
        payload = {"model": "llama3.2:1b", "messages": self.session_messages}

        try:
            # Send POST request
            response = requests.post(self.url, headers=self.headers, json=payload, stream=True)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse streaming response
            combined_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        # Extract 'response' field
                        combined_response += data.get("response", "")
                    except json.JSONDecodeError:
                        pass

            # Append chatbot's reply to session for context
            self.session_messages.append({"role": "assistant", "content": combined_response})
            return combined_response

        except requests.exceptions.RequestException as e:
            return f"Error: Unable to connect to the chatbot API. {str(e)}"

    def reset_conversation(self):
        """
        Resets the conversation context.
        """
        self.session_messages = []

# Example usage (if running as a standalone script)
if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        print("Chatbot initialized. Type 'exit' to quit or 'reset' to reset the conversation.")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting the chatbot. Goodbye!")
                break
            elif user_input.lower() == "reset":
                chatbot.reset_conversation()
                print("Conversation context reset.")
            else:
                reply = chatbot.send_message(user_input)
                print(f"Chatbot: {reply}")
    except ConnectionError as e:
        print(e)
