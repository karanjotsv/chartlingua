import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Create figure
fig = go.Figure()

# Add traces
trace_map = {
    "true": {"mode": "lines"},
    "approx. n=6": {"mode": "markers"}
}

for i, series in enumerate(chart_data):
    name = series.get("name")
    trace_style = trace_map.get(name, {"mode": "lines"}) # Default to lines
    
    if trace_style["mode"] == "lines":
        fig.add_trace(go.Scatter(
            x=series["x"],
            y=series["y"],
            name=name,
            mode='lines',
            line=dict(color=colors[i])
        ))
    elif trace_style["mode"] == "markers":
        fig.add_trace(go.Scatter(
            x=series["x"],
            y=series["y"],
            name=name,
            mode='markers',
            marker=dict(
                symbol='circle-open',
                size=6,
                color=colors[i],
                line=dict(width=1, color=colors[i])
            )
        ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        font=dict(size=16)
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        range=[0, 1],
        tickmode='linear',
        dtick=0.1,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 5],
        tickmode='linear',
        dtick=0.5,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F0F0F0',
    margin=dict(l=60, r=40, t=80, b=60),
    autosize=False,
    width=800,
    height=600
)

# Generate output filename
base_filename, _ = os.path.splitext(os.path.basename(json_file_path))
output_filename = f"{base_filename}.png"

# Save image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")