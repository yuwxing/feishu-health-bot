# Vercel版本的飞书健康机器人
import json
import httpx
from datetime import datetime

# 健康数据存储
health_records = {"water": [], "exercise": [], "sleep": []}

# 飞书配置
FEISHU_APP_ID = "cli_a90af0fde9389cc8"
FEISHU_APP_SECRET = "GEryspd7ROOf3T6QFa7gLkuPSQ3G7Dof"

def process_health_command(text_content: str):
    """处理健康命令"""
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    if "喝水" in text_content or "water" in text_content:
        record = {"type": "water", "time": current_time, "date": current_date}
        health_records["water"].append(record)
        today_water = len([r for r in health_records["water"] if r["date"] == current_date])
        return f"💧 喝水提醒已记录！\\n⏰ 记录时间：{current_time}\\n🎯 今天已喝水 {today_water} 次\\n💪 继续保持，健康生活！"
    
    elif "运动" in text_content or "exercise" in text_content or "打卡" in text_content:
        record = {"type": "exercise", "time": current_time, "date": current_date}
        health_records["exercise"].append(record)
        today_exercises = len([r for r in health_records["exercise"] if r["date"] == current_date])
        return f"🏃‍♂️ 运动打卡成功！\\n⏰ 打卡时间：{current_time}\\n🎯 今天已运动 {today_exercises} 次\\n💪 坚持运动，身体健康！"
    
    elif "睡眠" in text_content or "睡觉" in text_content or "sleep" in text_content:
        return f"😴 睡眠提醒设置成功！\\n⏰ 当前时间：{current_time}\\n🌙 建议睡眠时间：22:30\\n⏰ 早晨提醒时间：07:00\\n💤 保证充足睡眠，精力更充沛！"
    
    elif "功能" in text_content or "帮助" in text_content or "help" in text_content:
        return "🏥 飞书健康机器人功能：💧发送'喝水'记录饮水 🏃‍♂️发送'运动'打卡 😴发送'睡眠'提醒 📊发送'记录'查看统计"
    
    elif "记录" in text_content or "统计" in text_content:
        today_water = len([r for r in health_records["water"] if r["date"] == current_date])
        today_exercise = len([r for r in health_records["exercise"] if r["date"] == current_date])
        return f"📊 今日健康记录：💧喝水{today_water}次 🏃‍♂️运动{today_exercise}次"
    
    else:
        return "🤖 我是健康机器人，发送'帮助'查看功能"

async def send_feishu_message(user_id: str, content: str):
    """发送飞书消息"""
    try:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            result = response.json()
            
            if result.get("code") == 0:
                token = result.get("tenant_access_token")
                
                msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                msg_data = {
                    "receive_id": user_id,
                    "msg_type": "text",
                    "content": json.dumps({"text": content})
                }
                
                msg_response = await client.post(msg_url, headers=headers, json=msg_data)
                msg_result = msg_response.json()
                
                if msg_result.get("code") == 0:
                    return True
                else:
                    return False
            else:
                return False
                
    except Exception as e:
        return False

# Vercel入口点
def handler(request):
    """Vercel handler"""
    if request.method == 'GET':
        return {
            "message": "飞书健康机器人",
            "status": "运行中",
            "features": ["喝水提醒", "运动打卡", "睡眠提醒"]
        }
    
    elif request.method == 'POST':
        try:
            request_data = request.json()
            
            # 处理URL验证
            if "challenge" in request_data:
                return {"challenge": request_data["challenge"]}
            
            # 处理消息事件
            event_type = request_data.get("header", {}).get("event_type", "")
            if event_type == "im.message.receive_v1":
                event = request_data.get("event", {})
                user_id = event.get("sender", {}).get("sender_id", {}).get("user_id")
                message = event.get("message", {})
                content = message.get("content", "{}")
                
                try:
                    msg_data = json.loads(content)
                    text_content = msg_data.get("text", "")
                except:
                    text_content = content
                
                # 处理健康命令
                response_text = process_health_command(text_content.lower())
                
                # 发送回复消息
                if response_text and user_id:
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(send_feishu_message(user_id, response_text))
                    loop.close()
            
            return {"code": 0, "msg": "success"}
            
        except Exception as e:
            return {"error": str(e)}