import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series.get("data", []),
        name=series.get("name", ""),
        orientation='h',
        marker=dict(
            color=colors[i % len(colors)],
            line=dict(color='white', width=1)
        ),
        text=[f'<b>{val}%</b>' for val in series.get("data", [])],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color="white"
        )
    ))

# Combine title and subtitle for the main title
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for the annotation
source_note_text = []
if texts.get('source'):
    source_note_text.append(texts.get('source'))
if texts.get('note'):
    source_note_text.append(texts.get('note'))
source_text = "<br>".join(source_note_text)


# Configure the layout of the chart
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
        gridcolor='#E5E7EB',
        zeroline=False,
        ticks='outside',
        tickmode='linear',
        tick0=0,
        dtick=20,
        range=[0, 120],
        ticksuffix='%'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        ticks='',
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=170, r=40, b=110, t=50),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Generate the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")