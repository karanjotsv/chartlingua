import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

fig = go.Figure()
y_range = [-5, 105]

# Add background gradient shapes
fig.add_shape(type="rect", xref="paper", yref="y", x0=0, y0=50, x1=1, y1=y_range[1],
              fillcolor=config['colors']['background_gradient'][0], opacity=0.3, layer="below", line_width=0)
fig.add_shape(type="rect", xref="paper", yref="y", x0=0, y0=y_range[0], x1=1, y1=50,
              fillcolor=config['colors']['background_gradient'][1], opacity=0.3, layer="below", line_width=0)

# Add data traces
for i, series in enumerate(config['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode=series['mode'],
        line=dict(
            color=config['colors']['traces'][i],
            dash=series['line']['dash'],
            width=2
        ),
        marker=dict(
            symbol=series['marker']['symbol'],
            color=config['colors']['traces'][i],
            size=7
        )
    ))

# Add horizontal line for neutral feeling
fig.add_hline(y=50, line_width=1.5, line_dash="dash", line_color="darkgray")

# Add annotations
for ann in config['texts']['annotations']:
    arrow_color = None
    if ann.get('showarrow'):
        arrow_color = config['colors']['arrow'].get(ann['text'])

    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=ann.get('showarrow', False),
        font=dict(
            family="Arial",
            size=14,
            color=config['colors']['annotations'][ann['font_color_key']]
        ),
        align=ann['align'],
        xanchor='left' if ann['align'] == 'left' else 'center',
        yanchor='middle',
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        arrowhead=7 if ann.get('showarrow') else 0,
        arrowsize=0.8,
        arrowwidth=1.5,
        arrowcolor=arrow_color
    )

# Configure layout
fig.update_layout(
    xaxis_title=config['texts']['x_axis_title'],
    yaxis_title=config['texts']['y_axis_title'],
    font=dict(family="Arial", size=14, color="black"),
    xaxis=dict(
        title_font=dict(size=16, family="Arial Black"),
        tickfont=dict(size=14),
        showgrid=False,
        zeroline=False,
        range=[1977, 2018],
        tickvals=[1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]
    ),
    yaxis=dict(
        title_font=dict(size=16, family="Arial Black"),
        tickfont=dict(size=14),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=y_range,
        tickvals=[0, 25, 50, 75, 100]
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=90, t=20, b=120),
    annotations=[
        dict(
            text=config['texts']['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.28,
            align="left",
            xanchor="left",
            yanchor="bottom",
            font=dict(size=12, color="dimgray")
        )
    ]
)

# Generate output filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart generated and saved as {output_filename}")