import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Data Extraction from JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Chart Creation ---
# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the original order from the JSON
    direction='counterclockwise'
)

# --- 4. Layout Configuration ---
layout = go.Layout(
    # The original chart has a 3D effect which is not a standard feature in plotly.graph_objects.
    # We will represent it as a standard 2D pie chart.
    # The title object is left empty as no title is provided in the JSON.
    title=dict(text=None),
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.6,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0)', # Transparent background
        bordercolor='#000000',
        borderwidth=1
    ),
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig = go.Figure(data=[pie_trace], layout=layout)


# --- 5. Output ---
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")