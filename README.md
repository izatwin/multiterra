# multiterra

Reusable Pulumi components for generalized network and VM provisioning.

## Library usage

```python
from multiterra import (
    GeneralizedImage,
    GeneralizedSubnet,
    GeneralizedVM,
    GeneralizedVPC,
)
```

Primary components:
- `GeneralizedVPC`
- `GeneralizedSubnet`
- `GeneralizedImage`
- `GeneralizedVM`

## Run the example

The Pulumi program that previously lived in `src/__main__.py` is now at `examples/basic/__main__.py`.

```bash
cd examples/basic
pulumi preview
```

From repo root you can also run:

```bash
pulumi preview
```

## Notes

- Current component provider implementation is AWS-only.
- `buckets/` remains a separate prototype app and is not part of the component library package.
