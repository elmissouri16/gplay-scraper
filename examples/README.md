# Examples

This folder contains example scripts demonstrating all methods for each of the 7 method types.

## Files

### 1. app_methods_example.py
Covers:
- `app_analyze()` - Get all data as dictionary
- `app_get_field()` - Get single field value
- `app_get_fields()` - Get multiple fields
- Manual formatting of selected fields using standard Python printing

### 2. search_methods_example.py
Covers:
- `search_analyze()` - Get all search results
- `search_get_field()` - Get one field across results
- `search_get_fields()` - Get multiple fields across results
- Custom display of titles and developers using the returned data

### 3. reviews_methods_example.py
Covers:
- `reviews_analyze()` - Get all reviews
- `reviews_get_field()` - Extract a single review field
- `reviews_get_fields()` - Extract multiple review fields
- Manual formatting of reviewer names and scores

### 4. developer_methods_example.py
Covers:
- `developer_analyze()` - Get all developer apps
- `developer_get_field()` - Extract one field from each app
- `developer_get_fields()` - Extract multiple fields from each app
- Custom display of app titles and scores

### 5. list_methods_example.py
Covers:
- `list_analyze()` - Get all top chart apps
- `list_get_field()` - Extract one field from top charts
- `list_get_fields()` - Extract multiple fields from top charts
- Manual formatting of chart results

### 6. similar_methods_example.py
Covers:
- `similar_analyze()` - Get all similar apps
- `similar_get_field()` - Extract one field from similar apps
- `similar_get_fields()` - Extract multiple fields from similar apps
- Manual formatting of similar app summaries

### 7. suggest_methods_example.py
Covers:
- `suggest_analyze()` - Get search suggestions
- `suggest_nested()` - Get nested suggestions
- Custom formatting of nested suggestions

## Running Examples

```bash
# Run any example
python examples/app_methods_example.py
python examples/search_methods_example.py
python examples/reviews_methods_example.py
python examples/developer_methods_example.py
python examples/list_methods_example.py
python examples/similar_methods_example.py
python examples/suggest_methods_example.py
```

## Note

These examples are simple demonstrations. For more advanced use cases, check the documentation in the `README/` folder.
