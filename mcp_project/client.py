import asyncio
from fastmcp import Client

from formatter import (
    format_tool_result,
    format_resource,
    format_prompt,
    pretty_print,
    print_table
)

client = Client("http://127.0.0.1:8080/mcp")


async def main():
    async with client:

        print("\n=== MCP SYSTEM INFO ===")

        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        print("\nTools:", [t.name for t in tools])
        print("Resources:", [r.uri for r in resources])
        print("Prompts:", [p.name for p in prompts])

       
        schema_raw = await client.read_resource("data://schema")
        schema = format_resource(schema_raw)

        pretty_print(schema, "Dataset Schema")

        stats_raw = await client.call_tool("basic_stats", {
            "column": "salary"
        })

        stats = format_tool_result(stats_raw)

        print("\nSalary Statistics:")
        print_table(stats)

        prompt_raw = await client.get_prompt("analyst_prompt", {
            "query": "average salary"
        })

        prompt_text = format_prompt(prompt_raw)

        print("\nPrompt:")
        print("-" * 40)
        print(prompt_text)
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())