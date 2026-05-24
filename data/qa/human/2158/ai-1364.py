import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    # --- Argument Parsing ---
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    output_filename_base = json_path.stem

    # --- Data Loading ---
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']
    legend_items = texts['legend_items']

    # --- Data Preparation ---
    categories = [item['category'] for item in chart_data]
    
    # Data must be reversed for horizontal bar charts in Plotly to display top-to-bottom
    categories.reverse()

    # --- Chart Creation ---
    fig = go.Figure()

    # Add traces for each data series
    for i, series_name in enumerate(legend_items):
        values = [item['values'][i] for item in chart_data]
        values.reverse()  # Also reverse values to match categories

        fig.add_trace(go.Bar(
            y=categories,
            x=values,
            name=series_name,
            orientation='h',
            marker_color=colors[i],
            text=[f'{v}%' for v in values],
            textposition='outside',
            textfont=dict(color='black', size=12),
            cliponaxis=False
        ))

    # --- Layout Configuration ---
    # Combine title and subtitle if they exist
    title_text = ""
    if texts.get("title"):
        title_text += texts["title"]
    if texts.get("subtitle"):
        title_text += f'<br><span style="font-size:0.8em;color:grey;">{texts["subtitle"]}</span>'

    fig.update_layout(
        font_family="Arial",
        title_text=title_text if title_text else None,
        plot_bgcolor='white',
        barmode='group',
        bargap=0.3, # Gap between groups of bars
        bargroupgap=0.1, # Gap between bars within a group
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showgrid=True,
            gridcolor='lightgray',
            zeroline=False,
            ticksuffix='%',
            range=[0, 50]
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            showgrid=False,
            zeroline=False,
            automargin=True  # Automatically adjusts margin for long labels
        ),
        margin=dict(l=100, r=40, t=50, b=120)
    )

    # Add source and note annotations
    annotations = []
    if texts.get('source'):
        annotations.append(
            dict(
                xref="paper", yref="paper",
                x=1, y=-0.32,
                xanchor='right', yanchor='bottom',
                text=texts['source'],
                showarrow=False,
                font=dict(size=12, color="grey")
            )
        )
    if texts.get('note'):
         annotations.append(
            dict(
                xref="paper", yref="paper",
                x=0, y=-0.32,
                xanchor='left', yanchor='bottom',
                text=texts['note'],
                showarrow=False,
                font=dict(size=12, color="grey")
            )
        )
    
    if annotations:
        fig.update_layout(annotations=annotations)

    # --- Output ---
    output_path = f"{output_filename_base}.png"
    fig.write_image(output_path, scale=2)
    print(f"Chart successfully generated and saved to '{output_path}'")

if __name__ == '__main__':
    # To prevent any potential issues with running the script in different environments,
    # the main logic is wrapped in a function and called via __name__ == '__main__'.
    # This is a standard Python best practice.
    main()