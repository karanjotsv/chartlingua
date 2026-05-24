import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    fig = go.Figure()

    # Add pie charts
    for pie in chart_data['pie_charts']:
        fig.add_trace(go.Pie(
            values=pie['values'],
            marker=dict(colors=pie['colors']),
            domain=pie['domain'],
            rotation=pie['rotation'],
            textinfo='percent',
            texttemplate='%{value}%',
            textfont=dict(color='white', size=20, family='Arial'),
            hoverinfo='none',
            hole=0.0,
            sort=False,
            direction='clockwise',
            showlegend=False
        ))

    # Add shapes (lines and paths)
    for shape in chart_data.get('shapes', []):
        fig.add_shape(
            type=shape['type'],
            path=shape.get('path'),
            x0=shape.get('x0'), y0=shape.get('y0'),
            x1=shape.get('x1'), y1=shape.get('y1'),
            xref='paper', yref='paper',
            line=dict(color=shape['color'], width=3)
        )

    # Add text box annotations
    for anno in chart_data.get('annotations', []):
        fig.add_annotation(
            text=anno['text'],
            x=anno['x'], y=anno['y'],
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(family='Arial', size=14, color=anno.get('font_color', 'white')),
            bgcolor=anno.get('bgcolor'),
            borderpad=anno.get('borderpad', 4),
            yanchor=anno.get('yanchor', 'center'),
            xanchor=anno.get('xanchor', 'center'),
            align='center'
        )
        
    # Add center labels for pie charts
    for pie in chart_data['pie_charts']:
        label = pie['center_label']
        fig.add_annotation(
            text=label['text'],
            x=label['x'], y=label['y'],
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(family='Arial', size=label['size'], color='white'),
            align='center'
        )

    # Configure layout
    fig.update_layout(
        title=dict(
            text=chart_data['texts']['title'],
            y=0.98,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(family='Arial', size=32)
        ),
        showlegend=False,
        plot_bgcolor=chart_data['background_color'],
        paper_bgcolor=chart_data['background_color'],
        font=dict(family='Arial'),
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1])
    )

    # Generate and save output image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2, width=800, height=800)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()