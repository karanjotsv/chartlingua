import sys
import json
import pathlib
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create figure
fig = go.Figure()

# Create a list to hold all annotations
annotations = []

# Add traces and annotations for each data series
for i, series in enumerate(data_series):
    color = colors[i]

    # Add the main line trace
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(color=color, width=3),
        showlegend=False
    ))

    # Add markers for the first and last points
    fig.add_trace(go.Scatter(
        x=[series['x'][0], series['x'][-1]],
        y=[series['y'][0], series['y'][-1]],
        mode='markers',
        marker=dict(
            color='white',
            size=10,
            line=dict(color=color, width=2.5)
        ),
        showlegend=False
    ))

    # Add series name annotation (e.g., "Unfavorable")
    annotations.append(dict(
        x=series['label_pos']['x'],
        y=series['label_pos']['y'],
        text=f"<b>{series['name']}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color=color),
        xanchor='center'
    ))

    # Add start value annotation
    annotations.append(dict(
        x=series['x'][0],
        y=series['y'][0],
        text=str(series['y'][0]),
        showarrow=False,
        font=dict(family="Arial", size=12, color=color),
        xshift=-18
    ))

    # Add end value annotation
    annotations.append(dict(
        x=series['x'][-1],
        y=series['y'][-1],
        text=str(series['y'][-1]),
        showarrow=False,
        font=dict(family="Arial", size=12, color=color),
        xshift=18
    ))

# Combine source and note for the bottom annotation
source_text = f"{texts['source']}<br><b>{texts['note']}</b>"
annotations.append(dict(
    x=0,
    y=-0.22,
    xref='paper',
    yref='paper',
    text=source_text,
    showarrow=False,
    align='left',
    font=dict(family="Arial", size=11, color='black'),
    xanchor='left',
    yanchor='top'
))

# Update layout
fig.update_layout(
    annotations=annotations,
    title=dict(
        text=f"<b>{texts['title']}</b><br>{texts['subtitle']}",
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        tickvals=[2006, 2016],
        tickformat='d',
        showgrid=False,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        range=[-5, 105],
        tickvals=[0, 100],
        ticktext=['0', '100%'],
        gridcolor='#dddddd',
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color='black'),
    showlegend=False,
    margin=dict(l=40, r=40, t=120, b=120)
)

# Define output filename and save image
output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(output_path, scale=2)