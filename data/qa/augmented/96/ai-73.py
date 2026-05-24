import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]

# Format text for display on chart (e.g., "Category 52.3%")
custom_texts = [f"{item['category']} {item['value']}%" for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    text=custom_texts,
    textinfo='text',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='counterclockwise',
    rotation=90,
    pull=[0.005] * len(values)  # Create thin white lines between slices
))

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=100, r=100, t=50, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color='#555555')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")