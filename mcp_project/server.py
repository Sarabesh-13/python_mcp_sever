from fastmcp import FastMCP
import pandas as pd
import traceback
from pathlib import Path

# Get current file directory
BASE_DIR = Path(__file__).resolve().parent

# Build correct path
DATA_PATH = BASE_DIR/"data"/"data.csv"

mcp = FastMCP("Data Analyst Server")

# Load dataset
df = pd.read_csv(DATA_PATH)


# mcp resources can be used to provide information to the LLM, like dataset schema, etc.
@mcp.resource("data://schema")
def dataset_schema():
    return {
        "columns": list(df.columns),
        "num_rows": len(df),
        "dtypes": df.dtypes.astype(str).to_dict()
    }

# mcp resources can be used to provide dynamic data to the LLM, like dataset samples, metadata, etc.
@mcp.resource("data://sample")
def sample_data():
    return df.head(10).to_dict(orient="records")

# mcp resources can also be parameterized to provide specific information, like a specific column's data, etc.
@mcp.resource("data://column/{col}")
def get_column(col: str):
    if col not in df.columns:
        return {"error": "Column not found"}
    
    return df[col].head(20).tolist()


# mcp tools can be used for dynamic code execution, like running pandas code on the dataset, etc.
@mcp.tool
def run_analysis(code: str):
    """
    Executes pandas code safely on dataframe 'df'
    Example:
    df['salary'].mean()
    """
    try:
        allowed_globals = {
            "df": df,
            "pd": pd
        }

        result = eval(code, {"__builtins__": {}}, allowed_globals)

        if isinstance(result, pd.DataFrame):
            return result.head(20).to_dict()
        elif isinstance(result, pd.Series):
            return result.head(20).to_dict()
        else:
            return result

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

#mcp tools can be used for specific analyses, like basic statistics, etc.
@mcp.tool
def basic_stats(column: str):
    try:
        return {
            "mean": df[column].mean(),
            "median": df[column].median(),
            "min": df[column].min(),
            "max": df[column].max()
        }
    except Exception as e:
        return str(e)

# mcp tool could also be used for more complex operations, like groupby analysis, etc.
@mcp.tool
def groupby_analysis(group_col: str, value_col: str):
    try:
        result = df.groupby(group_col)[value_col].mean()
        return result.to_dict()
    except Exception as e:
        return str(e)

# mcp prompts can be used to guide the LLM on how to approach the user's query, what resources/tools to use, and how to structure the response.
@mcp.prompt()
def analyst_prompt(query: str):
    return f"""
You are a professional data analyst.

Dataset columns:
{list(df.columns)}

Sample data:
{df.head(5).to_string()}

User question:
{query}

Instructions:
- If calculation is needed → call tools
- Prefer pandas expressions
- Be precise and concise
- Never assume columns that don't exist
"""