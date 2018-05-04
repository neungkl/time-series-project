Time Series Project
===

A time series project during studying.

👉 Task: [task.pdf](document/task.pdf) <br>
👉 Report: [report.pdf](document/report.pdf)

## Run Script

To run the code, the dataset must be pre-load before starts the script.
All dataset available on [http://www.cs.ucr.edu/~eamonn/time_series_data/](http://www.cs.ucr.edu/~eamonn/time_series_data/)

Please firstly extract the dataset to `data` folder.

Then, starts the docker by:

```
docker-compose up
```

To run avering method, enter `localhost:8888` and run scipt inside Jupyter Lab.

If you would like to run DTW classification:

```
docker exec -it time-series-project_go_1 bash
cd src/task-1/
chmod +x ./run-dtw.sh
./run-dtw.sh
```

## Project Members

- Kosate Limpongsa [(@neungkl)](https://github.com/neungkl/time-series-project)
- Sirinthra Chantharaj [(@sirinthra-cc)](https://github.com/sirinthra-cc)