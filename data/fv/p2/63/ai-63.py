import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data
chart_data = chart_info.get('chart_data', [])

# Create figure with subplots
# Column 1 will hold the pie charts, Column 2 will be used for custom legends
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'domain', 'colspan': 1}, {'type': 'xy'}],
           [{'type': 'domain', 'colspan': 1}, {'type': 'xy'}]],
    column_widths=[0.6, 0.4],
    vertical_spacing=0.1,
    horizontal_spacing=0.05
)

# Plot data and create custom legends for each chart
subplot_details = [
    {'chart_index': 0, 'pie_row': 1, 'pie_col': 1, 'legend_xref': 'x2', 'legend_yref': 'y2'},
    {'chart_index': 1, 'pie_row': 2, 'pie_col': 1, 'legend_xref': 'x4', 'legend_yref': 'y4'}
]

for details in subplot_details:
    if details['chart_index'] < len(chart_data):
        data = chart_data[details['chart_index']]
        
        # Add Pie chart trace
        fig.add_trace(go.Pie(
            labels=data['labels'],
            values=data['values'],
            marker_colors=data['colors'],
            hoverinfo='label+percent',
            textinfo='none',
            sort=False,
            direction='clockwise'
        ), row=details['pie_row'], col=details['pie_col'])

        # Add title annotation for the subplot
        fig.add_annotation(
            xref=details['legend_xref'], yref=details['legend_yref'],
            x=0, y=1.0,
            text=f"<b>{data['title']}</b>",
            showarrow=False,
            font=dict(size=12),
            align='left',
            xanchor='left', yanchor='top'
        )

        # Add custom legend annotations
        y_pos = 0.8
        y_step = 0.2 if len(data['labels']) <= 4 else 0.15 # Adjust spacing for more items
        for label, color in zip(data['labels'], data['colors']):
            # Colored square
            fig.add_annotation(
                xref=details['legend_xref'], yref=details['legend_yref'],
                x=0, y=y_pos,
                text='■',
                showarrow=False,
                font=dict(color=color, size=20),
                align='left',
                xanchor='left', yanchor='middle'
            )
            # Text label
            fig.add_annotation(
                xref=details['legend_xref'], yref=details['legend_yref'],
                x=0.1, y=y_pos,
                text=label,
                showarrow=False,
                font=dict(size=11),
                align='left',
                xanchor='left', yanchor='middle'
            )
            y_pos -= y_step

# Update overall layout
fig.update_layout(
    showlegend=False,
    font_family="Arial",
    margin=dict(t=40, b=40, l=10, r=10),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
)

# Hide axes of the 'xy' subplots used for legends
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

# Generate output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")