import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    fig = go.Figure()

    # Add data traces
    for trace_data in chart_config['chart_data']:
        fig.add_trace(go.Scatter(
            x=trace_data['x'],
            y=trace_data['y'],
            mode='lines',
            name=trace_data['name'],
            line=dict(
                color=chart_config['colors']['series_colors'][trace_data['color_index']],
                width=3,
                dash=trace_data['line_style']
            ),
            showlegend=False
        ))
    
    # Add horizontal reference shapes from the 'shapes' key
    # These are added before the main traces to appear underneath if needed
    for shape in chart_config.get('shapes', []):
        fig.add_shape(
            type='line',
            x0=chart_config['layout_options']['x_range'][0],
            y0=shape['y'],
            x1=chart_config['layout_options']['x_range'][1],
            y1=shape['y'],
            line=dict(
                color=chart_config['colors']['grid'],
                width=2,
                dash=shape['dash']
            )
        )
    
    # Apply layout settings
    fig.update_layout(
        title_text=chart_config['texts']['title'],
        xaxis_title=chart_config['texts']['x_axis_title'],
        yaxis_title=chart_config['texts']['y_axis_title'],
        plot_bgcolor=chart_config['colors']['background'],
        paper_bgcolor=chart_config['colors']['background'],
        font=dict(
            family="Arial",
            size=14,
            color=chart_config['colors']['font']
        ),
        margin=dict(l=60, r=40, t=40, b=60),
        xaxis=dict(
            range=chart_config['layout_options']['x_range'],
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=chart_config['colors']['grid'],
            ticks="",
            showticklabels=False
        ),
        yaxis=dict(
            range=chart_config['layout_options']['y_range'],
            tickvals=chart_config['layout_options']['y_tickvals'],
            gridcolor=chart_config['colors']['grid'],
            gridwidth=2,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=chart_config['colors']['grid']
        )
    )

    # Add annotations
    for ann in chart_config.get('annotations', []):
        fig.add_annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(
                family="Arial",
                size=14,
                color=chart_config['colors']['font']
            ),
            xanchor=ann.get('xanchor', 'center'),
            yanchor=ann.get('yanchor', 'middle')
        )
    
    # Generate and save the image
    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()