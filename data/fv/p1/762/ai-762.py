import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
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

    fig = go.Figure()

    # Extract data from JSON
    chart_data = chart_info.get('chart_data', [])
    colors = chart_info.get('colors', [])
    texts = chart_info.get('texts', {})
    axis_ranges = chart_info.get('axis_ranges', {})
    shapes = chart_info.get('shapes', [])

    # Plot data series
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=series.get('name', ''),
            line=dict(
                color=colors[i] if i < len(colors) else None,
                dash=series.get('line_style'),
                width=2
            ),
            showlegend=False
        ))

    # Apply layout settings
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            range=axis_ranges.get('x'),
            showgrid=False,
            zeroline=True,
            zerolinecolor='blue',
            zerolinewidth=2,
            tickmode='linear',
            dtick=2,
            title_text=None
        ),
        yaxis=dict(
            range=axis_ranges.get('y'),
            showgrid=False,
            zeroline=True,
            zerolinecolor='blue',
            zerolinewidth=2,
            tickvals=[5],
            title_text=None
        ),
        showlegend=False
    )
    
    # Add annotations for axis titles and arrows
    x_range = axis_ranges.get('x', [-9, 9])
    y_range = axis_ranges.get('y', [-6, 6])
    
    # X-axis title and arrow
    fig.add_annotation(
        x=x_range[1], y=0,
        text=f"<b>{texts.get('x_axis_title', 'x')}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color="black"),
        xanchor='left',
        xshift=10
    )
    fig.add_annotation(
        ax=x_range[1] - 0.2, ay=0,
        x=x_range[1], y=0,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=1.5, arrowcolor='blue'
    )
    
    # Y-axis title and arrow
    fig.add_annotation(
        x=0, y=y_range[1],
        text=f"<b>{texts.get('y_axis_title', 'y')}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color="black"),
        yanchor='bottom',
        yshift=10
    )
    fig.add_annotation(
        ax=0, ay=y_range[1] - 0.2,
        x=0, y=y_range[1],
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=1.5, arrowcolor='blue'
    )

    # Add other annotations from JSON
    for ann in texts.get('annotations', []):
        fig.add_annotation(ann)

    # Add shapes from JSON
    for shape in shapes:
        fig.add_shape(shape)

    # Output image
    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()