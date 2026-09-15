import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
from flask import Flask, render_template, request, jsonify
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, SessionRevoked, FloodWait

app = Flask(__name__)

# ملاحظة: قم بوضع الـ API الخاص بك هنا
API_ID = 1234567  # استبدل برقم الـ API
API_HASH = "your_api_hash"  # استبدل الـ Hash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check_session():
    data = request.json
    session = data.get('session')
    
    async def run():
        try:
            async with Client("check_bot", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True) as client:
                me = await client.get_me()
                return {
                    "status": "working",
                    "message": "الحساب شغال وبحالة ممتازة ✅",
                    "info": {
                        "name": f"{me.first_name} {me.last_name or ''}",
                        "username": f"@{me.username}" if me.username else "لا يوجد",
                        "id": me.id,
                        "phone": f"+{me.phone_number}"
                    }
                }
        except Exception as e:
            return {"status": "stopped", "message": f"الحساب متوقف أو مفصول ❌ ({str(e)})"}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run())
    return jsonify(result)

@app.route('/api/change_name', methods=['POST'])
def change_name():
    data = request.json
    session = data.get('session')
    new_name = data.get('new_name')
    
    async def run():
        try:
            async with Client("name_bot", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True) as client:
                await client.update_profile(first_name=new_name)
                return {"success": True, "message": "تم تغيير الاسم بنجاح ✅"}
        except Exception as e:
            return {"success": False, "message": f"فشل تغيير الاسم: {str(e)}"}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return jsonify(loop.run_until_complete(run()))

@app.route('/api/get_messages', methods=['POST'])
def get_messages():
    data.get = request.json
    session = request.json.get('session')
    
    async def run():
        messages_list = []
        try:
            async with Client("msg_bot", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True) as client:
                async for message in client.get_chat_history("me", limit=5):
                    messages_list.append({
                        "text": message.text or "[محتوى غير نصي/وسائط]",
                        "date": str(message.date)
                    })
                return {"success": True, "messages": messages_list}
        except Exception as e:
            return {"success": False, "message": f"فشل سحب الرسائل: {str(e)}"}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return jsonify(loop.run_until_complete(run()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
