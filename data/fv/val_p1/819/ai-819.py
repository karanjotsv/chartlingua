import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# --- 2. Data Extraction and Preparation ---
data = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Prepare data for Plotly's horizontal bar chart
# Data must be reversed to display in the same top-to-bottom order as the image
categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]
text_labels = [f"{v}%" for v in values]

# --- 3. Chart Generation ---
fig = go.Figure()

# Add the single bar series
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0] if colors else '#369661',
        line=dict(width=0)
    ),
    text=text_labels,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family="Arial",
        size=14,
        color='white'
    )
))

# --- 4. Layout and Styling ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=110, r=10, t=10, b=10),
    xaxis=dict(
        visible=False,
        range=[0, max(values) * 1.05]  # Add padding for the longest bar's text
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14, color='#505050')
    )
)

# --- 5. Output ---
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")