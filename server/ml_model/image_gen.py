# ml_model/image_gen.py
import sys
import json

def generate_image_from_text(prompt):
    # Placeholder function to simulate image generation
    # Replace with model inference logic
    return f"Image generated for prompt: {prompt}"

if __name__ == "__main__":
    # Read input text prompt from command line argument
    input_data = json.loads(sys.argv[1])
    prompt = input_data['prompt']
    result = generate_image_from_text(prompt)
    
    # Output the result
    print(json.dumps({"image_data": result}))
