import sys
import json
import plotly.graph_objects as go

# Read the JSON file path from the command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load the chart data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
series_names = [key for key in chart_data[0].keys() if key != 'category']

# Create the figure object
fig = go.Figure()

# Add a trace for each data series
for i, series_name in enumerate(series_names):
    y_values = [d[series_name] for d in chart_data]
    trace_color = colors[i % len(colors)]
    
    fig.add_trace(go.Scatter(
        x=categories,
        y=y_values,
        name=series_name,
        mode='lines+markers+text',
        line=dict(color=trace_color, width=2.5),
        marker=dict(color=trace_color, size=7),
        text=[f'{val:.2f}' for val in y_values],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='#000000'
        )
    ))

# Update the layout for a clean, professional appearance
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[71.5, 79.5]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=50)
)

# Add source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        showarrow=False,
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.28,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=12, color="#666666")
    )

# Determine the output filename from the input JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")