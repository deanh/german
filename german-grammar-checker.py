import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define model name - Qwen2.5 3B
model_name = "Qwen/Qwen2.5-3B"

# Initialize tokenizer and model
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Use half-precision for efficiency
    device_map="auto"  # Automatically choose device (CPU or available GPU)
)

def correct_german_text(text, max_new_tokens=100):
    """
    Takes German text and returns a corrected version using Qwen2.5 3B.
    """
    # Create a prompt that instructs the model to perform grammar correction
    prompt = f"""Du bist ein Grammatik- und Rechtschreibhilfe-Tool für Deutsch. Überprüfe den folgenden deutschen Satz auf Fehler und gib die korrigierte Version zurück.
    
Original: {text}
Korrigiert:"""

    # Tokenize the input
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    
    # Generate the response
    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            temperature=0.1,  # Lower temperature for more deterministic outputs
            do_sample=False,  # Use greedy decoding for grammatical correctness
            pad_token_id=tokenizer.eos_token_id  # To avoid generation warnings
        )
    
    # Decode and clean up the response
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Extract just the corrected part (everything after "Korrigiert:")
    try:
        corrected_text = generated_text.split("Korrigiert:")[1].strip()
    except IndexError:
        corrected_text = "Error: Model did not produce a valid correction."
    
    return corrected_text

# Function to demonstrate batch processing
def batch_correct_german(sentences):
    """Process a batch of German sentences and show corrections."""
    for idx, sentence in enumerate(sentences, 1):
        print(f"\nExample {idx}:")
        print(f"Original: {sentence}")
        
        corrected = correct_german_text(sentence)
        print(f"Corrected: {corrected}")
        
        # Highlight differences (simplified)
        if sentence != corrected:
            print("Changes were made ✓")
        else:
            print("No changes needed ✓")

# Example sentences with different types of errors
example_sentences = [
    "Ich habe gestern ein Buch gekauft.", # Correct sentence
    "Ich habe gestern ein buch gekauft.", # Capitalization error
    "Die Kinder spielt im Garten.", # Subject-verb agreement error
    "Ich bin nach Berlin gefahren und habe mein Freund besucht.", # Wrong article "mein" instead of "meinen"
    "Wir mussen heute nach Hause gehen.", # Missing umlaut in "müssen"
    "Ich habe kein zeit für das.", # Gender error "kein" vs "keine"
]

if __name__ == "__main__":
    print(f"Model: {model_name}")
    print("Starting German grammar correction examples...")
    batch_correct_german(example_sentences)
    
    # Interactive mode
    print("\n\n--- Interactive Mode ---")
    print("Enter German sentences for correction (type 'exit' to quit):")
    
    while True:
        user_input = input("\nYour German text: ")
        if user_input.lower() == 'exit':
            break
            
        corrected = correct_german_text(user_input)
        print(f"Corrected: {corrected}")
