import os
import openai
import backoff 

completion_tokens = prompt_tokens = 0

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    
def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        outputs.extend([choice.message.content for choice in res.choices])
        # log completion tokens
        completion_tokens += res.usage.completion_tokens
        prompt_tokens += res.usage.prompt_tokens
    return outputs
    
def gpt_usage(backend="gpt-4"):
    ## CHANGE MODEL HERE
    # choices=['gpt-4-0314', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4o-mini', 'gpt-4.1', 'gpt-4.1-mini']
    global completion_tokens, prompt_tokens
    if (backend == "gpt-4") or (backend == "gpt-4-0314"):
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    elif backend == "gpt-4o":
        cost = completion_tokens / 1000 * 0.01 + prompt_tokens / 1000 * 0.00250
    elif backend == "gpt-4o-mini":
        cost = completion_tokens / 1000 * 0.0060 + prompt_tokens / 1000 * 0.0015
    elif backend == "gpt-4.1":
        cost = completion_tokens / 1000 * 0.00800 + prompt_tokens / 1000 * 0.00200
    elif backend == "gpt-4.1-mini":
        cost = completion_tokens / 1000 * 0.00160 + prompt_tokens / 1000 * 0.00040
    # need to add cost completion for any added models like 4.1 or o1mini
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}
