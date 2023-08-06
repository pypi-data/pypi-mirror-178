# pydantic custom types
A collection of custom types for pydantic  
https://github.com/pydantic/pydantic

Useful for validation input parameters for infrastructure pipelines when building kubernetes apps/clusters

## Requirements

`python >= 3.10`

## Installation

`pip install pydantic-custom-types`

## Examples

```python
from pydantic import BaseModel
from pydantic_custom_types.kubernetes import NamespaceName, SecretName

class K8sNamespace(BaseModel):
    # These string types only allow: lowercase/numbers/dash, cannot start with dash/number
    # NamepaceName has linit at 63 characters
    # SecretName has linit at 63 characters
    name: NamespaceName 
    secret_name: SecretName

# will pass
K8sNamespace(
    name="my-namespace",
    secret_name="my-secret"
)

# will not pass
K8sNamespace(
    name="-0mynameSpace",
    secret_name="0mysecret"
)
```