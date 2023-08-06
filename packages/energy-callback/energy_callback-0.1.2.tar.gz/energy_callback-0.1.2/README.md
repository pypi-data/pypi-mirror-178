# 2022-B : Energy and Performance tracking with Tensorflow

## Using Tensorflow and Tensorboard
TODO add usage for tensorflow and tensorboard to ensure users have their code setup in the correct format
## Energy Callback Python Package
Install the python package for generating the callback function

`$pip install energy-callback`


### Usage
Import the package 

` import energy_callback`

Create a callback object 

`callback = energy_callback.Callback() `

Args:
- country (str): Country for estimating gCO2e per kWh Default: 'United Kingdom'
- csv_path (str): Filepath to csv file to log results. Default: './tb_experiment_1.csv'

For example to change the country to France and the csv path to 'my_csv.csv':

`callback = energy_callback.Callback('France', 'my_csv.csv')
`

Input the callback object into the model.fit function

```
history = model.fit(x=x_train,
          y=y_train,
          epochs=5,
          validation_data=(x_test, y_test),
          callbacks=[tensorboard_callback, callback])
```

Use callback.get_csv() to generate csv containing performance and energy values for each epoch of training. Make sure to pass in the history value from model.fit to include the tensorboard model performance metrics in the csv. Default csv filepath is 'tb_experiment_1.csv'

`callback.get_csv(history)`

### Energy Calculations
The package will check if it can access the intel-rapl directory and use the values here for
calculating joules otherwise it will use the [python-energy-monitor](https://github.com/mattclifford1/python-energy-monitor) package 

To estimate the co2e value the tracker uses the carbon intensity for the given country and uses the corresponding gco2/kWh value from here https://ourworldindata.org/grapher/carbon-intensity-electricity
The default value is United Kingdom. 