import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_details.get('chart_data', {})
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# Create a new figure
fig = go.Figure()

# Add a bar trace for each series, preserving the order from the JSON
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Build the source/note string
source_note_text = []
if texts.get('source'):
    source_note_text.append(texts.get('source'))
if texts.get('note'):
    source_note_text.append(texts.get('note'))
caption_text = "<br>".join(source_note_text)


# Update layout for a professional look and feel
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        automargin=True,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 45],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
        gridcolor='lightgray',
        gridwidth=1,
        showgrid=True,
        zeroline=False
    ),
    legend=dict(
        title_text=texts.get('legend_title'),
        orientation='h',
        yanchor='bottom',
        y=-0.4, # Adjusted to accommodate long, angled labels
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, t=80, b=180), # Increased bottom margin for labels and legend
    annotations=[
        dict(
            text=caption_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.5, # Position below the legend
            xanchor='left',
            yanchor='bottom',
            align='left'
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")