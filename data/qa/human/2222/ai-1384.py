import sys
import json
import plotly.graph_objects as go
import os

# Load data from JSON file specified in command-line argument
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
legend_labels = texts['legend_labels']

# Prepare data for Plotly traces
categories = [d['category'] for d in chart_data]
num_series = len(legend_labels)
series_data = [[d['values'][i] for d in chart_data] for i in range(num_series)]

# Initialize figure
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_data[i],
        name=legend_labels[i],
        orientation='h',
        marker=dict(color=colors[i]),
        text=[f'{val:.1f}' if val % 1 != 0 else int(val) for val in series_data[i]],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family="Arial", size=12),
        hovertemplate='%{x}<extra></extra>'
    ))

# Construct title string
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Set up annotations for source text
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            showarrow=False,
            text=texts['source'],
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    )

# Configure layout
fig.update_layout(
    barmode='stack',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 31],
        tickvals=[0, 5, 10, 15, 20, 25, 30]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=150, r=40, t=50, b=140),
    annotations=annotations
)

# Derive output filename from the input JSON file path
output_filename_base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
output_image_path = f"{output_filename_base}.png"

# Write the image file
fig.write_image(output_image_path, scale=2)