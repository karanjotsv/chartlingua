import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    texttemplate='%{text}'
))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['xaxis_title'],
        showgrid=False,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['yaxis_title'],
        range=[0, 30000],
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000],
        showgrid=True,
        gridcolor='#E5E5E5',
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, b=100, t=50),
    annotations=[]
)

# Add title if it exists
if texts.get('title'):
    fig.update_layout(
        title=dict(
            text=f"<b>{texts['title']}</b>" + (f"<br><sub>{texts['subtitle']}</sub>" if texts.get('subtitle') else ""),
            x=0.05,
            xanchor='left',
            font=dict(size=20)
        )
    )

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color="grey")
    )

# Generate output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")