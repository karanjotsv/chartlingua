import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename = json_path.with_suffix(".png")

# --- 2. Load Data from JSON ---
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 3. Create Chart Figure ---
fig = go.Figure()

# --- 4. Add Traces ---
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None, width=2)
    ))

# --- 5. Configure Layout ---
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        range=[0, 70],
        showgrid=True,
        gridcolor='#D3D3D3',
        griddash='dot',
        zeroline=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 3.5],
        showgrid=True,
        gridcolor='#D3D3D3',
        griddash='dot',
        zeroline=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=80, b=80),
    plot_bgcolor='white',
    paper_bgcolor='#F0F0F0'
)

# --- 6. Output Chart ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")