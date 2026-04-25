import os
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv

# এনভায়রনমেন্ট ভেরিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)

# গ্রোক ক্লায়েন্ট সেটআপ (রেন্ডার থেকে এপিআই কি নিবে)
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html', task=None, response=None)

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_task = request.form.get('task')
    if not user_task:
        return render_template('index.html', error="Please enter a task!")

    try:
        # গ্রোক এআই মডেল কল করা
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional assistant. Break down tasks into clear steps."
                },
                {
                    "role": "user",
                    "content": f"Please break down this task: {user_task}",
                }
            ],
            # এখানে 'llama3-8b-8192' এর বদলে নিচেরটি লিখুন:
            model="llama-3.3-70b-versatile", 
        )
        
        response_text = chat_completion.choices[0].message.content
        return render_template('index.html', task=user_task, response=response_text)
    
    except Exception as e:
        # এরর মেসেজ যাতে ইউজার দেখতে পারে
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    # রেন্ডার সার্ভারের পোর্টের জন্য এই অংশটি জরুরি
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
