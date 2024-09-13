import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = 'Cluster Visualisation',
    page_icon = '📊',
    layout = 'wide',                   # Use full-width layout
    initial_sidebar_state = 'collapsed' # Sidebar state: "expanded", "collapsed", "auto"
)

if 'initialised' not in st.session_state:
    st.session_state['Original Dataset'] = pd.read_csv(r'./data/sampled_srs_preprocessed_knn_n3.csv', index_col = 'CUST_ID')
    st.session_state['PCA Dataset'] = pd.read_csv(r'./data/knn3_pca.csv', index_col = 'CUST_ID')
    st.session_state['t-SNE Dataset'] = pd.read_csv(r'./data/knn3_tsne3.csv', index_col = 'CUST_ID')
    st.session_state['UMAP Dataset'] = pd.read_csv(r'./data/knn3_umap3.csv', index_col = 'CUST_ID')

    st.session_state['Cluster Dataset'] = pd.read_csv(r'./data/clusters.csv', index_col = 'CUST_ID')
    st.session_state['Scores Dataset'] = pd.read_csv(r'./data/scores.csv', index_col = 0)

    st.session_state.model_params = {
        'agg': {
            'Number of Clusters': 7,
            'Linkage Method': 'Ward'
        },
        'ms': {
            'Quantile': 0.2
        },
        'birch': {
            'Threshold': 0.9,
            'Branching Factor': 50,
            'Number of Clusters': 5
        },
        'hdbscan': {
            'Minimum Cluster Size': 40,
            'Minimum Samples': 6
        },
        'optics': {
            'Minimum Samples': '120',
            'Xi': '0.005',
        }
    }

    st.session_state.initialised = True

# Title for the app
st.title('Cluster Visualisation', anchor = False)

# Step 1: Model Selection
st.multiselect(
    label = 'Select Your Favourite Models:',
    options = ['Agglomerative', 'Mean Shift', 'BIRCH', 'HDBSCAN', 'OPTICS'],
    max_selections = 2,
    help = 'Select and Compare Up to 2 Models',
    placeholder = 'Select Up to 2 Models',
    key = 'selected_models'
)

if st.session_state.selected_models:
    selected_models = st.session_state.selected_models
    sections = st.columns(len(selected_models))

    for model, section in zip(selected_models, sections):
        with section:
            with st.expander(f'{model} Model Hyperparameter Tuning'):
                if model == 'Agglomerative':
                    ncluster_slider = st.slider(
                        label = 'Number of Clusters',
                        min_value = 2,
                        max_value = 10,
                        value = st.session_state.model_params['agg']['Number of Clusters'],
                        step = 1
                    )

                    linkage_slider = st.select_slider(
                        label = 'Linkage Method',
                        options = ['Ward', 'Complete', 'Average', 'Single'],
                        value =  st.session_state.model_params['agg']['Linkage Method']
                    )

                    st.session_state.model_params['agg']['Number of Clusters'] = ncluster_slider
                    st.session_state.model_params['agg']['Linkage Method'] = linkage_slider
                elif model == 'Mean Shift':
                    quantile_slider = st.slider(
                        label = 'Quantile',
                        min_value = 0.1,
                        max_value = 0.5,
                        value = st.session_state.model_params['ms']['Quantile'],
                        step = 0.1
                    )

                    st.session_state.model_params['ms']['Quantile'] = quantile_slider
                elif model == 'BIRCH':
                    threshold_slider = st.slider(
                        label = 'Threshold',
                        min_value = 0.1,
                        max_value = 0.9,
                        value = st.session_state.model_params['birch']['Threshold'],
                        step = 0.2
                    )

                    branchingfactor_slider = st.slider(
                        label = 'Branching Factor',
                        min_value = 10,
                        max_value = 50,
                        value = st.session_state.model_params['birch']['Branching Factor'],
                        step = 10
                    )

                    nclusters_slider = st.slider(
                        label = 'Number of Clusters',
                        min_value = 2,
                        max_value = 6,
                        value = st.session_state.model_params['birch']['Number of Clusters'],
                        step = 1
                    )

                    st.session_state.model_params['birch']['Threshold'] = threshold_slider
                    st.session_state.model_params['birch']['Branching Factor'] = branchingfactor_slider
                    st.session_state.model_params['birch']['Number of Clusters'] = nclusters_slider
                elif model == 'HDBSCAN':
                    minclustersize_slider = st.slider(
                        label = 'Minimum Cluster Size',
                        min_value = 5,
                        max_value = 50,
                        value = st.session_state.model_params['hdbscan']['Minimum Cluster Size'],
                        step = 5
                    )

                    minsamples_slider = st.slider(
                        label = 'Minimum Samples',
                        min_value = 5,
                        max_value = 10,
                        value = st.session_state.model_params['hdbscan']['Minimum Samples'],
                        step = 1
                    )

                    st.session_state.model_params['hdbscan']['Minimum Cluster Size'] = minclustersize_slider
                    st.session_state.model_params['hdbscan']['Minimum Samples'] = minsamples_slider
                elif model == 'OPTICS':
                    minsamples_slider = st.select_slider(
                        label = 'Minimum Samples',
                        options = ['30', '60', '80', '120', '140'],
                        value = st.session_state.model_params['optics']['Minimum Samples'],
                    )

                    xi_slider = st.select_slider(
                        label = 'Xi',
                        options = ['0.0005', '0.005', '0.01', '0.02', '0.05'],
                        value = st.session_state.model_params['optics']['Xi'],
                    )

                    st.session_state.model_params['optics']['Minimum Samples'] = minsamples_slider
                    st.session_state.model_params['optics']['Xi'] = xi_slider

if st.session_state.selected_models:
    plot_tab, score_tab = st.tabs(
        tabs = ['📈 Charts', '🎯 Scores']
    )

    with plot_tab:
        # Step 2: Dataset Selection
        with st.expander('Dataset'):
            st.radio(
                label = "Select a dataset:",
                options = ['Original Dataset', 'PCA Dataset', 't-SNE Dataset', 'UMAP Dataset'],
            horizontal = True,
            captions = ['No changes', 'Principal Component Analysis', 't-Stochastic Neighbouring Embedding', 'Uniform Manifold Approximation and Projection (UMAP)'],
            index = None,
            key = 'selected_dataset')

        if 'selected_dataset' not in st.session_state:
            st.session_state.selected_dataset = None

        # Step 3: Column Selection
        if st.session_state.selected_dataset:
            st.multiselect(
                label = 'Select your favourite features:',
                options = st.session_state[st.session_state.selected_dataset].columns,
                max_selections = 3,
                help = 'Select up to 3 features to compare',
                placeholder = 'Select up to 2 features',
                key = 'selected_features')

        # Step 4: Display Results
        if 'selected_features' in st.session_state and st.session_state.selected_features and st.session_state.selected_dataset and st.session_state.selected_models:
            sections = st.columns(len(st.session_state.selected_models))

            selected_features = st.session_state.selected_features
            df_selected = st.session_state[st.session_state.selected_dataset][selected_features]
            for model, section in zip(st.session_state.selected_models, sections):
                with section:

                    # Need plot graphs here
                    model_params = st.session_state.model_params[
                        'agg' if model == 'Agglomerative' else
                        'ms' if model == 'Mean Shift' else
                        'birch' if model == 'BIRCH' else
                        'hdbscan' if model == 'HDBSCAN' else
                        'optics'
                    ]

                    if model == 'Agglomerative':
                        df_clusters = (
                            st.session_state['Cluster Dataset'][[f'agg_ncluster{model_params["Number of Clusters"]}_linkage{model_params["Linkage Method"].lower()}']]
                            .rename(columns = {f'agg_ncluster{model_params["Number of Clusters"]}_linkage{model_params["Linkage Method"].lower()}': 'cluster'})
                        )
                    elif model == 'Mean Shift':
                        df_clusters = (
                            st.session_state['Cluster Dataset'][[f'ms_quantile{model_params["Quantile"]}']]
                            .rename(columns = {f'ms_quantile{model_params["Quantile"]}': 'cluster'})
                        )
                    elif model == 'BIRCH':
                        df_clusters = (
                            st.session_state['Cluster Dataset'][[f'birch_threshold{model_params["Threshold"]}_factor{model_params["Branching Factor"]}_ncluster{model_params["Number of Clusters"]}']]
                            .rename(columns = {f'birch_threshold{model_params["Threshold"]}_factor{model_params["Branching Factor"]}_ncluster{model_params["Number of Clusters"]}': 'cluster'})
                        )
                    elif model == 'HDBSCAN':
                        df_clusters = (
                            st.session_state['Cluster Dataset'][[f'hdbscan_mincluster{model_params["Minimum Cluster Size"]}_minsample{model_params["Minimum Samples"]}']]
                            .rename(columns = {f'hdbscan_mincluster{model_params["Minimum Cluster Size"]}_minsample{model_params["Minimum Samples"]}': 'cluster'})
                        )
                    elif model == 'OPTICS':
                        df_clusters = (
                            st.session_state['Cluster Dataset'][[f'optics_minsamp{model_params["Minimum Samples"]}_xi{model_params["Xi"]}']]
                            .rename(columns = {f'optics_minsamp{model_params["Minimum Samples"]}_xi{model_params["Xi"]}': 'cluster'})
                        )

                    chart_data = pd.concat([df_selected, df_clusters], axis = 1)

                    if len(selected_features):
                        with st.container(height = 500 if len(selected_features) == 1 else 700, border = True):
                            if len(selected_features) == 1:
                                # Create a scatter plot to show the distribution of the feature with colors for clusters
                                fig = px.strip(
                                    chart_data,
                                    x = selected_features[0],
                                    y = 'cluster',
                                    color = 'cluster',
                                    title = f'1D Clustering Visualisation ofr {model}',
                                    height = 400
                                )

                                fig.update_traces(marker = dict(size = 8))
                            elif len(selected_features) == 2:
                                fig = px.scatter(
                                    chart_data,
                                    x = selected_features[0],
                                    y = selected_features[1],
                                    color='cluster',
                                    color_continuous_scale='cividis'
                                )

                                fig.update_layout(
                                    height = 650,
                                    title= f'2D Clustering Visualisation for {model}'
                                )

                                fig.update_traces(marker = dict(size = 5))
                            elif len(selected_features) == 3:
                                fig = px.scatter_3d(
                                    chart_data,
                                    x = selected_features[0],
                                    y = selected_features[1],
                                    z = selected_features[2],
                                    color = 'cluster',
                                    color_continuous_scale='inferno')

                                fig.update_layout(
                                    title = f'3D Clustering Visualisation for {model}',
                                    height = 660,
                                    scene = dict(
                                        xaxis_title= chart_data.columns[0],
                                        yaxis_title= chart_data.columns[1],
                                        zaxis_title= chart_data.columns[2]
                                    )
                                )

                                fig.update_traces(marker = dict(size = 2))

                            st.plotly_chart(fig, use_container_width=True)

    with score_tab:
        if st.session_state.selected_models:
            sections = st.columns(len(st.session_state.selected_models))
            selected_models = st.session_state.selected_models

            selected_model_params = {}
            df_score = pd.DataFrame()
            for model in selected_models:
                selected_model_params[model] = st.session_state.model_params[
                    'agg' if model == 'Agglomerative' else
                    'ms' if model == 'Mean Shift' else
                    'birch' if model == 'BIRCH' else
                    'hdbscan' if model == 'HDBSCAN' else
                    'optics'
                ]

                if model == 'Agglomerative':
                    df_score[model] = st.session_state['Scores Dataset'][f'agg_ncluster{selected_model_params[model]["Number of Clusters"]}_linkage{selected_model_params[model]["Linkage Method"].lower()}']
                elif model == 'Mean Shift':
                    df_score[model] = st.session_state['Scores Dataset'][f'ms_quantile{selected_model_params[model]["Quantile"]}']
                elif model == 'BIRCH':
                    df_score[model] = st.session_state['Scores Dataset'][f'birch_threshold{selected_model_params[model]["Threshold"]}_factor{selected_model_params[model]["Branching Factor"]}_ncluster{selected_model_params[model]["Number of Clusters"]}']
                elif model == 'HDBSCAN':
                    df_score[model] = st.session_state['Scores Dataset'][f'hdbscan_mincluster{selected_model_params[model]["Minimum Cluster Size"]}_minsample{selected_model_params[model]["Minimum Samples"]}']
                elif model == 'OPTICS':
                    df_score[model] = st.session_state['Scores Dataset'][f'optics_minsamp{selected_model_params[model]["Minimum Samples"]}_xi{selected_model_params[model]["Xi"]}']

            for model, section in zip(selected_models, sections):
                with section:
                    st.header(f'{model}', divider = 'rainbow')

                    sub_sections = st.columns(len(selected_model_params[model]))

                    for i, key in enumerate(selected_model_params[model]):
                        with sub_sections[i]:
                            st.metric(label = f'**{key}**', value =f'{selected_model_params[model][key]}')

                    st.divider()

                    silhoutte_scores = (df_score[model].values[0], df_score.loc[:, df_score.columns != model].values[0])
                    db_scores = (df_score[model].values[1], df_score.loc[:, df_score.columns != model].values[1])
                    ch_scores = (df_score[model].values[2], df_score.loc[:, df_score.columns != model].values[2])
                    if(len(selected_models) > 1):
                        st.metric(label = '**Silhoutte Score**', value = round(silhoutte_scores[0], 4), delta = round((silhoutte_scores[0] - silhoutte_scores[1])[0], 4))
                        st.metric(label = '**Davies-Bouldin Index**', value = round(db_scores[0], 4), delta = round((db_scores[0] - db_scores[1])[0], 4))
                        st.metric(label = '**Calinski-Harabasz Score**', value = round(ch_scores[0], 4), delta = round((ch_scores[0] - ch_scores[1])[0], 4))
                    else:
                        st.metric(label = '**Silhoutte Score**', value = round(silhoutte_scores[0], 4))
                        st.metric(label = '**Davies-Bouldin Index**', value = round(db_scores[0], 4))
                        st.metric(label = '**Calinski-Harabasz Score**', value = round(ch_scores[0], 4))