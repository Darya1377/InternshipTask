import requests
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns


def draw_plots(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    if not os.path.exists('plots'):
        os.makedirs('plots')

    plot_paths = []
    plot_path = f'plots/heatmap.png'
    df_corr = df.corr(numeric_only=True)
    sns.heatmap(df_corr, annot=True, fmt='.2f', cmap='RdYlGn', annot_kws={'size': 8})
    plt.savefig(plot_path, bbox_inches='tight')
    plot_paths.append(plot_path)

    plt.figure()
    plot_path = f'plots/scatterplot.png'
    sns.scatterplot(data=df, x="max", y="min", hue="gt_corners", palette="Set1")
    plt.title("Scatterplot gt_corners", fontsize=18)
    plt.savefig(plot_path, bbox_inches='tight')
    plot_paths.append(plot_path)

    plt.figure()
    plot_path = f'plots/pairwise_relationships.png'
    sns.pairplot(data=df[df.columns[3:]], diag_kind='kde')
    plt.title("Pairwise relationships", fontsize=18)
    plt.savefig(plot_path, bbox_inches='tight')
    plot_paths.append(plot_path)

    return plot_paths


def main():

    url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    response = requests.get(url)

    if response.status_code == 200:
        with open('data.json', 'wb') as file:
            file.write(response.content)
    else:
        print('Не удалось загрузить JSON файл')

    draw_plots('data.json')


if __name__ == '__main__':
    main()
