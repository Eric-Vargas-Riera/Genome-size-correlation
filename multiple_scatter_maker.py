import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import argparse
import sys

parser = argparse.ArgumentParser(description='Generar scatter plots de análisis de especies de peces')
parser.add_argument('--input', '-i', default='GNM.csv', 
                    help='Archivo CSV con los datos (por defecto: GNM.csv)')
parser.add_argument('--output', '-o', default='fish_analysis.png',
                    help='Nombre del archivo de salida (por defecto: fish_analysis.png)')
parser.add_argument('--delimiter', '-d', default=';',
                    help='Delimitador del CSV (por defecto: ;)')
args = parser.parse_args()

try:
    df_raw = pd.read_csv(args.input, delimiter=args.delimiter, header=None)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{args.input}'")
    sys.exit(1)

fish_types_row = df_raw.iloc[0, 1:].values
fish_types_filled = pd.Series(fish_types_row).fillna(method='ffill').values
species_names = df_raw.iloc[1, 1:].values
metrics = df_raw.iloc[2:, 0].values
data_values = df_raw.iloc[2:, 1:].values

df = pd.DataFrame(data_values.T, columns=metrics)
df['Species'] = species_names
df['Type'] = fish_types_filled

for col in metrics:
    df[col] = df[col].apply(lambda x: str(x).replace(',', '.') if pd.notna(x) and str(x).strip() != '' else np.nan)
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Type'] = df['Type'].astype(str).str.strip()
df['Species'] = df['Species'].astype(str).str.strip()
df = df[df['Type'].notna()]
df = df[df['Type'] != '']
df = df[df['Type'] != 'nan']
df = df[df['Type'].isin(['Teleost', 'Pleuronectiformes'])]
df = df[df['Species'].notna()]
df = df[df['Species'] != '']
df = df[df['Species'] != 'nan']

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle('Correlation Analysis in Fish Species', fontsize=16, fontweight='bold')

colors = {'Pleuronectiformes': '#FF6B6B', 'Teleost': '#4ECDC4'}

def plot_scatter_with_regression(ax, x_data, y_data, fish_types, x_label, y_label, title, show_xlabel=True):
    mask_pleuro = fish_types == 'Pleuronectiformes'
    mask_teleost = fish_types == 'Teleost'
    
    ax.scatter(x_data[mask_pleuro], y_data[mask_pleuro], 
               c=colors['Pleuronectiformes'], label='Pleuronectiformes', 
               alpha=0.6, edgecolors='black', s=80)
    ax.scatter(x_data[mask_teleost], y_data[mask_teleost], 
               c=colors['Teleost'], label='Teleost', 
               alpha=0.6, edgecolors='black', s=80)
    
    valid_mask = ~(np.isnan(x_data) | np.isnan(y_data))
    x_clean = x_data[valid_mask]
    y_clean = y_data[valid_mask]
    
    if len(x_clean) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
        correlation, _ = stats.pearsonr(x_clean, y_clean)
        
        x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
        y_line = slope * x_line + intercept
        
        ax.plot(x_line, y_line, 'r--', linewidth=2, label='Linear Regression')
        
        equation_text = f'y = {slope:.4f}x + {intercept:.4f}'
        r_squared_text = f'R² = {r_value**2:.4f}'
        r_text = f'R = {r_value:.4f}'
        
        ax.text(0.05, 0.95, equation_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax.text(0.05, 0.88, r_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax.text(0.05, 0.81, r_squared_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    if show_xlabel:
        ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
    ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, linestyle='--')

try:
    genome_col = next((col for col in df.columns if 'genome' in col.lower() and 'size' in col.lower()), None)
    gene_size_col = next((col for col in df.columns if 'gene' in col.lower() and 'real' in col.lower()), None)
    exon_count_col = next((col for col in df.columns if 'exon' in col.lower() and 'count' in col.lower()), None)
    intron_count_col = next((col for col in df.columns if 'intron' in col.lower() and 'count' in col.lower()), None)
    
    if not all([genome_col, gene_size_col, exon_count_col, intron_count_col]):
        print("Error: No se pudieron encontrar todas las columnas necesarias.")
        sys.exit(1)
    
    genome_size = df[genome_col].values
    gene_size = df[gene_size_col].values
    exon_count = df[exon_count_col].values
    intron_count = df[intron_count_col].values
    fish_type = df['Type'].values
    
    plot_scatter_with_regression(axes[0], genome_size, gene_size, fish_type,
                                 'Genome Size (Mb)', 'Gene Size (bp)',
                                 '', show_xlabel=False)
    
    plot_scatter_with_regression(axes[1], genome_size, exon_count, fish_type,
                                 'Genome Size (Mb)', 'Exon Count',
                                 '', show_xlabel=False)
    
    plot_scatter_with_regression(axes[2], genome_size, intron_count, fish_type,
                                 'Genome Size (Mb)', 'Intron Count',
                                 '', show_xlabel=True)
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.0)  # Ajustar separación: 0.0=juntos, 0.3=separados
    
    plt.savefig(args.output, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado como '{args.output}'")
    
    plt.show()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
