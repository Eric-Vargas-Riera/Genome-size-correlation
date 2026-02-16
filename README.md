# Genome-size-correlation

This repository contains the Python script used to compute Pearson correlations and generate regression plots for the comparative genomics analysis of Teleost and Pleuronectiformes species.

*The script in this repository has been completly generated with IA (Claude Sonnet 4.5)*

Author: Èric Vargas Riera
Course: Genomics
Year: 2026





# Instructions


📊 Description

This script generates 3 vertically stacked scatter plots analyzing the relationship between genome size and other genomic features in fish species.

Generated Plots

A) Genome Size vs Intron Length

B) Genome Size vs Intron Count

C) Genome Size vs Gene Count

✨ Features

✅ 3 vertically stacked scatter plots
✅ Correlation coefficient (R) for each plot
✅ Coefficient of determination (R²) for each plot
✅ Linear regression line in each plot
✅ Regression equation displayed on each plot
✅ Points colored by fish group:

🔴 Pleuronectiformes: Red (#FF6B6B)

🔵 Teleost: Turquoise (#4ECDC4)
✅ Command-line arguments for flexibility

📦 Requirements
pip install pandas matplotlib numpy scipy

🚀 Usage
Basic usage (uses GNM.csv by default):
python fish_scatter_plots.py

Specify a CSV file:
python fish_scatter_plots.py my_file.csv

Specify output file:
python fish_scatter_plots.py GNM.csv --output results.png


Or using the short form:

python fish_scatter_plots.py GNM.csv -o results.png

Specify a different delimiter:
python fish_scatter_plots.py data.csv --delimiter ","


Or using the short form:

python fish_scatter_plots.py data.csv -d ","

Show help:
python fish_scatter_plots.py --help

📋 Arguments
Argument	Short Form	Description	Default
csv_file	-	CSV file containing the data	GNM.csv
--output	-o	Output filename	fish_analysis.png
--delimiter	-d	CSV delimiter	;
📄 CSV Format

The script expects a CSV file with the following special structure:

Species;Teleost;;;Pleuronectiformes;;...
;A. polyacantus;A. latus;...species...
Genome Size (Mb);956,7;685,1;470,2;...
Gene count;29862;29897;25551;...
Intron count;269984;284477;242169;...
Intron length;2826;2000;1279;...


Format characteristics:

First row: indicates the group (Teleost or Pleuronectiformes)

Second row: species names

Remaining rows: genomic metrics (Genome Size, Gene count, Intron count, Intron length)

Delimiter: semicolon (;)

Decimals: comma (,) — automatically converted to dot

📊 Statistical Information

For each plot, the script calculates:

Regression equation: y = mx + b

R (Pearson correlation coefficient): measures the strength of linear association (-1 to 1)

R² (Coefficient of determination): proportion of variance explained (0 to 1)

🎨 Code Customization
Change colors

Modify the color dictionary:

colors = {'Pleuronectiformes': '#FF6B6B', 'Teleost': '#4ECDC4'}

Adjust figure size
fig, axes = plt.subplots(3, 1, figsize=(10, 12))  # (width, height)

Change output resolution
plt.savefig(args.output, dpi=300, bbox_inches='tight')  # Modify dpi

🔧 Troubleshooting
Error: FileNotFoundError
FileNotFoundError: [Errno 2] No such file or directory: 'GNM.csv'


Solution: Make sure the CSV file is in the same directory or specify the full path:

python fish_scatter_plots.py "C:\full\path\to\GNM.csv"

Error: Required columns not found

Solution: The script automatically searches for columns containing:

"genome" and "size" → Genome Size

"intron" and "length" → Intron Length

"intron" and "count" → Intron Count

"gene" and "count" → Gene Count

Verify that your CSV includes columns with these keywords.

Error: Empty plots or missing data

Solution: Ensure that the first row of the CSV contains "Teleost" or "Pleuronectiformes" for each species.

📝 Examples
Example 1: Full analysis with custom output
python fish_scatter_plots.py GNM.csv -o genomic_analysis_2026.png

Example 2: CSV with comma delimiter
python fish_scatter_plots.py fish_data.csv -d "," -o results.png

Example 3: View help and then run
Show help first
python fish_scatter_plots.py --help

Then run
python fish_scatter_plots.py

📄 Output

The script generates:

Console output: Information about processed species and detected columns

PNG file: High-resolution image (300 DPI) with the 3 plots

Interactive window: Matplotlib visualization (can be closed)

🎯 Example Console Output
Data loaded: 18 species
Teleost: 10
Pleuronectiformes: 8

Detected columns:
  Genome Size: Genome Size (Mb)
  Intron Length: Intron length
  Intron Count: Introns count
  Gene Count: Gene count

👨‍💻 Author

Script developed for fish genomic analysis – February 2026
