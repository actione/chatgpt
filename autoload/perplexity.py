#!/usr/bin/env python3
import os
import argparse
import json
from chatcore import load_session, save_session
try:
    import openai
except Exception as e:
    os.system("pip3 install --user openai")
    import openai

def chat(model, content, session):
    if "PERPLEXITY_API_KEY" in os.environ.keys():
        openai.api_key = os.environ.get("PERPLEXITY_API_KEY")
    else:
        return "ERROR: please set environment variable PERPLEXITY_API_KEY!"
    msg = {"role": "user", "content": content}
    msgs = load_session(session)
    msgs.append(msg)
    try:
        response_msg = openai.ChatCompletion.create(model=model, messages=msgs, api_base="https://api.perplexity.ai").choices[0].message
    except Exception as e:
        return e
    msgs.append(response_msg)
    save_session(session, msgs)
    return response_msg.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--session", default="")
    parser.add_argument("content")
    result = parser.parse_args()
    print(chat(result.model,result.content, result.session))

if __name__ == "__main__":
    main()


