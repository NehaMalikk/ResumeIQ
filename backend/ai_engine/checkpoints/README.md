# Model Checkpoints

This directory stores trained model artifacts and checkpoints for the HireMatch AI engine.

## Planned Structure

```
checkpoints/
├── embeddings/       # Sentence-transformer / embedding model weights
├── ner/              # Named entity recognition models
├── classifiers/      # Skill and section classification models
└── manifests/        # Checkpoint metadata (version, metrics, config)
```

## Guidelines

- **Do not commit** large model weight files to git.
- Track checkpoint metadata (hash, metrics, training config) in manifest files.
- Use consistent naming: `{model_name}-v{version}-{date}/`.
- Document required dependencies and input/output schemas per checkpoint.

## TODO

- [ ] Set up model registry integration (local or cloud)
- [ ] Define checkpoint loading interface in `inference/predictor.py`
- [ ] Add `.gitkeep` or manifest-only tracking for empty directories
