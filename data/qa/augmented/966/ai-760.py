import sys
import json
import plotly.graph_objects as go

# Read data from JSON file specified in command-line argument
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data_series = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=data_series['x'],
    y=data_series['y'],
    marker_color=colors[0],
    text=[f'{val:,}'.replace(',', ' ') for val in data_series['y']],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none',
    cliponaxis=False
))

# Configure y-axis ticks with space as thousand separator
y_tick_vals = list(range(0, 20001, 2500))
y_tick_text = [f'{v:,}'.replace(',', ' ') for v in y_tick_vals]

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'] if texts['x_axis_title'] else '',
        showgrid=False,
        showline=False,
        tickmode='array',
        tickvals=data_series['x'],
        ticktext=[str(year) for year in data_series['x']]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        range=[0, 20000],
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        showline=False,
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts['additional_info'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            font=dict(color="#0073B2")
        ),
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=11)
        )
    ]
)

# Determine output filename from input JSON path
base_filename = sys.argv[1]
if '/' in base_filename:
    base_filename = base_filename.split('/')[-1]
if '.' in base_filename:
    base_filename = base_filename.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")