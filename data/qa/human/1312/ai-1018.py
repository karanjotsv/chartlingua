import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly by separating categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Assign colors: the first bar gets the first color, the rest get the second
bar_colors = [colors[0]] + [colors[1]] * (len(chart_data) - 1)

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=bar_colors, line_width=0),
    text=values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(color='white', size=14, family='Arial'),
    texttemplate='<b>%{x}</b>',
    hoverinfo='none'
))

# Configure the layout of the chart
title_text = f"<b style='font-size: 24px;'>{texts['title']}</b><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", color="black"),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[0, max(values) * 1.15]  # Ensure space for text inside bars
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed',  # Display categories from top to bottom
        tickfont=dict(size=14, color='#333333')
    ),
    plot_bgcolor='#F1F1F1',
    paper_bgcolor='#F1F1F1',
    showlegend=False,
    margin=dict(l=80, r=20, t=150, b=120),
    # Add source and footer text at the bottom
    annotations=[
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0.01, y=-0.15,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#555555')
        ),
        dict(
            text=f"<b>{texts['footer']}</b>",
            xref="paper", yref="paper",
            x=0.01, y=-0.25,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=14, color='black')
        )
    ],
    # Add the dotted line separating the first category from the rest
    shapes=[
        go.layout.Shape(
            type="line",
            xref="paper",
            yref="y",
            x0=0,
            y0=0.5,
            x1=1,
            y1=0.5,
            line=dict(
                color="grey",
                width=1,
                dash="dot",
            )
        )
    ]
)

# Derive the output filename from the input JSON path
# e.g., 'path/to/chart.json' -> 'path/to/chart.png'
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")