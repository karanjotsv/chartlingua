import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
series_names = chart_info['series_names']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
series_data_values = []
label_colors = []

# Unpack series data and label colors
series_0_data = []
series_0_colors = []
series_1_data = []
series_1_colors = []

for item in chart_data:
    series_0_data.append(item['values'][0]['value'])
    series_0_colors.append(item['values'][0]['label_color'])
    series_1_data.append(item['values'][1]['value'])
    series_1_colors.append(item['values'][1]['label_color'])

series_data_values = [series_0_data, series_1_data]
label_colors = [series_0_colors, series_1_colors]

# Initialize figure
fig = go.Figure()

# Add traces for each data series
for i, series_name in enumerate(series_names):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series_data_values[i],
        mode='lines+markers',
        name=series_name,
        line=dict(color=colors[i], width=3),
        marker=dict(color=colors[i], size=8, symbol='circle'),
        hoverinfo='none'
    ))

# Add data labels as annotations for precise control
for i in range(len(series_names)):
    for j in range(len(categories)):
        val_series0 = series_data_values[0][j]
        val_series1 = series_data_values[1][j]
        
        # Determine y-shift to prevent overlap, especially at the crossover point
        if i == 0:  # 'Favor' series
            yshift = 10 if val_series0 > val_series1 else -12
        else:  # 'Oppose' series
            yshift = -10 if val_series1 < val_series0 else 12

        fig.add_annotation(
            x=categories[j],
            y=series_data_values[i][j],
            text=str(series_data_values[i][j]),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color=label_colors[i][j]
            ),
            yshift=yshift
        )

# Add series name annotations
for ann in texts['series_annotations']:
    fig.add_annotation(
        x=ann['category'],
        y=ann['value'],
        text=ann['text'],
        showarrow=False,
        xshift=ann['xshift'],
        yshift=ann['yshift'],
        xanchor=ann['xanchor'],
        font=dict(
            family="Arial",
            size=14,
            color=ann['font_color']
        )
    )

# Configure layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family="Arial", size=22, color='#333333'),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickfont=dict(family="Arial", size=14, color='black')
    ),
    yaxis=dict(
        visible=False,
        range=[20, 80]
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=100, b=120),
    width=650,
    height=550
)

# Add source annotation
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0,
    y=-0.25,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(family="Arial", size=11, color='#666666')
)

# Generate output image file
output_filename = json_file_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")