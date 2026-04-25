import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# আপনার Groq API Key এখানে দিন (console.groq.com থেকে পাওয়া কি-টি)
# client = Groq(api_key="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")
client = Groq(api_key="YOUR_GROQ_API_KEY")

@app.route('/')
def index():
    return render_template('index.html', task=None, response=None)

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_task = request.form.get('task')
    try:
        # Groq-এর শক্তিশালী মডেল ব্যবহার করে উত্তর তৈরি করা
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional assistant. Break down tasks into clear, beautiful bulleted steps in Bengali and English as per context. Maintain a professional and fresh tone."
                },
                {
                    "role": "user",
                    "content": f"Please break down this task: {user_task}",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # আপনার সুন্দর ইনডেক্স পেজে উত্তর পাঠানো
        return render_template('index.html', task=user_task, response=response_text)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)