# DataCenter-Traces-Datasets
Pip package that makes available the datasets published in: https://github.com/alejandrofdez-us/DataCenter-Traces-Datasets. Please, check the mentioned repository for a deeper understanding.

## Alibaba 2018 machine usage
Processed from the original files found at:
https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2018

This repository dataset of machine usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field            | Type       | Label | Comment                                            |
+--------------------------------------------------------------------------------------------+
| cpu_util_percent | bigint     |       | [0, 100]                                           |
| mem_util_percent | bigint     |       | [0, 100]                                           |
| net_in           | double     |       | normarlized in coming network traffic, [0, 100]    |
| net_out          | double     |       | normarlized out going network traffic, [0, 100]    |
| disk_io_percent  | double     |       | [0, 100], abnormal values are of -1 or 101         |
+--------------------------------------------------------------------------------------------+
```

Three sampled datasets are found: average value of each column grouped every 10 seconds as original, and downsampled to 30 seconds and 300 seconds as well.
Every column includes the average utilization of the whole data center.

### Figures
Some figures were generated from these datasets

| ![cpu_util_percent_usage_days_1_to_8_grouped_10_seconds](https://user-images.githubusercontent.com/19324988/202569296-3bb72ad4-92e7-4200-a19d-ef6fc26722ce.png) |
|:--:|
|Figure: CPU utilization sampled every 10 seconds|

|![mem_util_percent_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202569501-7840c0a0-b4e8-4f7d-bb92-875e38c616e8.png)|
|:--:|
|Figure: Memory utilization sampled every 300 seconds|

|![net_in_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571345-79581b7f-c7cd-4690-aeea-56cc9f903396.png)|
|:--:|
|Figure: Net in sampled every 300 seconds|

|![net_out_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571570-d0067db7-3b75-4fb1-a866-8eeec78dd415.png)|
|:--:|
|Figure: Net out sampled every 300 seconds|

|![disk_io_percent_usage_days_1_to_8_grouped_300_seconds](https://user-images.githubusercontent.com/19324988/202571350-1f5defbf-6cb0-456a-b9d3-2f4d64a8021b.png)|
|:--:|
|Figure: Disk io sampled every 300 seconds|

## Google 2019 instance usage
Processed from the original dataset and queried using Big Query. More information available at:
https://research.google/tools/datasets/google-cluster-workload-traces-2019/

This repository dataset of instance usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field                         | Type       | Label | Comment                               |
+--------------------------------------------------------------------------------------------+
| cpu_util_percent              | double     |       | [0, 100]                              |
| mem_util_percent              | double     |       | [0, 100]                              |
| assigned_mem_percent          | double     |       | [0, 100]                              |
| avg_cycles_per_instruction    | double     |       | [0, _]                                |
+--------------------------------------------------------------------------------------------+
```
One sampled dataset is found: average value of each column grouped every 300 seconds as original.
Every column includes the average utilization of the whole data center.

### Figures
Some figures were generated from these datasets

|![cpu_usage_day_26](https://user-images.githubusercontent.com/19324988/202570580-6be32fd7-3e39-4e0a-bc8e-abda05c5edd2.png)|
|:--:|
|Figure: CPU usage day 26 sampled every 300 seconds|

|![mem_usage_day_26](https://user-images.githubusercontent.com/19324988/202570586-388eafcd-a70e-40d3-8a80-9cdab0ef6236.png)|
|:--:|
|Figure: Mem usage day 26 sampled every 300 seconds|

|![assigned_mem_day_26](https://user-images.githubusercontent.com/19324988/202570579-6d9744f8-97fb-42d2-bb9a-b9c7cf88bdb4.png)|
|:--:|
|Figure: Assigned mem day 26 sampled every 300 seconds|

|![cycles_per_instruction_day_26](https://user-images.githubusercontent.com/19324988/202570583-e28bae12-8540-4a69-845b-12cfc9be8c33.png)|
|:--:|
|Figure: Cycles per instruction day 26 sampled every 300 seconds|




## Azure v2 virtual machine workload
Processed from the original dataset. More information available at:
https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md

This repository dataset of instance usage includes the following columns:
```Bash
+--------------------------------------------------------------------------------------------+
| Field                         | Type       | Label | Comment                               |
+--------------------------------------------------------------------------------------------+
| cpu_usage                     | double     |       | [0, _]                                |
| assigned_mem                  | double     |       | [0, _]                                |
+--------------------------------------------------------------------------------------------+
```
One sampled dataset is found: sum value of each column grouped every 300 seconds as original.
Every column includes the total consumption of the whole data center virtual machines.

### Figures
Some figures were generated from these datasets

|![cpu_usage_month](https://user-images.githubusercontent.com/19324988/202569892-50ceb7d1-7892-4c36-bd81-ab2b3398bf58.png)|
|:--:|
|Figure: CPU total usage by virtual machines sampled every 300 seconds.|

|![assigned_mem_month](https://user-images.githubusercontent.com/19324988/202569860-c85fe1da-4604-435f-8315-7d6b828a8ba2.png)|
|:--:|
|Figure: Total assigned memory for virtual machines sampled every 300 seconds.|



## Installation

```Bash
pip install datacentertracesdatasets
```

## Usage

To load the original Alibaba's 2018 machine usage, with the mean usage of all machines for each timestamp (8 days, 10 seconds timestep) as a Pandas DataFrame:

```Python
from datacentertracesdatasets import loadtraces
alibaba_2018_original_machine_usage_df = loadtraces.get_trace(trace_name='alibaba2018', trace_type='machine_usage', stride_seconds=10)
```

If, instead of a Pandas DataFrame, a numpy NDArray is needed, the ```format``` parameter can be used:

```Python
azure_v2_machine_usage_ndarray = loadtraces.get_trace(trace_name='azure_v2', trace_type='machine_usage', stride_seconds=300, format='ndarray')
```

Or, for Google 2019 machine usage:
```Python
azure_v2_machine_usage_ndarray = loadtraces.get_trace(trace_name='google2019', trace_type='machine_usage', stride_seconds=300, format='ndarray')
```

In addition to the original Alibaba 2018 machine usage dataset, which has a 10-seconds timestep, two additional downsampled versions of 30 and 300 seconds timesteps are provided, which can be retrieved by using the ```stride_seconds``` argument:

```Python
alibaba_2018_machine_usage_300_timestep_df = loadtraces.get_trace(trace_name='alibaba2018', trace_type='machine_usage', stride_seconds=300, format='ndarray')
```

## Dataset metadata

The dataset structure and metadata can be retrieved with the ```get_dataset_info``` method:

```Python
dataset_info = get_dataset_info(trace_name='alibaba2018', trace_type='machine_usage', stride_seconds=300)
```

Which returns:

````Python
dataset_info = {
                "timestamp_frequency_secs": 300,
                "column_config": {
                    "cpu_util_percent": {
                        "column_index": 0,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "mem_util_percent": {
                        "column_index": 1,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "net_in": {
                        "column_index": 2,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "net_out": {
                        "column_index": 3,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    },
                    "disk_io_percent": {
                        "column_index": 4,
                        "y_axis_min": 0,
                        "y_axis_max": 100
                    }

                },
                "metadata": {
                    "fields": {
                        "cpu_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "mem_util_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "net_in": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "net_out": {
                            "type": "numerical",
                            "subtype": "float"
                        },
                        "disk_io_percent": {
                            "type": "numerical",
                            "subtype": "float"
                        }
                    }
                }
            }
````



Currently only Alibaba 2018's, Google 2019's and Azure_V2 (virtual) machine usage traces are available. In the future, we plan to add the following:
* Alibaba's 2018 batch_task workload trace.
* Google's 2019 batch_task workload trace.