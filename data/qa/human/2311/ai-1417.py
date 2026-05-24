import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Extract categories and series names in the correct order
categories = [item['category'] for item in chart_data]
series_names = list(chart_data[0]['series'].keys())

# Add a trace for each series
for i, series_name in enumerate(series_names):
    values = [item['series'][series_name] for item in chart_data]
    
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        name=series_name,
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=[f'{v}%' for v in values],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=12)
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br>{texts["subtitle"]}'
    
# Combine source and note for annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f'<br>{texts["note"]}'

# Update layout for a professional appearance
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        ticksuffix='%',
        range=[0, 85]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=280, r=20, t=50, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")