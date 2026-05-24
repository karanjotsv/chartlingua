import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Read JSON data from the specified file path
json_path = Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract chart data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data structures for the Plotly pie chart
labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

# Generate custom text for each slice to accurately reflect the original chart's labeling
# This will display "Label<br>Value%" for slices with labels, and nothing for those without.
custom_text_list = []
for item in chart_data:
    if item.get('label'):
        custom_text_list.append(f"{item['label']}<br>{item['value']}%")
    else:
        custom_text_list.append('')

# Construct the main title and subtitle string using HTML for formatting
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
else:
    full_title = title_text or subtitle_text

# Create the figure object
fig = go.Figure()

# Add the pie chart trace to the figure
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    text=custom_text_list,
    textinfo='text',
    textposition='inside',
    sort=False,
    direction='clockwise',
    rotation=120  # Orient the chart to match the original image
))

# Update trace properties, specifically the font for the text on slices
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=16,
        color='black'
    )
)

# Update the overall layout of the figure
fig.update_layout(
    title_text=full_title,
    font_family="Arial",
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=50, b=20)
)

# Construct and add the source/note annotation if present in the JSON
source_text = texts.get('source') or ''
note_text = texts.get('note') or ''
if source_text or note_text:
    annotation_text = []
    if source_text:
        annotation_text.append(f"Source: {source_text}")
    if note_text:
        annotation_text.append(f"Note: {note_text}")

    fig.add_annotation(
        text="<br>".join(annotation_text),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        yanchor='top',
        xanchor='left',
        font=dict(size=10)
    )

# Generate the output filename and save the chart as a PNG image
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Image generated: {output_filename}")