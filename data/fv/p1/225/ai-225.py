import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    chart_data = chart_info["chart_data"]
    texts = chart_info["texts"]
    colors = chart_info["colors"]

    fig = make_subplots(rows=2, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}]])

    # Add first pie chart
    fig.add_trace(go.Pie(
        labels=chart_data[0]['labels'],
        values=chart_data[0]['values'],
        name='',
        marker_colors=colors,
        sort=False,
        direction='clockwise',
        showlegend=True,
        textinfo='none',
        hoverinfo='label+percent'
    ), row=1, col=1)

    # Add second pie chart
    fig.add_trace(go.Pie(
        labels=chart_data[1]['labels'],
        values=chart_data[1]['values'],
        name='',
        marker_colors=colors,
        sort=False,
        direction='clockwise',
        showlegend=False,
        textinfo='none',
        hoverinfo='label+percent'
    ), row=2, col=1)

    # Construct main title and source strings
    title_parts = [texts.get('title'), texts.get('subtitle')]
    main_title_text = '<br>'.join(filter(None, title_parts))

    source_parts = [texts.get('source'), texts.get('note')]
    source_text = '<br>'.join(filter(None, source_parts))

    # Calculate x-position for annotations to center them over the pie charts
    # Assuming the legend on the right takes up about 40% of the space
    pie_chart_area_width = 0.6
    annotation_x_pos = pie_chart_area_width / 2

    fig.update_layout(
        title_text=main_title_text if main_title_text else None,
        font_family="Arial",
        font_size=12,
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=800,
        height=600,
        margin=dict(l=20, r=20, t=60, b=60),
        legend=dict(
            traceorder="normal",
            x=0.7, # Position legend to the right
            y=0.5,
            yanchor="middle",
            xanchor="left",
            bgcolor='rgba(255,255,255,0.5)'
        ),
        annotations=[
            dict(
                text=f"<b>{chart_data[0]['title']}</b>",
                x=annotation_x_pos,
                y=0.82,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=18, family="Arial"),
                xanchor='center'
            ),
            dict(
                text=f"<b>{chart_data[1]['title']}</b>",
                x=annotation_x_pos,
                y=0.18,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=18, family="Arial"),
                xanchor='center'
            ),
            dict(
                text=source_text if source_text else None,
                x=0,
                y=-0.1,
                xref="paper",
                yref="paper",
                showarrow=False,
                xanchor="left",
                yanchor="top",
                align="left",
                font=dict(size=10)
            )
        ]
    )

    # Define domains for the pie charts to make space for the legend
    fig.update_traces(domain_row=0, domain_column=0, domain={'x': [0, pie_chart_area_width], 'y': [0.55, 1.0]})
    fig.update_traces(domain_row=1, domain_column=0, domain={'x': [0, pie_chart_area_width], 'y': [0, 0.45]})

    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()