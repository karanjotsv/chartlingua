import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON object
data = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize a Plotly Figure object
fig = go.Figure()

# Add the primary line trace to the figure
fig.add_trace(go.Scatter(
    x=data['x'],
    y=data['y'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=data['text_labels'],
    textposition=data['text_positions'],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none'
))

# Create a list for annotations (source, notes, etc.)
annotations_list = []
if texts.get('note'):
    annotations_list.append(dict(
        xref="paper", yref="paper",
        x=0.01, y=-0.25,
        xanchor='left', yanchor='bottom',
        text=f"ⓘ {texts['note']}",
        showarrow=False,
        font=dict(family="Arial", size=12, color=colors[0])
    ))
if texts.get('source'):
    annotations_list.append(dict(
        xref="paper", yref="paper",
        x=0.99, y=-0.25,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    ))

# Update the figure's layout, styling, and annotations
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color='#666666')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#EAEAEA',
        zeroline=False,
        tickvals=[3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5],
        ticktext=['3%', '3.25%', '3.5%', '3.75%', '4%', '4.25%', '4.5%', '4.75%', '5%'],
        range=[2.9, 5.1],
        tickfont=dict(size=12, color='#666666')
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations_list
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)