import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config['chart_data']
categories = chart_config['categories']
texts = chart_config['texts']
colors = chart_config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors['series_colors'][i],
            line=dict(width=0)
        ),
        text=series['text'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=16,
            color=colors['text_colors'][i]
        )
    ))

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size:16px;color:#555555'>{texts['subtitle']}</span>"

# Combine source and credit text
source_text = f"{texts['source']}<br><br><b>{texts['credit']}</b>"

# Create annotations for the series labels above the top bar
annotations = []
west_values = [d['values'][0] for d in chart_data]
cumulative_sum = 0
for i, series in enumerate(chart_data):
    x_pos = cumulative_sum + west_values[i] / 2
    annotations.append(
        dict(
            x=x_pos,
            y=-0.4, # Position above the top bar
            xref='x',
            yref='y',
            text=f"<b>{series['name']}</b>",
            showarrow=False,
            font=dict(family="Arial", size=14, color='black')
        )
    )
    cumulative_sum += west_values[i]

# Add source text as an annotation at the bottom
annotations.append(
    dict(
        x=0,
        y=-0.3,
        xref='paper',
        yref='paper',
        xanchor='left',
        yanchor='top',
        text=source_text,
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=12, color='#555555')
    )
)

# Update layout for a clean, professional look
fig.update_layout(
    barmode='stack',
    showlegend=False,
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.97,
        yanchor='top',
        font=dict(size=24, family="Arial")
    ),
    xaxis=dict(
        visible=False,
        range=[0, 100] # Set range to 100 as data is in percentages
    ),
    yaxis=dict(
        autorange="reversed",
        showline=False,
        showgrid=False,
        tickfont=dict(size=16, family="Arial")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=150, b=220), # Adjust margins for text
    annotations=annotations,
    font=dict(family="Arial")
)

# Derive output filename from the input JSON path
base_name = json_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")