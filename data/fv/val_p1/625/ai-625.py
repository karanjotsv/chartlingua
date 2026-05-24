import sys
import json
import plotly.graph_objects as go

# Read the JSON file from the command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly's horizontal bar chart
# Data is reversed to match the top-to-bottom order of the original image
categories = [d['category'] for d in data][::-1]
values = [d['value'] for d in data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    name=''
))

# Build the title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}"

# Build the source/note string for annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 10000000]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=180, r=30, t=80, b=80)
)

# Add source/note annotation if present
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left'
    )

# Determine the output filename and save the image
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")