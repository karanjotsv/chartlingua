import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON file at {json_path}")
    sys.exit(1)

data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

values = [item.get('value') for item in data]
# Create custom labels for the legend, formatted as in the original image (e.g., "Category 12,3%")
legend_labels = [f"{item.get('category')} {str(item.get('value')).replace('.', ',')}%" for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=legend_labels,
    values=values,
    marker=dict(colors=colors),
    hoverinfo='label',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=-45,  # Sets start angle to approximate original chart
    domain=dict(x=[0, 0.7]) # Reserve space on the right for the legend
))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.75,
        traceorder="normal",
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=80, b=30, l=30, r=30),
    showlegend=True
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")