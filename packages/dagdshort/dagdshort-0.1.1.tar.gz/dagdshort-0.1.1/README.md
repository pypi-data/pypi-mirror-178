# dagdshort
**dagdshort** is a Python based multithreaded URL shortener with a memory-cache. It uses the [da.gd](https://da.gd/) service.

As a disclaimer, this is an unofficial package and it has no association with da.gd. If you use this package extensively, making a financial donation to da.gd is encouraged.

Other operations are outside the scope of this package.

[![cicd badge](https://github.com/impredicative/dagdshort/workflows/cicd/badge.svg?branch=master)](https://github.com/impredicative/dagdshort/actions?query=workflow%3Acicd+branch%3Amaster)

## Links
| Caption   | Link                                                |
|-----------|-----------------------------------------------------|
| Repo      | https://github.com/impredicative/dagdshort/         |
| Changelog | https://github.com/impredicative/dagdshort/releases |
| Package   | https://pypi.org/project/dagdshort/                 |

## Requirements

### Python
Python ≥3.9 is required. Any older version of Python will not work.

## Usage
To install the package, run:

    $ pip install dagdshort

Usage examples:
```python
>>> import dagdshort

# Setup
>>> shortener = dagdshort.Shortener(user_agent_suffix='<YourGitUsername>/<YourGitRepoName>', max_cache_size=256)

# Shorten
>>> long_urls = ['https://github.com/impredicative/dagdshort/', 'https://pypi.org/project/dagdshort/']
>>> shortener.shorten_urls(long_urls)
{'https://github.com/impredicative/dagdshort/': 'https://da.gd/W9s06',
 'https://pypi.org/project/dagdshort/': 'https://da.gd/KtGTB'}

# Show cache info
>>> shortener.cache_info
{'Shortener._shorten_url': CacheInfo(hits=0, misses=2, maxsize=256, currsize=2)}
```

To obtain the fastest response, URLs must be shortened together in a batch as in the examples above.
Up to 8 concurrent workers are automatically used. The max limit can, if really necessary, be changed by setting `config.MAX_WORKERS` before initializing the shortener.
