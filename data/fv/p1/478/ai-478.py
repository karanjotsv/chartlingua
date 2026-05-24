import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get file path from command line
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Derive output filename from JSON filename
output_filename = json_file_path.with_suffix('.png')

# Load data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Initialize figure
fig = go.Figure()

# Plot data series from JSON
color_idx = 0
for series in config['chart_data']:
    if series.get('type') == 'marker':
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='markers',
            marker=dict(
                symbol='diamond',
                size=12,
                color=config['colors']['spot_marker']['fill'],
                line=dict(
                    color=config['colors']['spot_marker']['border'],
                    width=2
                )
            ),
            name=series.get('name', ''),
            showlegend=series.get('showlegend', True)
        ))
    else:
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(
                color=config['colors']['series'][color_idx],
                width=3
            ),
            name=series.get('name', '')
        ))
        # Add arrow at the end of the line
        fig.add_annotation(
            x=series['x'][-1],
            y=series['y'][-1],
            showarrow=True,
            arrowhead=2,
            arrowwidth=1.5,
            arrowcolor=config['colors']['series'][color_idx],
            ax=15,
            ay=0
        )
        color_idx += 1

# Add helper lines and shapes based on data
# Horizontal dotted line for Money Market Return
money_market_y = config['chart_data'][0]['y'][1]
fig.add_shape(
    type="line", x0=-10, y0=money_market_y, x1=110, y1=money_market_y,
    line=dict(color="black", width=1, dash="dot")
)

# Vertical dashed line for Strike 1
strike1_x, strike1_y = config['chart_data'][0]['x'][1], config['chart_data'][0]['y'][1]
fig.add_shape(
    type="line", x0=strike1_x, y0=0, x1=strike1_x, y1=strike1_y,
    line=dict(color="black", width=1, dash="dash")
)

# Vertical dashed line for Strike 2
strike2_x, strike2_y = config['chart_data'][1]['x'][1], config['chart_data'][1]['y'][1]
fig.add_shape(
    type="line", x0=strike2_x, y0=0, x1=strike2_x, y1=strike2_y,
    line=dict(color="black", width=1, dash="dash")
)

# Add text annotations from JSON
for ann in config['texts']['annotations']:
    fig.add_annotation(
        text=ann.get('text', ''),
        x=ann.get('x'), y=ann.get('y'), showarrow=False,
        xanchor=ann.get('xanchor', 'center'), yanchor=ann.get('yanchor', 'middle'),
        ax=ann.get('ax', 0), ay=ann.get('ay', 0),
        font=dict(family="Arial", size=12)
    )

# Add y-axis arrow
fig.add_annotation(
    x=0, y=60, showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor='black', ax=0, ay=-15
)

# Update layout
texts = config['texts']
fig.update_layout(
    template="plotly_white",
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='black',
        showline=False, showticklabels=False, range=[-10, 120],
        title_standoff=10, title_font=dict(size=14)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black',
        showticklabels=False, range=[-60, 60],
        title_standoff=10, title_font=dict(size=14)
    ),
    legend=dict(
        x=0.98, y=0.4, xanchor='right', yanchor='top',
        bgcolor='rgba(255,255,255,0)', borderwidth=0
    ),
    margin=dict(l=60, r=20, t=20, b=80),
    annotations=[
        dict(
            text=texts['source'], showarrow=False,
            xref="paper", yref="paper",
            x=0.98, y=0.01,
            xanchor='right', yanchor='bottom', align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Write image to file
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")