"""
This is a sample MCP server that provides access to a dataset and allows the LLM to run pandas code on it. The server is built using FastMCP and provides the following resources and tools:
- `data://schema`: Returns the schema of the dataset
- `data://sample`: Returns a sample of the dataset
- `data://column/{col}`: Returns the first 20 values of a specific column
- `run_code`: Allows the LLM to run pandas code on the dataset and returns the
    result as a string.
To run the server, use the following command:
```python server.py
```
Make sure to have the required dependencies installed, such as FastMCP and pandas. The server will be accessible at `http://localhost:port` and you can interact with it using the provided endpoints to explore the dataset and run code on it.
"""

