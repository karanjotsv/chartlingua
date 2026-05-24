import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get paths from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
    
output_path = json_path.with_suffix('.png')

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create figure
fig = go.Figure()

# Add traces for each data series
annotations = []
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        showlegend=False
    ))
    
    # Add annotation for the series name at the end of the line
    annotations.append(dict(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        xanchor='left',
        yanchor='middle',
        xshift=8,
        showarrow=False,
        font=dict(
            family='Arial',
            size=12,
            color=color
        )
    ))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px; color:#555555;'>{texts['subtitle']}</span>"

# Add source and license annotations
annotations.extend([
    dict(
        xref="paper", yref="paper",
        x=0, y=-0.1,
        xanchor='left', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family='Arial', size=12, color='#7f7f7f')
    ),
    dict(
        xref="paper", yref="paper",
        x=1, y=-0.1,
        xanchor='right', yanchor='top',
        text=texts['license'],
        showarrow=False,
        font=dict(family='Arial', size=12, color='#7f7f7f')
    )
])


# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickvals=[2005, 2006, 2008, 2010, 2012, 2014],
        range=[2004.5, 2015.5]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        tickvals=[0, 2, 4, 6, 8],
        ticktext=[f"{y} years" for y in [0, 2, 4, 6, 8]],
        range=[0, 10]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family='Arial',
        size=12
    ),
    margin=dict(l=60, r=150, t=100, b=80),
    annotations=annotations
)

# Save the figure to a file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")