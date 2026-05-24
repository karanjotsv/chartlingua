import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = [d['category'] for d in chart_data]
num_series = len(texts['series_names'])

# Create the figure
fig = go.Figure()

# Add traces for each series
for i in range(num_series):
    series_name = texts['series_names'][i]
    y_values = [d['values'][i] for d in chart_data]
    
    fig.add_trace(go.Bar(
        name=series_name,
        x=categories,
        y=y_values,
        marker_color=colors[i],
        text=[f'{v}%' for v in y_values],
        textposition='outside',
        cliponaxis=False # Ensures text for 0 values is visible
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure layout
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 105],
        ticksuffix='%',
        gridcolor='#E5E5E5'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    margin=dict(l=60, r=40, b=140, t=50),
    annotations=[
        dict(
            text=texts.get('source_left', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.4,
            xanchor='left', yanchor='bottom',
            align='left'
        ),
        dict(
            text=texts.get('source_right', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.4,
            xanchor='right', yanchor='bottom',
            align='right'
        )
    ]
)

fig.update_traces(textfont_size=12, textangle=0)

# Generate output PNG
output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")