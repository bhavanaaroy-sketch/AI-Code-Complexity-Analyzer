import streamlit as st
import ast
from radon.complexity import cc_visit

# -------------------------------
# SAFE ANALYZER FUNCTION
# -------------------------------
def analyze_code(code):
    results = {}

    # Safe complexity check
    try:
        complexity = cc_visit(code)
    except:
        complexity = []

    functions = []
    for func in complexity:
        functions.append({
            "name": func.name,
            "complexity": func.complexity
        })

    # Safe AST parsing
    try:
        tree = ast.parse(code)
        loop_count = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
        func_count = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
    except:
        loop_count = 0
        func_count = 0

    results["functions"] = functions
    results["loops"] = loop_count
    results["function_count"] = func_count

    return results

# -------------------------------
# SUGGESTIONS FUNCTION
# -------------------------------
def generate_suggestions(results):
    suggestions = []

    for func in results["functions"]:
        if func["complexity"] > 10:
            suggestions.append(f"⚠️ Function '{func['name']}' is too complex. Break it into smaller parts.")

    if results["loops"] > 3:
        suggestions.append("⚠️ Too many loops detected. Try optimizing logic or reducing nesting.")

    if results["function_count"] == 0:
        suggestions.append("⚠️ No functions found. Use functions to improve structure.")

    if not suggestions:
        suggestions.append("✅ Code looks good! No major issues found.")

    return suggestions

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="AI Code Analyzer", layout="centered")

st.title("💻 AI Code Complexity Analyzer")
st.write("Upload your Python file and get analysis with smart suggestions.")

uploaded_file = st.file_uploader("📂 Upload Python File", type=["py"])

if uploaded_file is not None:
    try:
        code = uploaded_file.read().decode("utf-8")
    except:
        st.error("❌ Error reading file. Please upload a valid Python file.")
        st.stop()

    st.subheader("📄 Uploaded Code")
    st.code(code, language='python')

    # Run analysis safely
    results = analyze_code(code)
    suggestions = generate_suggestions(results)

    # Results
    st.subheader("📊 Analysis Results")

    st.write("### 🔹 Functions & Complexity")
    if results["functions"]:
        for func in results["functions"]:
            st.write(f"Function `{func['name']}` → Complexity: **{func['complexity']}**")
    else:
        st.write("No functions found.")

    st.write(f"🔁 Total Loops: **{results['loops']}**")
    st.write(f"📌 Total Functions: **{results['function_count']}**")

    # Suggestions
    st.subheader("🤖 AI Suggestions")
    for s in suggestions:
        st.write(s)