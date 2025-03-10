import openai
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up API keys
openai.api_key = 'your_openai_api_key'
stripe.api_key = 'your_stripe_api_key'

# AI Snapshot Prompt Template
SNAPSHOT_PROMPT = """
Provide a concise and insightful life snapshot report for the user. Cover the following categories briefly:

1. Emotional Health: Current mood and stress level with immediate actionable advice.
2. Financial Snapshot: Brief assessment and actionable suggestions.
3. Relationship Check: Quick analysis of user's relationships and practical tips.
4. Productivity Analysis: Simple, effective advice to enhance productivity.

User input:
"""

# Route to get a free brief snapshot
@app.route('/free_snapshot', methods=['POST'])
def free_snapshot():
    data = request.json
    user_input = data.get('user_input', '')
    prompt = SNAPSHOT_PROMPT + user_input + "\nProvide a brief summary (2 sentences per category maximum)."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    summary = response.choices[0].message.content.strip()
    return jsonify({
        "free_snapshot": summary,
        "upgrade_message": "Get your detailed, personalized report for just $5!",
        "payment_link": "https://your_stripe_payment_link_here"
    })

# Webhook after successful payment for premium detailed snapshot
@app.route('/premium_snapshot', methods=['POST'])
def premium_snapshot():
    data = request.json
    user_input = data.get('user_input', '')

    detailed_prompt = SNAPSHOT_PROMPT + user_input + "\nProvide a detailed report (5-6 sentences per category). Include highly personalized recommendations."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": detailed_prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    detailed_report = response.choices[0].message.content.stri
