import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)


chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly
categories_reversed = chart_data['categories'][::-1]
series_data = chart_data['series']

# Create figure
fig = go.Figure()

# Add traces for each series
for i, series in enumerate(series_data):
    # Reverse values to match reversed categories
    values_reversed = series['values'][::-1]
    
    # Prepare text labels for bars (show >0 values)
    text_labels = [str(v) if v is not None and v > 0 else '' for v in values_reversed]
    
    # Set text color based on bar color for better contrast
    text_font_color = 'white' if i in [0, 3] else 'black'
    
    fig.add_trace(go.Bar(
        y=categories_reversed,
        x=values_reversed,
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=text_labels,
        textposition='inside',
        texttemplate='%{text}',
        textfont=dict(
            family='Arial',
            size=12,
            color=text_font_color
        ),
        insidetextanchor='middle'
    ))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px; color:#555555'>{texts['subtitle']}</span>"

# Combine source and logo
source_text = f"{texts['source']}<br><br><b>{texts['logo']}</b>"

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.98,
        yanchor='top',
        font=dict(family='Arial', size=18, color='black')
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[0, 100.5] # Add a little padding to the right
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed',
        ticks='',
        tickfont=dict(family='Arial', size=12, color='black')
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.01,
        xanchor='center',
        x=0.5,
        traceorder='normal',
        font=dict(family='Arial', size=12)
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=260, r=20, t=120, b=120),
    height=500,
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.22,
            xanchor='left',
            yanchor='top',
            text=source_text,
            showarrow=False,
            align='left',
            font=dict(family='Arial', size=11, color='#666666')
        )
    ]
)
# Add a line above the logo
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0, y0=-0.17, x1=1, y1=-0.17,
    line=dict(color="black",width=1)
)

# Generate output image file path from JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")