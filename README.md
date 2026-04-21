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

The example is in `examples/basic/__main__.py`.

```bash
cd examples/basic
pulumi preview
```

From repo root you can also run:

```bash
pulumi preview
```
