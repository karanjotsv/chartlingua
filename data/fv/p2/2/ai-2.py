import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    filename_base = os.path.splitext(os.path.basename(json_path))[0]

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data['chart_data']
    colors = chart_data['colors']

    labels = [item['label'] for item in data]
    outer_colors = colors['outer']
    inner_colors = colors['inner']

    # Values for the outer ring trace (total size of each category)
    total_values = [sum(item['values']) for item in data]
    # Values for the inner ring trace
    inner_values = [item['values'][1] for item in data]

    fig = go.Figure()

    # Add the outer ring. This is a pie chart representing the total value of each category,
    # styled with the 'outer' color. The labels are positioned outside this ring.
    fig.add_trace(go.Pie(
        labels=labels,
        values=total_values,
        marker=dict(
            colors=outer_colors,
            line=dict(color='#ffffff', width=2)
        ),
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black', weight='bold'),
        textinfo='label',
        sort=False,
        direction='clockwise',
        rotation=102 # Adjust rotation to position "Other" at the top
    ))
    
    # Add the inner ring. This is a smaller pie chart plotted on top of the first one.
    # Its values represent the inner portion of each category.
    fig.add_trace(go.Pie(
        labels=labels,
        values=inner_values,
        marker=dict(
            colors=inner_colors,
            line=dict(color='#ffffff', width=2)
        ),
        textinfo='none',
        sort=False,
        direction='clockwise',
        domain={'x': [0.17, 0.83], 'y': [0.17, 0.83]},
        rotation=102
    ))

    # Update layout to create the central hole and format the chart
    fig.update_layout(
        showlegend=False,
        margin=dict(l=80, r=80, t=40, b=40),
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='white',
        # Add a white circle in the center to create the donut hole effect
        shapes=[
            go.layout.Shape(
                type="circle",
                xref="paper", yref="paper",
                x0=0.415, y0=0.415, x1=0.585, y1=0.585,
                fillcolor="white",
                line_color="white"
            )
        ]
    )

    output_filename = f"{filename_base}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()