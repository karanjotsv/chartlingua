import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=8)
    ))

    # Add data labels for the series if specified
    if s.get('show_labels', False):
        for j, val in enumerate(s.get('data', [])):
            fig.add_annotation(
                x=categories[j],
                y=val,
                text=f"{val}",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                ),
                yshift=15
            )

# Combine source and note for the footer
source_text = []
if texts.get("source_left"):
    source_text.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.25,
            xanchor="left", yanchor="bottom",
            text=texts["source_left"],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0072B2")
        )
    )

if texts.get("source_right"):
    footer_right_text = texts["source_right"]
    if texts.get("note"):
        # The image has these visually separated, so we add space.
        footer_right_text += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{texts['note']}"
        
    source_text.append(
         dict(
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor="right", yanchor="bottom",
            text=footer_right_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=(f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"
              if texts.get('title') else ""),
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        range=[10, 14],
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=40, b=120),
    annotations=source_text
)

# Determine output filename from JSON path
output_filename = f"{Path(json_path).stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")