import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and text from the JSON structure
data_series = chart_config['chart_data'][0]
texts = chart_config['texts']
colors = chart_config['colors']

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data and styling from JSON
fig.add_trace(go.Bar(
    x=data_series['x_values'],
    y=data_series['y_values'],
    marker_color=colors[0],
    text=data_series['y_values'],
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False  # Allows text to be drawn outside the axis range
))

# Combine title and subtitle if they exist
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the chart layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=title_text if title_text else None,
    title_x=0.05,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        range=[0, 700],
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        type='category'
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('note', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,  # Position adjusted for bottom margin
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,  # Position adjusted for bottom margin
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Style the text on top of the bars
fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

# Derive the output filename from the input JSON filename
base_filename = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")