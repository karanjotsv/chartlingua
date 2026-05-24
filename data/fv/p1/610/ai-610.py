import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Extract data from JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create a figure
fig = go.Figure()

# Define domains for the pie charts
domains = [
    {'x': [0.55, 1.0], 'y': [0.55, 1.0]}, # Top right
    {'x': [0.0, 0.45], 'y': [0.0, 0.45]},  # Bottom left
    {'x': [0.55, 1.0], 'y': [0.0, 0.45]}   # Bottom right
]

# Pull the first slice of each pie chart, as in the original image
pull_values = [0.2] + [0] * (len(chart_data[0]['values']) - 1)

# Add pie chart traces
for i, data in enumerate(chart_data):
    fig.add_trace(go.Pie(
        labels=data['labels'],
        values=data['values'],
        name=data['title'],
        domain=domains[i],
        marker_colors=colors,
        hoverinfo='label+percent',
        textinfo='none',
        pull=pull_values,
        sort=False,
        showlegend=False
    ))

# Define annotations for titles and custom legends
annotations = []

# Main Title and Subtitle
main_title_text = f"<b>{texts['main_title']}</b><br>{texts['subtitle']}"
annotations.append(
    go.layout.Annotation(
        text=main_title_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.02,
        y=0.98,
        font=dict(size=20)
    )
)

# Chart titles and their custom legends
legend_positions = [
    {'title_x': 0.77, 'title_y': 1.0, 'legend_x': 0.86, 'legend_y': 0.85}, # Top right
    {'title_x': 0.22, 'title_y': 0.5, 'legend_x': 0.35, 'legend_y': 0.38}, # Bottom left
    {'title_x': 0.77, 'title_y': 0.5, 'legend_x': 0.86, 'legend_y': 0.38}  # Bottom right
]
legend_y_step = 0.06

for i, data in enumerate(chart_data):
    # Chart title
    annotations.append(go.layout.Annotation(
        text=f"<b>{data['title']}</b>",
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=legend_positions[i]['title_x'],
        y=legend_positions[i]['title_y'],
        font=dict(size=16)
    ))

    # Custom legend items for each chart
    for j, label in enumerate(data['labels']):
        # Legend color marker
        annotations.append(go.layout.Annotation(
            text='■',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=legend_positions[i]['legend_x'],
            y=legend_positions[i]['legend_y'] - (j * legend_y_step),
            font=dict(color=colors[j], size=20),
            xanchor='left',
            yanchor='middle'
        ))
        # Legend label text
        annotations.append(go.layout.Annotation(
            text=label,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=legend_positions[i]['legend_x'] + 0.02,
            y=legend_positions[i]['legend_y'] - (j * legend_y_step),
            xanchor='left',
            yanchor='middle'
        ))

# Update layout
fig.update_layout(
    height=600,
    width=1000,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    annotations=annotations
)

# Generate output filename from the JSON path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")