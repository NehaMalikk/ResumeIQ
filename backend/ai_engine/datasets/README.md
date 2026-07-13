# Datasets

This directory stores training, validation, and test datasets for the HireMatch AI engine.

## Planned Structure

```
datasets/
├── raw/              # Original resume and JD files (gitignored)
├── processed/        # Cleaned and labeled datasets
├── golden/           # Curated benchmark set for regression testing
└── manifests/        # Dataset version manifests and metadata
```

## Guidelines

- **Do not commit** raw resume files containing real PII.
- Use anonymized or synthetic data for development.
- Version datasets with semantic versioning (e.g., `v1.0.0`).
- Document dataset schema in manifest JSON files.

## TODO

- [ ] Define dataset schema for resume-JD pairs
- [ ] Create synthetic dataset generator for development
- [ ] Establish data labeling workflow for skill annotations
