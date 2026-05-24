import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    fig = go.Figure()

    # Add data series
    for i, series in enumerate(chart_data["chart_data"]):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(color=chart_data["colors"][i], width=2.5),
            name=series.get('name', ''),
            showlegend=False
        ))

    # Update layout
    texts = chart_data["texts"]
    fig.update_layout(
        font=dict(family="Arial", size=18, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=texts["x_axis_title"],
            range=[-15, 55],
            tickmode='array',
            tickvals=[-10, 0, 10, 20, 30, 40, 50],
            showline=True,
            linewidth=1.5,
            linecolor='black',
            ticks='outside',
            tickwidth=1.5,
            ticklen=8,
            mirror=True,
            minor=dict(
                ticks="outside",
                ticklen=4,
                tickwidth=1,
                tickcolor='black',
                dtick=5
            )
        ),
        yaxis=dict(
            title=texts["y_axis_title"],
            autorange='reversed',
            range=[36.5, 32.0],
            tickmode='array',
            tickvals=[32.3, 33.3, 34.3, 35.3, 36.3],
            showline=True,
            linewidth=1.5,
            linecolor='black',
            ticks='outside',
            tickwidth=1.5,
            ticklen=8,
            mirror=True,
            title_standoff=10
        ),
        margin=dict(l=60, r=20, t=60, b=80),
        annotations=texts.get("annotations", []),
        shapes=chart_data.get("shapes", [])
    )
    
    # Generate and save image
    output_filename = json_path.with_suffix(".png")
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()