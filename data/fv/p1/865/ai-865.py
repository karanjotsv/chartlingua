import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# --- 2. Load Data from JSON ---
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 3. Create Chart ---
fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines',
        line=dict(
            color=colors[i % len(colors)] if colors else None,
            width=3
        ),
        connectgaps=False
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    xaxis=dict(
        title=f"<b>{texts.get('x_axis_title', '')}</b>",
        tickvals=list(range(1915, 2015, 3)),
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title=f"<b>{texts.get('y_axis_title', '')}</b>",
        range=[0, 90],
        dtick=10,
        gridcolor='#D3D3D3',
        linecolor='black',
        ticks='outside',
        zeroline=False
    ),
    margin=dict(l=100, r=20, t=20, b=50) # Adjusted margins for axis titles
)

# --- 5. Output Image ---
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart successfully generated and saved to {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)