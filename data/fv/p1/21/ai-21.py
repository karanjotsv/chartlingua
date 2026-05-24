import sys
import json
import os
import plotly.graph_objects as go

# The script expects the path to the JSON file as the only command-line argument.
json_path = sys.argv[1]

# Load the chart specification from the provided JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data, texts, and colors from the loaded JSON.
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Prepare data lists for Plotly.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize a Plotly Figure.
fig = go.Figure()

# Add the pie chart trace, ensuring the original order is preserved.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='none'
))

# Combine title and subtitle from the JSON into a single HTML string for the title.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the chart layout, including title, legend, font, and margins.
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='#D3D3D3',
    margin=dict(t=80, b=180, l=40, r=40)  # Increased bottom margin for source text.
)

# Add the source text as an annotation at the bottom of the chart.
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0,
        y=0.01,
        xanchor='left',
        yanchor='bottom',
        showarrow=False,
        align='left',
        font=dict(size=10)
    )

# Determine the output image filename from the input JSON filename.
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

# Save the generated chart to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")