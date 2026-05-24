import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly traces
y_categories = [d['category'] for d in chart_data]
num_series = len(texts['legend_labels'])

fig = go.Figure()

# Create and add a bar trace for each data series
for i in range(num_series):
    series_values = [d['values'][i] for d in chart_data]
    
    # The last color is light, requiring dark text; others are dark, requiring white text.
    text_font_color = 'black' if i == num_series - 1 else 'white'
    
    fig.add_trace(go.Bar(
        y=y_categories,
        x=series_values,
        name=texts['legend_labels'][i],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=series_values,
        texttemplate='%{text}',
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color=text_font_color
        )
    ))

# Combine title and subtitle for the main title text
title_text = f"{texts['title']}<br>{texts['subtitle']}"

# Update the figure layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18)
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        tickfont=dict(family="Arial", size=14)
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=0.88,
        xanchor='left',
        x=0.01,
        traceorder='normal',
        font=dict(family="Arial", size=12),
        bgcolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=130, r=40, t=150, b=120),
    font=dict(family="Arial"),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=11, color='#666666')
        )
    ]
)

# Generate the output PNG file
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")