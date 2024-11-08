from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)

# Variable to store the chat history
chat_history_ids = torch.tensor([])

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=['POST'])
def chat():
    global chat_history_ids  # Declare global to modify the chat history
    
    # Get the user's message from the JSON data in the POST request
    msg = request.json.get("msg")
    
    # Encode the new user input and add EOS token
    new_user_input_ids = tokenizer.encode(str(msg) + tokenizer.eos_token, return_tensors='pt')
    
    # Append the new user input to the chat history
    if chat_history_ids.size(0) > 0:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids
    
    # Generate a response, limiting the chat history to 1000 tokens
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode and return the bot's response
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
