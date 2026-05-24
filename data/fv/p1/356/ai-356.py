import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)

    chart_data = chart_spec['chart_data']
    texts = chart_spec['texts']
    colors = chart_spec['colors']

    fig = go.Figure()

    # Add the main rank trace (blue line)
    main_trace_data = chart_data[0]
    fig.add_trace(go.Scatter(
        x=main_trace_data['x'],
        y=main_trace_data['y'],
        mode='lines',
        line=dict(color=colors[0], width=2),
        name=main_trace_data.get('name', ''),
        showlegend=False,
        connectgaps=False
    ))

    # Add all divider and other traces (black lines)
    divider_color = colors[1]
    for series in chart_data[1:]:
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(color=divider_color, width=1.5),
            name=series.get('name', ''),
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        font_family="Arial",
        xaxis=dict(
            range=[1929, 2017],
            tickmode='linear',
            tick0=1930,
            dtick=2,
            showgrid=False,
            zeroline=False,
            ticks="outside",
            tickson="boundaries"
        ),
        yaxis=dict(
            range=[85, -2],
            autorange=False,
            tickmode='linear',
            tick0=0,
            dtick=10,
            gridcolor='#D3D3D3',
            zeroline=False,
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(t=100, b=50, l=50, r=30),
        height=500,
        width=1200,
    )

    # Apply reversed y-axis correctly
    fig.update_yaxes(autorange="reversed")

    # Generate output image file path from input JSON file path
    output_filename = json_path.stem + ".png"
    
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()