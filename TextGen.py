import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Function 1: Load the Model and Tokenizer
def load_model_and_tokenizer(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

# Function 2: Tokenize Input
def tokenize_input(text, tokenizer):
    return tokenizer(text, return_tensors="pt")

# Function 3: Generate Text
def generate_text(input_text, tokenizer, model, max_length=50, temperature=1.0, top_k=50, top_p=0.95):
    input_ids = tokenize_input(input_text, tokenizer)["input_ids"]
    output_ids = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        pad_token_id=tokenizer.eos_token_id
    )
    return output_ids

# Function 4: Decode Tokens
def decode_output(output_ids, tokenizer):
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Function 5: Summarize Text (Example)
def summarize_text(input_text, tokenizer, model, max_length=100):
    prompt = f"summarize: {input_text}"
    output_ids = generate_text(prompt, tokenizer, model, max_length=max_length)
    return decode_output(output_ids, tokenizer)

# Function 6: Interactive Chat
def chat_with_model(tokenizer, model, max_length=50):
    print("Start chatting with the model (type 'exit' to stop):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        output_ids = generate_text(user_input, tokenizer, model, max_length=max_length)
        response = decode_output(output_ids, tokenizer)
        print(f"Model: {response}")

# Example Usage
if __name__ == "__main__":
    pass
