### Data API

Link: http://air-visualization.wangzhao.ml:5678/query  

**POST**

Fotmat:

```
{
    "password": "vPybQ52DHBfWByPUQVLNuVM7LZyfZ88kNw7ucYHKbNxqXbU",
    "type": "daily", // Or "hourly", hourly to be finished (5 Nov)
    "start_time": "2013010100", // 10 digits, 2013010100 - 2013013100 supported
    "end_time": "2013010200"
}
```

Expected return: 

```
{
  "status": "Successful", // Or failed with reasons.
  "data": {
            "attribute": [attribute names, as which the data are following]
            "2013010100": [[..., ..., ..., ]
                           [..., ..., ..., ]
                                  .
                                  .
                                  .
                           [..., ..., ..., ]] // 13 values each objects.
            "2013010200": ...
                  .
                  .
          }
}

```
