import sys
import json
import pathlib
import plotly.graph_objects as go

# Read JSON data from the file path provided as a command-line argument
json_path = pathlib.Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize a new figure
fig = go.Figure()

# Iterate through the data series from the JSON and add them to the figure
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        text=series['y'],
        textposition='outside',
        cliponaxis=False,
        marker=dict(
            color=colors[i],
            line=dict(
                color='#000000',
                width=1.5
            )
        )
    ))

# Construct the title string from title and subtitle fields
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the figure layout for a clean, accurate appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        # Set y-axis range to prevent data labels from being clipped
        range=[0, max(data_series[0]['y']) * 1.25]
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=120, b=50, l=50, r=50)
)

# Add a source annotation if provided in the JSON
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        showarrow=False,
        text=source_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        xanchor='left',
        yanchor='top',
        align='left'
    )
    # Increase bottom margin to accommodate the source text
    fig.update_layout(margin_b=80)

# Derive the output image filename from the input JSON filename
output_path = json_path.with_suffix(".png")

# Write the figure to a high-resolution PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")