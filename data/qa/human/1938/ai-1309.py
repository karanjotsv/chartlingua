import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Try to read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_config.get('chart_data', [])
chart_texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for the pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    hoverinfo='label+percent'
))

# Update trace properties for layout and appearance
fig.update_traces(
    textposition='outside',
    textinfo='label+percent',
    textfont=dict(
        family="Arial",
        size=14
    ),
    pull=[0.01] * len(labels) # Small pull for better label line visibility
)

# Construct title and subtitle from JSON
title_text = chart_texts.get('title')
subtitle_text = chart_texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += f"<i>{subtitle_text}</i>"

# Prepare annotations for source and note
annotations = []
source_text = chart_texts.get('source')
if source_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.1,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=10, color="grey")
        )
    )

note_text = chart_texts.get('note')
if note_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.1,
            xanchor='left', yanchor='top',
            text=note_text,
            showarrow=False,
            font=dict(family="Arial", size=10, color="grey")
        )
    )

# Update layout for the final appearance
fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=80, t=80, b=100),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations
)

# Generate the output PNG filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")