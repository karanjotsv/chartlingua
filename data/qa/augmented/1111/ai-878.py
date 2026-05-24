import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Read data from JSON file
json_file_path = Path(sys.argv[1])
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Prepare paths
output_image_path = json_file_path.with_suffix(".png")

# Initialize figure
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(config['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        line=dict(color=config['colors']['series'][i], width=3),
        marker=dict(color=config['colors']['series'][i], size=8),
        text=[f"{val:.2f}" for val in series['y']],
        textposition='top center',
        textfont=dict(
            family='Arial',
            size=14,
            color=config['colors']['text_labels']
        ),
        hoverinfo='none'
    ))

# Add alternating background rectangles for visual separation
for i in range(len(config['chart_data'][0]['x'])):
    if i % 2 == 1:
        fig.add_vrect(
            x0=i - 0.5, x1=i + 0.5,
            fillcolor=config['colors']['background_odd_cols'],
            layer="below",
            line_width=0,
        )

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=dict(
            text=config['texts']['y_axis_title'],
            standoff=10
        ),
        showticklabels=False,
        showline=False,
        zeroline=False,
        gridcolor=config['colors']['grid'],
        gridwidth=1,
        griddash='dot'
    ),
    annotations=[
        # Additional Information
        dict(
            text=config['texts']['additional_info'],
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            showarrow=False,
            font=dict(color=config['colors']['info_links'], size=12)
        ),
        # Source/Copyright
        dict(
            text=config['texts']['source'],
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='bottom',
            showarrow=False,
            font=dict(color=config['colors']['copyright'], size=12)
        ),
        # Show Source
        dict(
            text=config['texts']['show_source'],
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='bottom',
            showarrow=False,
            font=dict(color=config['colors']['info_links'], size=12)
        )
    ]
)

# Write image to file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")