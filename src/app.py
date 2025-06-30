import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px

import numpy as np
import plotly.graph_objects as go

# Load the processed H1B visa data

top_20_employers_df = pd.read_csv('src/data/top_20_employers.csv')
top_20_employer_wage_stats = pd.read_csv('src/data/top_20_employer_wage_stats.csv')
top_20_employers_merged = pd.read_csv('src/data/top_20_employers_merged.csv')

top_20_job_titles_df = pd.read_csv('src/data/top_20_job_titles.csv')
top_20_job_title_wage_stats = pd.read_csv('src/data/top_20_job_title_wage_stats.csv')
top_20_job_titles_merged = pd.read_csv('src/data/top_20_job_titles_merged.csv')

top_50_employers_by_median_wage = pd.read_csv('src/data/top_50_employers_by_median_wage.csv')

state_counts = pd.read_csv('src/data/state_counts.csv')
state_median_wage = pd.read_csv('src/data/state_median_wage.csv')

top_500_job_titles = pd.read_csv('src/data/top_500_job_titles.csv')
top_2000_employers = pd.read_csv('src/data/top_2000_employers.csv')

top_500_job_title_stats = pd.read_csv('src/data/top_500_job_title_stats.csv')
top_2000_employer_stats = pd.read_csv('src/data/top_2000_employer_stats.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Add this near the top of your layout, outside any Divs:


# Define the layout of the app
app.layout = html.Div([
    dcc.Interval(id='jobtitle-histogram-interval', interval=500, n_intervals=0, max_intervals=1),
    dcc.Interval(id='employer-histogram-interval', interval=500, n_intervals=0, max_intervals=1),
    html.H1("H1B Data Analysis (2020-2024)"),
    html.Div([
        html.Div([
            html.Div([
                html.H2("Top 20 employers by number of certified H1B applications", style={"marginTop": "0px", "marginLeft": "30px"}),
                dcc.Loading(dcc.Graph(id='top-employers-bar', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
            html.Div([
                html.H2("Median prevailing wage of the top 20 H1B employers", style={"marginTop": "0px", "marginLeft": "30px"}),
                dcc.Loading(dcc.Graph(id='top-employers-wage-bar', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
        ], style={"width": "100%", "display": "flex", "flexDirection": "row"}),
        html.Div([
            html.Div([
                html.H2("Top 20 job titles by number of certified H1B applications", style={"marginTop": "30px", "marginLeft": "30px"}),
                dcc.Loading(dcc.Graph(id='top-jobtitles-bar', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
            html.Div([
                html.H2("Median prevailing wage of the top 20 job jitles", style={"marginTop": "30px", "marginLeft": "30px"}),
                dcc.Loading(dcc.Graph(id='top-jobtitles-wage-bar', style={"marginTop": "30px", "marginLeft": "30px", "width": "100%"}), type="circle"),
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
        ], style={"width": "100%", "display": "flex", "flexDirection": "row"}),
       
        html.Div([
            html.Div([
                html.H2("Top 20 Employers: Application Count vs. Median Wage", style={"marginTop": "30px", "marginLeft": "30px"}),
            dcc.Loading(dcc.Graph(id='top20-employers-scatter', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
        ], style={"width": "96%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"width": "100%", "display": "flex", "flexDirection": "row"}),

        html.Div([
            html.Div([
                html.H2("Top 20 Job Titles: Application Count vs. Median Wage", style={"marginTop": "30px", "marginLeft": "30px"}),
        dcc.Loading(dcc.Graph(id='top20-jobtitles-scatter', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
        ], style={"width": "96%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"width": "100%", "display": "flex", "flexDirection": "row"}),
    
        html.Div([
            html.Div([
                html.H2("Top 50 employers by median prevailing wage (500+ applications)", style={"marginTop": "30px", "marginLeft": "30px"}),
                dcc.Loading(dcc.Graph(id='top50-employers-bar', style={"marginLeft": "30px", "width": "100%"}), type="circle"),
            ], style={"width": "96%", "display": "inline-block", "verticalAlign": "top"}),
        ], style={"width": "100%", "display": "flex", "flexDirection": "row"}),
    ], style={"width": "100%", "marginTop": "40px"}),
    

    html.Div([
        html.Div([
            html.H2("H1B Application Count by Worksite State", style={"marginTop": "40px", "marginLeft": "30px"}),
            dcc.Loading(dcc.Graph(id='state-count-map', style={"marginLeft": "30px"}), type="circle")
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([
            html.H2("Median Prevailing Wage by Worksite State", style={"marginTop": "40px", "marginLeft": "30px"}),
            dcc.Loading(dcc.Graph(id='state-median-salary-map', style={"marginLeft": "30px"}), type="circle")
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"width": "100%", "marginTop": "20px"}),
    html.Div([
        html.Div([
            html.H2("Median Prevailing Wage by Job Title", style={"marginTop": "20px", "marginLeft": "30px"}),
            html.P(
                "Select a job title from the list (limited to top 500 job titles by count).",
                style={"color": "blue", "fontWeight": "normal", "marginLeft": "30px", "fontStyle": "oblique"}
            ),
            dcc.Dropdown(
                id='job-title-dropdown',
                options=[
                    {'label': jt, 'value': jt}
                    for jt in top_500_job_titles['JOB_TITLE_GROUPED'].values.tolist()
                ],
                value='Software Engineer',
                clearable=False,
                style={"marginLeft": "30px", "width": "90%"}
            ),
            dcc.Loading(dcc.Graph(id='choropleth-map', style={"marginLeft": "30px"}), type="circle"),
            dcc.Loading(dcc.Graph(id='jobtitle-wage-histogram', style={"height": 500, "marginLeft": "30px"}), type="circle"),
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([
            html.H2("Median Prevailing Wage by Employer", style={"marginTop": "20px", "marginLeft": "30px"}),
            html.P(
                "Select an employer from the list (limited to top 2000 employers by application count).",
                style={"color": "blue", "fontWeight": "normal", "marginLeft": "30px", "fontStyle": "oblique"}
            ),
            dcc.Dropdown(
                id='employer-dropdown',
                options=[
                    {'label': emp, 'value': emp}
                    for emp in top_2000_employers['EMPLOYER_NAME'].values.tolist()

                ],
                value='Google LLC',
                clearable=False,
                style={"marginLeft": "30px", "width": "90%"}
            ),
            dcc.Loading(dcc.Graph(id='employer-choropleth-map', style={"marginLeft": "30px"}), type="circle"),
            dcc.Loading(dcc.Graph(id='employer-wage-histogram', style={"height": 500, "marginLeft": "30px"}), type="circle"),
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"})
    ], style={"width": "100%", "marginTop": "20px"}),

    # --- Data Sources Section ---
html.Div([
        html.H2("Data Sources", style={"marginTop": "40px", "marginLeft": "30px"}),
        html.P([
            "All data visualized in this dashboard is based on publicly available H-1B disclosure data from the U.S. Department of Labor (2020-2024). ",
            html.A(
                "https://www.dol.gov/agencies/eta/foreign-labor/performance",
                href="https://www.dol.gov/agencies/eta/foreign-labor/performance",
                target="_blank",
                style={"color": "blue", "textDecoration": "underline"}
            )
        ], style={"marginLeft": "30px", "marginRight": "30px"}),
                html.P([
            "This dashboard uses the cleaned dataset compiled by Zongao Bian, available at ",
            html.A(
                "https://www.kaggle.com/datasets/zongaobian/h1b-lca-disclosure-data-2020-2024",
                href="https://www.kaggle.com/datasets/zongaobian/h1b-lca-disclosure-data-2020-2024",
                target="_blank",
                style={"color": "blue", "textDecoration": "underline"}
            ),
            " with additional processing of the dataset."
        ], style={"marginLeft": "30px", "marginRight": "30px"}),
        html.P([
            "© Athul Girija, 2025 | Licensed under ",
            html.A(
                "CC BY-SA 4.0",
                href="https://creativecommons.org/licenses/by-sa/4.0/",
                target="_blank",
                style={"color": "#888", "textDecoration": "underline"}
            )
        ], style={"marginLeft": "30px", "marginTop": "30px", "color": "#888", "fontSize": "14px"})
    ])
])


@app.callback(
    Output('choropleth-map', 'figure'),
    Input('job-title-dropdown', 'value')
)
def update_jobtitle_map(selected_job_title):
    # Use the precomputed top_300_job_title_stats instead of h1b_visa_data
    # Assumes columns: 'JOB_TITLE_GROUPED', 'PREVAILING_WAGE', 'WORKSITE_STATE'
    df = top_500_job_title_stats[top_500_job_title_stats['JOB_TITLE_GROUPED'] == selected_job_title]
    state_stats = (
        df.groupby("WORKSITE_STATE")["PREVAILING_WAGE"]
        .median()
        .reset_index()
        .rename(columns={"PREVAILING_WAGE": "median"})
    )
    fig = px.choropleth(
        state_stats,
        locations="WORKSITE_STATE",
        locationmode="USA-states",
        color="median",
        color_continuous_scale="Viridis",
        scope="usa",
        labels={"median": "Wage"},
        title=f"Median Prevailing Wage for {selected_job_title}"
    )
    fig.update_layout(
        width=900,
        height=500,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        dragmode=False  # Disables both pan and zoom
    )
    return fig

@app.callback(
    Output('employer-choropleth-map', 'figure'),
    Input('employer-dropdown', 'value')
)
def update_employer_map(selected_employer):
    # Use the precomputed top_2000_employer_stats instead of h1b_visa_data
    # Assumes columns: 'EMPLOYER_NAME', 'PREVAILING_WAGE', 'WORKSITE_STATE'
    df = top_2000_employer_stats[top_2000_employer_stats['EMPLOYER_NAME'] == selected_employer]
    state_salary = (
        df.groupby("WORKSITE_STATE")["PREVAILING_WAGE"]
        .median()
        .reset_index()
    )
    fig = px.choropleth(
        state_salary,
        locations="WORKSITE_STATE",
        locationmode="USA-states",
        color="PREVAILING_WAGE",
        color_continuous_scale="Viridis",
        scope="usa",
        labels={"PREVAILING_WAGE": "Wage"},
        title=f"Median Prevailing Wage for {selected_employer}"
    )
    fig.update_layout(
        width=900,
        height=500,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        dragmode=False  # Disables both pan and zoom
    )
    return fig

@app.callback(
    Output('top-employers-bar', 'figure'),
    Input('job-title-dropdown', 'value')  # Dummy input to trigger update; you can use Input() with no dependency if you want it static
)
def update_top_employers_bar(_):
    # Use the precomputed top_20_employers_df instead of h1b_visa_data
    # Assumes top_20_employers_df has columns: 'EMPLOYER_NAME', 'COUNT'
    df = top_20_employers_df.sort_values('COUNT', ascending=True)
    fig = px.bar(
        x=df['COUNT'],
        y=df['EMPLOYER_NAME'],
        orientation='h',
        labels={'x': 'Number of Applications', 'y': 'Employer'},
    )
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":200,"b":0},
        yaxis={'categoryorder':'total ascending'}
    )
    return fig

@app.callback(
    Output('state-count-map', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_state_count_map(_):
    # Use the precomputed state_counts df instead of h1b_visa_data
    # Assumes state_counts has columns: 'WORKSITE_STATE', 'count'
    df = state_counts.copy()
    fig = px.choropleth(
        df,
        locations="WORKSITE_STATE",
        locationmode="USA-states",
        color="count",
        color_continuous_scale="Greens",
        scope="usa",
        labels={"count": "Count"},
    )
    fig.update_layout(
        width=900,
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            x=0.90  # Move colorbar to the left (default is 1.02)
        )
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.0,
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        dragmode=False  # Disables both pan and zoom
    )
    return fig

@app.callback(
    Output('state-median-salary-map', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_state_median_salary_map(_):
    # Use the precomputed state_median_wage df instead of h1b_visa_data
    # Assumes state_median_wage has columns: 'WORKSITE_STATE', 'median_salary'
    df = state_median_wage.copy()
    fig = px.choropleth(
        df,
        locations="WORKSITE_STATE",
        locationmode="USA-states",
        color="MEDIAN_PREVAILING_WAGE",
        color_continuous_scale="Viridis",
        scope="usa",
        labels={"MEDIAN_PREVAILING_WAGE": "Prevailing Wage"},
    )
    fig.update_layout(
        width=900,
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            x=0.94  # Move colorbar to the left (default is 1.02)
        )
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=2.9,
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        dragmode=False  # Disables both pan and zoom
    )
    return fig



# ...existing code...

@app.callback(
    Output('top-employers-wage-bar', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_top_employers_wage_bar(_):
    # Use the precomputed top_20_employer_wage_stats instead of h1b_visa_data
    # Assumes top_20_employer_wage_stats has columns: 'EMPLOYER_NAME', 'median', 'std'
    wage_stats = top_20_employer_wage_stats.sort_values(by='median', ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=wage_stats['median'],
        y=wage_stats['EMPLOYER_NAME'],
        orientation='h',
        error_x=dict(
            type='data',
            array=wage_stats['std'],
            visible=True
        ),
        name='Median Wage',
        marker_color='lightblue'
    ))
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":200,"b":0},
        yaxis={'categoryorder':'array', 'categoryarray': wage_stats['EMPLOYER_NAME'].tolist()},
        xaxis_title='Prevailing Wage',
    )
    return fig


@app.callback(
    Output('top-jobtitles-bar', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_top_jobtitles_bar(_):
    # Use the precomputed top_20_job_titles_df instead of h1b_visa_data
    # Assumes top_20_job_titles_df has columns: 'JOB_TITLE', 'COUNT'
    df = top_20_job_titles_df.sort_values('COUNT', ascending=True)
    fig = px.bar(
        x=df['COUNT'],
        y=df['JOB_TITLE'],
        orientation='h',
        labels={'x': 'Number of Applications', 'y': 'Job Title'},
    )
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":200,"b":0},
        yaxis={'categoryorder':'total ascending'}
    )
    return fig


@app.callback(
    Output('top-jobtitles-wage-bar', 'figure'),
    Input('top-jobtitles-bar', 'figure')  # Dummy input to trigger update
)
def update_top_jobtitles_wage_bar(_):
    # Use the precomputed top_20_job_title_wage_stats instead of h1b_visa_data
    # Assumes top_20_job_title_wage_stats has columns: 'JOB_TITLE', 'median', 'std'
    wage_stats = top_20_job_title_wage_stats.sort_values(by='median', ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=wage_stats['median'],
        y=wage_stats['JOB_TITLE_GROUPED'],
        orientation='h',
        error_x=dict(
            type='data',
            array=wage_stats['std'],
            visible=True
        ),
        name='Median Wage',
        marker_color='lightgreen'
    ))
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":200,"b":0},
        yaxis={'categoryorder':'array', 'categoryarray': wage_stats['JOB_TITLE_GROUPED'].tolist()},
        xaxis_title='Prevailing Wage',
    )
    return fig

@app.callback(
    Output('jobtitle-wage-histogram', 'figure'),
    [Input('job-title-dropdown', 'value'),
     Input('jobtitle-histogram-interval', 'n_intervals')]
)
def update_jobtitle_wage_histogram(selected_job_title, n_intervals):
    if n_intervals == 0:
        # Return an empty figure until interval fires
        return go.Figure()
    df = top_500_job_title_stats[top_500_job_title_stats['JOB_TITLE_GROUPED'] == selected_job_title]
    median_wage = df["PREVAILING_WAGE"].median()
    q1 = df["PREVAILING_WAGE"].quantile(0.10)
    q3 = df["PREVAILING_WAGE"].quantile(0.90)
    fig = px.histogram(
        df,
        x="PREVAILING_WAGE",
        nbins=75,
        title=f"Distribution of Prevailing Wage for {selected_job_title}",
        labels={"PREVAILING_WAGE": "Prevailing Wage"},
        color_discrete_sequence=["#636EFA"]
    )
    fig.add_vline(
        x=q1,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"10%",
        annotation_position="top"
    )
    fig.add_vline(
        x=median_wage,
        line_dash="solid",
        line_color="red",
        annotation_text=f"Median: {round(median_wage, -3)/1000:.0f}k",
        annotation_position="top right"
    )
    fig.add_vline(
        x=q3,
        line_dash="dot",
        line_color="green",
        annotation_text=f"90%",
        annotation_position="top"
    )
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":0,"b":0},
        bargap=0.1
    )
    return fig

# Then, in your employer-wage-histogram callback:
@app.callback(
    Output('employer-wage-histogram', 'figure'),
    [Input('employer-dropdown', 'value'),
     Input('employer-histogram-interval', 'n_intervals')]
)
def update_employer_wage_histogram(selected_employer, n_intervals):
    if n_intervals == 0:
        # Return an empty figure until interval fires
        return go.Figure()
    # ...existing code...
    df = top_2000_employer_stats[top_2000_employer_stats['EMPLOYER_NAME'] == selected_employer]
    median_wage = df["PREVAILING_WAGE"].median()
    q1 = df["PREVAILING_WAGE"].quantile(0.10)
    q3 = df["PREVAILING_WAGE"].quantile(0.90)
    fig = px.histogram(
        df,
        x="PREVAILING_WAGE",
        nbins=75,
        title=f"Distribution of Prevailing Wage for {selected_employer}",
        labels={"PREVAILING_WAGE": "Prevailing Wage"},
        color_discrete_sequence=["#EF553B"]
    )
    fig.add_vline(
        x=q1,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"10%",
        annotation_position="top"
    )
    fig.add_vline(
        x=median_wage,
        line_dash="solid",
        line_color="blue",
        annotation_text=f"Median: {round(median_wage, -3)/1000:.0f}k",
        annotation_position="top right"
    )
    fig.add_vline(
        x=q3,
        line_dash="dot",
        line_color="green",
        annotation_text=f"90%",
        annotation_position="top"
    )
    fig.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":0,"b":0},
        bargap=0.1
    )
    return fig

@app.callback(
    Output('top50-employers-bar', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_top50_employers_bar(_):
    # Use the precomputed top_50_employers_by_median_wage instead of h1b_visa_data
    # Assumes columns: 'EMPLOYER_NAME', 'median', 'std', 'count'
    df = top_50_employers_by_median_wage.sort_values(by='median', ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['EMPLOYER_NAME'],
        y=df['median'],
        error_y=dict(
            type='data',
            array=df['std'],
            visible=True
        ),
        name='Median Wage',
        marker_color='mediumpurple'
    ))
    fig.update_layout(
        height=600,
        margin={"r":0,"t":0,"l":50,"b":0},
        xaxis={'categoryorder':'array', 'categoryarray': df['EMPLOYER_NAME'].tolist(), 'tickangle': -45},
        yaxis_title='Median Prevailing Wage'
    )
    return fig


@app.callback(
    Output('top20-employers-scatter', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_top20_employers_scatter(_):
    # Scatter plot: x=median wage, y=count, marker size=count, label=EMPLOYER_NAME (hover only)
    df = top_20_employers_merged.copy()
    # Only show text labels if median > 30k or count > 150k
    text_labels = [
        name if (median > 140E3 or count > 20E3 or median < 80E3) else ""
        for name, median, count in zip(df['EMPLOYER_NAME'], df['median'], df['COUNT'])
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['median'],
        y=df['COUNT'],
        mode='markers+text',
        marker=dict(
            size=df['COUNT'] / df['COUNT'].max() * 100 + 10,  # scale marker size
            color='royalblue',
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        text=text_labels,
        textposition='top center',
        hovertext=df['EMPLOYER_NAME'],
        hovertemplate="<b>%{hovertext}</b><br>Median Wage: %{x}<br>Applications: %{y}<extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        xaxis_title="Median Prevailing Wage",
        yaxis_title="Application Count",
        height=400,
        margin={"r":0,"t":0,"l":50,"b":0}
    )
    return fig

@app.callback(
    Output('top20-jobtitles-scatter', 'figure'),
    Input('top-employers-bar', 'figure')  # Dummy input to trigger update
)
def update_top20_jobtitles_scatter(_):
    # Scatter plot: x=median wage, y=count, marker size=count, label=JOB_TITLE
    df = top_20_job_titles_merged.copy()
    # Limit to only those with median wage >= 80k
    df = df[df['median'] >= 80000]
    # Only show text labels if median > 100k or count > 10k
    text_labels = [
        job if (median > 100000 or count > 10000) else ""
        for job, median, count in zip(df['JOB_TITLE'], df['median'], df['COUNT'])
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['median'],
        y=df['COUNT'],
        mode='markers+text',
        marker=dict(
            size=df['COUNT'] / df['COUNT'].max() * 100 + 10,  # scale marker size
            color='seagreen',
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        text=text_labels,
        textposition='top center',
        hovertemplate="<b>%{text}</b><br>Median Wage: %{x}<br>Applications: %{y}<extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        xaxis_title="Median Prevailing Wage",
        yaxis_title="Application Count",
        yaxis_type="log",
        height=600,
        margin={"r":0,"t":0,"l":50,"b":0}
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=False)
