import json
import requests

import openai_proxy


def authenticate():
    if openai_proxy.username == "" \
            or openai_proxy.course_id == "" \
            or openai_proxy.access_key == "" \
            or openai_proxy.access_token == "":
        return "Please set your username, courseId, accessKey, and accessToken"
    return False


class Completion:
    @staticmethod
    def create(prompt,
               engine="babbage",
               temperature=0.7,
               max_tokens=200,
               top_p=1,
               frequency_penalty=0,
               presence_penalty=0,
               stop=[],
               n=1
               ):
        error = authenticate()
        if error:
            return error

        body = {
            "username": openai_proxy.username,
            "courseId": openai_proxy.course_id,
            "accessKey": openai_proxy.access_key,
            "accessToken": openai_proxy.access_token,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "engine": engine,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop,
            "n": n
        }
        r = requests.post('http://openai-proxy.herokuapp.com/b/request/openai', json=body)
        print(r)
        response = json.loads(r.text)
        if response['status'] == 'success':
            return response['response']
        else:
            return response['error']


