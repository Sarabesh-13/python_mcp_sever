import json


def format_tool_result(result):
    """
    Extracts and parses tool output
    """
    try:
        text = result.content[0].text
        return json.loads(text)
    except Exception:
        return text


def format_resource(result):
    """
    Extracts and parses resource output
    """
    try:
        text = result[0].text
        return json.loads(text)
    except Exception:
        return text


def format_prompt(prompt):
    """
    Extracts prompt text
    """
    try:
        return prompt.messages[0].content.text
    except Exception:
        return str(prompt)


def pretty_print(data, title=None):
    """
    Nicely prints JSON data
    """
    if title:
        print(f"\n {title}")
        print("-" * 40)

    try:
        print(json.dumps(data, indent=2))
    except Exception:
        print(data)


def print_table(data):
    """
    Simple key-value table format
    """
    print("\n-----------------------------")
    for key, value in data.items():
        print(f"{key:<15} : {value}")
    print("-----------------------------")