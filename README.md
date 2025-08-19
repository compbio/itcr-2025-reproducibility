# README
# Acute Myeloid Leukemia Heatmap Analysis

This repository contains an R notebook for analyzing acute myeloid leukemia (AML) RNA-sequencing data and generating annotated heatmaps for gene expression clustering analysis.

## Overview

This analysis uses RNA-sequencing data from 19 AML model mice samples to create clustered heatmaps that visualize gene expression patterns. The data comes from [Shih et al., 2017](https://pubmed.ncbi.nlm.nih.gov/28193779/) and has been pre-processed by [refine.bio](https://www.refine.bio/).

The analysis focuses on:
- Gene expression clustering
- Sample clustering
- Treatment and mutation annotation
- High-variance gene selection

## Dataset Information

- **Source**: [refine.bio experiment SRP070849](https://www.refine.bio/experiments/SRP070849)
- **Samples**: 19 AML model mice samples
- **Data type**: RNA-sequencing (quantile normalized)
- **Mutations studied**: IDH2, TET2, and wild-type (WT)
- **Treatments**: 
  - IDH2 mutant AML: Vehicle or AG-221
  - TET2 mutant AML: Vehicle or 5-Azacytidine (Decitabine)

## Prerequisites

### R Version
- R >= 3.6.0 (recommended)

### Required R Packages
```r
# Core packages (auto-installed by script)
pheatmap
magrittr
readr
dplyr
tibble

# Optional for session info
sessioninfo
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd aml-heatmap-analysis
```

2. Install required R packages (if not already installed):
```r
# Run in R console
if (!("pheatmap" %in% installed.packages())) {
  install.packages("pheatmap", update = FALSE)
}
install.packages(c("magrittr", "readr", "dplyr", "tibble", "sessioninfo"))
```

## Usage

### Data Structure
Ensure your data files are organized as follows:
```
project/
├── data/
│   └── SRP070849/
│       ├── SRP070849.tsv          # Gene expression matrix
│       └── metadata_SRP070849.tsv  # Sample metadata
├── plots/                          # Generated plots (auto-created)
├── results/                        # Analysis results (auto-created)
└── analysis.Rmd                   # Main analysis notebook
```

### Running the Analysis

#### Option 1: Run the entire notebook
```r
# In RStudio
# Open the .Rmd file and click "Run All"
# Or knit to HTML: Ctrl+Shift+K (Windows) or Cmd+Shift+K (Mac)
```

#### Option 2: Run individual sections
```r
# Load libraries
library(pheatmap)
library(magrittr)
set.seed(12345)

# Read data
metadata <- readr::read_tsv("data/SRP070849/metadata_SRP070849.tsv")
expression_df <- readr::read_tsv("data/SRP070849/SRP070849.tsv") %>%
  tibble::column_to_rownames("Gene")

# Generate heatmap
variances <- apply(expression_df, 1, var)
upper_var <- quantile(variances, 0.75)
df_by_var <- data.frame(expression_df) %>%
  dplyr::filter(variances > upper_var)

# Create annotation
annotation_df <- metadata %>%
  dplyr::mutate(
    mutation = dplyr::case_when(
      startsWith(refinebio_title, "TET2") ~ "TET2",
      startsWith(refinebio_title, "IDH2") ~ "IDH2",
      startsWith(refinebio_title, "WT") ~ "WT",
      TRUE ~ "unknown"
    )
  ) %>%
  dplyr::select(refinebio_accession_code, mutation, refinebio_treatment) %>%
  tibble::column_to_rownames("refinebio_accession_code")

# Generate heatmap
heatmap_annotated <- pheatmap(
  df_by_var,
  cluster_rows = TRUE,
  cluster_cols = TRUE,
  show_rownames = FALSE,
  annotation_col = annotation_df,
  main = "Annotated Heatmap",
  colorRampPalette(c("deepskyblue", "black", "yellow"))(25),
  scale = "row"
)
```

### Command Examples

#### Basic heatmap generation:
```r
# Create simple heatmap without annotation
basic_heatmap <- pheatmap(df_by_var, scale = "row")
```

#### Customized heatmap:
```r
# Heatmap with custom colors and clustering
custom_heatmap <- pheatmap(
  df_by_var,
  cluster_rows = TRUE,
  cluster_cols = TRUE,
  clustering_distance_rows = "euclidean",
  clustering_method = "complete",
  color = colorRampPalette(c("blue", "white", "red"))(50),
  scale = "row"
)
```

#### Save heatmap to different formats:
```r
# Save as PNG
png("plots/my_heatmap.png", width = 800, height = 600)
print(heatmap_annotated)
dev.off()

# Save as PDF
pdf("plots/my_heatmap.pdf", width = 10, height = 8)
print(heatmap_annotated)
dev.off()
```

## Output Files

The analysis generates the following files:

### Results Directory (`results/`)
- `top_90_var_genes.tsv`: High-variance genes used for clustering

### Plots Directory (`plots/`)
- `aml_heatmap.png`: Annotated heatmap visualization

## Key Features

1. **Gene Filtering**: Selects genes with variance in the upper quartile (75th percentile)
2. **Sample Annotation**: Automatically annotates samples by mutation type and treatment
3. **Clustering**: Performs hierarchical clustering on both genes and samples
4. **Visualization**: Creates publication-ready heatmaps with color-coded annotations

## Customization Options

### Gene Selection Criteria
```r
# Select top 100 most variable genes
top_genes <- head(order(variances, decreasing = TRUE), 100)
df_top_genes <- expression_df[top_genes, ]

# Select genes with specific fold change
# (requires additional differential expression analysis)
```

### Color Schemes
```r
# Alternative color palettes
colors_viridis <- viridis::viridis(25)
colors_rcolorbrewer <- RColorBrewer::brewer.pal(11, "RdYlBu")
colors_custom <- c("navy", "white", "firebrick")
```

### Clustering Methods
```r
# Different clustering options
pheatmap(df_by_var,
  clustering_distance_rows = "correlation",  # or "euclidean", "maximum", etc.
  clustering_method = "ward.D2"             # or "complete", "average", etc.
)
```

## Troubleshooting

### Common Issues

1. **File not found errors**
   ```r
   # Check if files exist
   file.exists("data/SRP070849/SRP070849.tsv")
   file.exists("data/SRP070849/metadata_SRP070849.tsv")
   ```

2. **Memory issues with large datasets**
   ```r
   # Increase memory limit (Windows)
   memory.limit(size = 8000)  # 8GB
   
   # Use data.table for large files
   library(data.table)
   expression_df <- fread("data/SRP070849/SRP070849.tsv")
   ```

3. **Package installation issues**
   ```r
   # Install from Bioconductor if needed
   if (!require("BiocManager", quietly = TRUE))
     install.packages("BiocManager")
   BiocManager::install("package_name")
   ```

## Citation

If you use this analysis in your research, please cite:

- Original paper: Shih et al., 2017. PMID: 28193779
- refine.bio: [https://www.refine.bio/](https://www.refine.bio/)
- pheatmap package: Kolde R (2019). pheatmap: Pretty Heatmaps. R package version 1.0.12.

## License

This analysis is adapted from the [refine.bio-examples](https://alexslemonade.github.io/refinebio-examples/) repository by CCDL for ALSF and modified by Candace Savonen.

## Support

For questions about the analysis or issues with the code, please:
1. Check the troubleshooting section above
2. Review the original [refine.bio examples](https://alexslemonade.github.io/refinebio-examples/)
3. Open an issue in this repository