import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        text=series['y'],
        textposition='outside',
        texttemplate='%{text}',
        marker_color=colors['bar_colors'][i],
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# Create annotations for footer text
annotations = []
if texts.get('note_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note_left'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="blue"),
            align="left"
        )
    )
if texts.get('source_right'):
    # The original has "Show source" below the copyright, but it's not in the JSON.
    # Replicating just the copyright text.
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source_right'],
            showarrow=False,
            font=dict(family="Arial", size=12),
            align="right"
        )
    )

# Update layout for a clean, professional look
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1.8],
        tickmode='linear',
        dtick=0.25,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0]['x'],
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        ticks='outside'
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=annotations,
    bargap=0.2
)

# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")