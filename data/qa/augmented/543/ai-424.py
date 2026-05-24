import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- Chart Recreation from JSON data ---

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build title string, handling null values
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += f"<i>{texts['subtitle']}</i>"

# Create a list for annotations, starting with the source
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="gray")
        )
    )

# Update layout
fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis=dict(
        range=[0, 1250],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        zeroline=False,
        tickformat=","
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=80),
    annotations=annotations,
    bargap=0.3
)

# --- Output ---

# Generate the output filename from the input JSON path
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")