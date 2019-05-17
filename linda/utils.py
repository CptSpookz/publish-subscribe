import json
                                
# recebe a mensagem em json e transforma em um dicionário encodado em utf-8
def pack(data: dict):
    message_json = json.dumps(data)
    message = f'{len(message_json)}:{message_json}'

    return message.encode('utf-8')


# recebe a mensagem em string e transforma em json
def unpack(data: str):
    message_json = {'op': "", 'sender': "", 'topic': "", 'msg': ""}
    try:
        message_json = json.loads(data)
    except Exception as e:
        print("Error: ", e)
    return message_json
