import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from '{json_path}': {e}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly; lists must be reversed for top-to-bottom display
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

categories.reverse()
values.reverse()
colors.reverse()

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=values,
    texttemplate='%{text}',
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(color='white', size=14, family='Arial'),
    hoverinfo='none'
))

# Combine title and subtitle with HTML for styling
full_title_text = (
    f"<span style='font-size: 26px; font-weight: bold;'>{texts['title']}</span><br>"
    f"<span style='font-size: 16px; color: #505050;'>{texts['subtitle']}</span>"
)

# Update layout to match the source image
fig.update_layout(
    title=dict(
        text=full_title_text,
        x=0,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, max(values) * 1.1]  # Ensure space for text on the longest bar
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        automargin=True,
        tickfont=dict(size=14),
        categoryorder='array',
        categoryarray=categories
    ),
    margin=dict(l=100, r=20, t=120, b=180),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    bargap=0.4
)

# Add source and note information as a single annotation
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0,
    y=-0.28,  # Positioned below the plot area
    xanchor='left',
    yanchor='top',
    align='left',
    showarrow=False,
    font=dict(size=12, color='#555555')
)

# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")