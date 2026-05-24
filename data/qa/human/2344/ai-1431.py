import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_info['chart_data']]
num_series = len(chart_info['texts']['legend_labels'])
series_data = []
for i in range(num_series):
    series_data.append([item['values'][i] for item in chart_info['chart_data']])

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=chart_info['texts']['legend_labels'][i],
        marker_color=chart_info['colors'][i],
        text=[f"{y}%" for y in series_data[i]],
        textposition='outside',
        texttemplate='<b>%{text}</b>',
        cliponaxis=False,
        textfont=dict(
            family='Arial',
            size=12
        )
    ))

# Configure layout
fig.update_layout(
    barmode='group',
    bargap=0.25,
    bargroupgap=0.1,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12, color='#333333'),
    yaxis=dict(
        title_text=chart_info['texts']['y_axis_title'],
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        ticktext=['0%', '10%', '20%', '30%', '40%', '50%'],
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
        traceorder='normal',
        font=dict(size=14)
    ),
    margin=dict(l=80, r=40, b=150, t=50, pad=4),
    annotations=[
        dict(
            text=chart_info['texts']['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.38,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Define output filename and save the image
output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")