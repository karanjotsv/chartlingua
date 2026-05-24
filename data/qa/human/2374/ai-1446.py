import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create the figure object
fig = go.Figure()

# Add bar traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=[f"{val}{texts['data_labels_suffix']}" for val in series['y']],
        textposition='outside',
        textfont=dict(family='Arial', size=14, color='black'),
        cliponaxis=False
    ))

# Build combined title string
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += f"<sub>{texts['subtitle']}</sub>"

# Update the layout for a professional appearance
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color='#000000'),
    title_text=title_text if title_text else None,
    title_x=0.5,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        range=[0, 8.5],
        tickvals=[0, 2, 4, 6, 8],
        ticksuffix=texts['data_labels_suffix'],
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, b=120, t=50, pad=4),
    annotations=[
        dict(
            showarrow=False,
            text=texts['source'],
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")