# sandpaper
Python module for table type data normalization

## Basic Usage

```python
from sandpaper import SandPaper

paper = SandPaper('my-sandpaper').strip(  # strip whitespace from column comment
    column_filter=r'comment'
).translate_text(                         # get group id from column group
    column_filter=r'group',
    from_regex=r'^group_(\d+)$',
    to_format='{0}'
).translate_date(                         # normalize date from column date
    column_filter=r'date',
    from_formats=['%Y-%m-%d', '%m-%d'],
    to_format='%c'
)

for result in s.apply('~/Downloads/exported_data.{1..3}.{csv,xls{,x}}'):
    # apply sandpaper rules to all files matching the brace expanded glob given
    print(result)
```
