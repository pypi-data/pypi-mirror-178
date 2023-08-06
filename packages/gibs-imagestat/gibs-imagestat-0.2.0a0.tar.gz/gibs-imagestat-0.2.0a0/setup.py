# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dag']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'fastapi>=0.87,<0.88',
 'lxml>=4.9.1,<5.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'starlette>=0.21,<0.22',
 'urllib3>=1.26.8,<2.0.0',
 'uvicorn>=0.19,<0.20',
 'xarray>=2022.3.0,<2023.0.0']

setup_kwargs = {
    'name': 'gibs-imagestat',
    'version': '0.2.0a0',
    'description': 'Application capable of computing statistics on GIBS images',
    'long_description': '# gibs-imagestat\nCalculate statistics on GIBS hosted imagery\n\n## Initial Implementation Use Cases & Exchange Data Specification\n\n### 1. Imagery Spatial Summary Statistics – single (current) Time Step. \n**Input Parameters** (from Worldview UI passed to Imagery Analysis tool for execution):\n- Spatial Bounding Box: Lat_min, Lat_max, Lon_min, Lon_max \xa0(in -90 to 90, -180 to 180 format)\n- Time range: Time_min, Time_max (to keep this general, but for this particular use case just the current time step from the Worldview data picker will be passed into Imagery Analysis tool for imagery value extraction and analysis. \xa0ie. Time_min = Time_max\n- Satellite Dataset(s) shortname: \xa0list of one or more imagery dataset shortnames selected and being visualized in Worldview for imagery value extraction/analysis in Imagery Analysis tool\n- Analysis Type: “Spatial summary statistics” (standard label that we will define to describe the analysis to be conducted for handling by both Imagery Analysis tool and Worldview).\n- Analysis sub-Type: “Time Step” (standard label that we will define to describe the analysis to be conducted for handling by both Imagery Analysis tool and Worldview)\n- Analysis shortname: “spatial_summary_stats”\n\nFor this use case “Spatial summary – Time Step” Imagery Analysis tool will extract values for each specified imagery dataset for just the single time over the spatial domain defined. \xa0Imagery Analysis tool will then compute and return mean, variance, standard error and pixel count statistics, plus a frequency distribution of geophysical values for each specified imagery dataset again for just the single time for the spatial domain specified.\n\n**Output Data** (passed from Imagery Analysis tool to Worldview -UI for display):\n- Numerical statistical summary data: Spatial mean, variance, standard error and pixel count for each dataset for tabular output.\n- Summary plot data: frequency distribution of geophysical values for each dataset for charting as one or more histograms.\n\n### 2. Imagery Spatial Summary Statistics – Time Range (summary over multiple time steps of imagery).\n**Input Parameters** (from Worldview UI passed to Imagery Analysis tool for execution):\n- Spatial Bounding Box: Lat_min, Lat_max, Lon_min, Lon_max \xa0(in -90 to 90, -180 to 180 format)\n- Time range: Time_min, Time_max (user to specify a start and end time range over which the spatio-temporal summary statistics will be computed)\n- Satellite Dataset(s) shortname: \xa0list of one or more imagery dataset shortnames selected and being visualized in Worldview for imagery value extraction/analysis in Imagery Analysis tool\n- Analysis Type: “Spatial summary statistics”\n- Analysis sub-Type: “Time Range”\n- Analysis shortname: “spatiotemporal_summary_stats”\n\nFor this use case “Spatial summary – Time Range” Imagery Analysis tool will extract values for each specified imagery dataset for the spatial domain defined for the range of times. \xa0Imagery Analysis tool will then compute and return a single set of mean, variance, standard error and pixel count statistics, plus a frequency distribution of geophysical values for each specified imagery dataset again across time for the spatial domain specified.\n\n**Output Data** (passed from Imagery Analysis tool to Worldview -UI for display):\n- Numerical statistical summary data: Spatial mean, variance, standard error and pixel count that integrated across time for each dataset for tabular output.\n- Summary plot data: frequency distribution of geophysical values for each dataset for charting as one or more histograms.\n\n\n\n',
    'author': 'podaac-tva',
    'author_email': 'podaac-tva@jpl.nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/podaac/gibs-imagestat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
