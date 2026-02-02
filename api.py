import json

def handler(request):
    try:
        if request.method == 'GET':
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "message": "飞书健康机器人",
                    "status": "运行中",
                    "test": "OK"
                })
            }
        
        elif request.method == 'POST':
            try:
                request_data = request.json()
                
                # 处理URL验证
                if "challenge" in request_data:
                    return {
                        "statusCode": 200,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({"challenge": request_data["challenge"]})
                    }
                
                # 简单回复
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"code": 0, "msg": "success"})
                }
                
            except Exception as e:
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"code": 0, "msg": "success"})
                }
    
    except Exception as e:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
