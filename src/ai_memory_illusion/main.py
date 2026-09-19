import os
from openai import OpenAI
from markrender import MarkdownRenderer

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL = os.environ["MODEL"]

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
renderer = MarkdownRenderer()

def create_memory() -> list[dict]:
    """
    Create LLM memory as a list of dicts.

    As per API surface definition, every call to the LLM API is stateless.
    This means that all the relevant context window must be stored in memory
    and provided as required.
    """
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": "You must respond every prompt."},
        {"role": "system", "content": "You must respond with markdown."}
    ]


def main():
    memory = create_memory()

    # Run with this line commented and uncommented to see the effect of the stateless
    # LLM calls.
    # memory.append({"role": "user", "content": "Hi! I'm Bianca!"})

    response = client.chat.completions.create(model=MODEL, messages=memory)

    renderer.render(response.choices[0].message.content)

    memory.append({"role": "user", "content": "Could you tell me an interesting fact?"})

    response = client.chat.completions.create(model=MODEL, messages=memory)

    renderer.render(response.choices[0].message.content)

    memory.append({"role": "user", "content": "Could you tell me another one?"})

    response = client.chat.completions.create(model=MODEL, messages=memory)

    renderer.render(response.choices[0].message.content)

    memory.append({"role": "user", "content": "What is my name?"})

    response = client.chat.completions.create(model=MODEL, messages=memory)

    renderer.render(response.choices[0].message.content)

    renderer.finalize()


if __name__ == "__main__":
    main()
