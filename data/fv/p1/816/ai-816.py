import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Derive base filename for output
output_filename_base = json_path.rsplit('.', 1)[0]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(str(int(v)))
    else:
        text_labels.append(f'{v:.1f}')

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=text_labels,
    textposition='auto',
    textfont=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    hoverinfo='none'
))

# Update layout
title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else texts.get('subtitle')

fig.update_layout(
    title_text=title_text,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=50, b=80),
    yaxis=dict(
        range=[0, 90],
        tickmode='linear',
        dtick=10,
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    )
)

# Add source/note annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

# Save the figure as a PNG image
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")