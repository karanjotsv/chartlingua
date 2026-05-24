import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly's horizontal bar chart
# Data needs to be reversed for Plotly to display it from top to bottom
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()
colors.reverse()

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    hoverinfo='none',
    showlegend=False
))

# Add data labels next to each bar
for i, (cat, val) in enumerate(zip(categories, values)):
    fig.add_annotation(
        x=val,
        y=cat,
        text=f"{val:.2f} t",  # Format value with suffix
        showarrow=False,
        xanchor='left',
        xshift=5,
        font=dict(family="Arial", size=12, color="black")
    )

# Combine title and subtitle using HTML tags for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #555;'>{texts.get('subtitle', '')}</span>"

# Update layout for styling, titles, axes, and margins
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=14, color="#333"),
    paper_bgcolor='#F8F8F8',
    plot_bgcolor='white',
    margin=dict(l=240, r=40, t=100, b=80),
    xaxis=dict(
        showticklabels=True,
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticksuffix=' t',
        tickformat='.1f',
        range=[0, max(values) * 1.1]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        autorange='reversed'
    ),
    # Add source and note annotations at the bottom
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            font=dict(size=12, color="#777")
        ),
        dict(
            text=texts.get('note', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            font=dict(size=12, color="#777")
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")