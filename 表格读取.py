#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role
# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# 封装模型响应函数
def get_response(messages):
    try:
        print("正在调用API...")
        # 尝试使用Generation模型而不是MultiModalConversation
        response = dashscope.Generation.call(
            model='qwen3-vl-flash',
            messages=messages,
            result_format='message'
        )
        print(f"API响应状态码: {response.status_code}")
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

content = [
    {'image': 'https://ts2.tc.mm.bing.net/th/id/OIP-C.YtjgYNq1e8RrkvRKNjLA2QHaKU?rs=1&pid=ImgDetMain&o=7&rm=3'}, # Local path
    {'text': '这是一个表格图片，帮我提取里面的内容，输出JSON格式'}
]

messages=[{"role": "user", "content": content}]
# 得到响应
response = get_response(messages)

if response:
    print(f"完整响应: {response}")
    
    # 检查响应结构
    if hasattr(response, 'output') and response.output:
        if hasattr(response.output, 'choices') and response.output.choices:
            choice = response.output.choices[0]
            if hasattr(choice, 'message') and choice.message:
                message = choice.message
                if hasattr(message, 'content') and message.content:
                    content = message.content
                    print(f"消息内容: {content}")
                    
                    # 尝试打印文本内容
                    try:
                        if isinstance(content, list) and len(content) > 0:
                            if isinstance(content[0], dict) and 'text' in content[0]:
                                print("提取的表格内容:")
                                print(content[0]['text'])
                            else:
                                print("内容格式不符合预期:")
                                print(content)
                        else:
                            print("内容格式不符合预期:")
                            print(content)
                    except Exception as e:
                        print(f"打印内容时出错: {str(e)}")
                else:
                    print("响应中没有content字段")
            else:
                print("响应中没有message字段")
        else:
            print("响应中没有choices字段")
    else:
        print("响应中没有output字段")
else:
    print("获取响应失败")

