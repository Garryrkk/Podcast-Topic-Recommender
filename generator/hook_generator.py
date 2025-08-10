import openai

openai.api_key = "YOUR_API_KEY"

def generate_hook(topic):
    prompt = f"Generate a catchy podcast title and hook for a Gen Z mental health podcast episode about: {topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response['choices'][0]['message']['content']
