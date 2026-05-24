import sys
import json
import os
import math
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    # Add the pie chart trace with percentage values inside
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
        textinfo='percent',
        textfont=dict(family='Arial', size=14, color='white'),
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        rotation=80
    ))

    # Add annotations for labels outside the pie chart
    annotations = []
    total_value = sum(values)
    current_angle = 80 # Corresponds to pie's rotation
    
    # Define how far from the center the labels and arrow tips should be
    label_radius_multiplier = 1.3
    arrow_tip_radius_multiplier = 1.05

    for item in chart_data:
        slice_angle = (item['value'] / total_value) * 360
        mid_angle_deg = current_angle + (slice_angle / 2)
        mid_angle_rad = math.radians(-mid_angle_deg) # Negative for clockwise from 3 o'clock

        # Calculate positions for the annotation text
        label_x = label_radius_multiplier * math.cos(mid_angle_rad)
        label_y = label_radius_multiplier * math.sin(mid_angle_rad)

        # Calculate positions for the arrow to point to (edge of the pie)
        arrow_x = arrow_tip_radius_multiplier * math.cos(mid_angle_rad)
        arrow_y = arrow_tip_radius_multiplier * math.sin(mid_angle_rad)

        # Determine text alignment based on position
        if -90 < mid_angle_deg % 360 < 90 or 270 < mid_angle_deg % 360 < 360:
             xanchor = 'left'
        else:
             xanchor = 'right'

        annotations.append(
            go.layout.Annotation(
                x=label_x,
                y=label_y,
                text=item['label'],
                showarrow=True,
                arrowhead=0,
                ax=arrow_x,
                ay=arrow_y,
                axref='x',
                ayref='y',
                font=dict(family='Arial', size=12, color='#333333'),
                xanchor=xanchor,
                yanchor='middle'
            )
        )
        current_angle += slice_angle

    title_text = texts['title']
    if texts.get('subtitle'):
        title_text += f"<br><span style='font-size: 14px; color: #808080;'>{texts['subtitle']}</span>"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        showlegend=False,
        margin=dict(t=100, b=80, l=120, r=120),
        paper_bgcolor='white',
        plot_bgcolor='white',
        annotations=annotations
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2, width=600, height=500)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()