import json

def lambda_handler(event, context):
    try:
        if event.get('httpMethod') == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': '飞书健康机器人',
                    'status': '运行中'
                })
            }
        
        elif event.get('httpMethod') == 'POST':
            try:
                body = json.loads(event.get('body', '{}'))
                
                if 'challenge' in body:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'challenge': body['challenge']})
                    }
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'code': 0, 'msg': 'success'})
                }
                
            except Exception as e:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'code': 0, 'msg': 'success'})
                }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
