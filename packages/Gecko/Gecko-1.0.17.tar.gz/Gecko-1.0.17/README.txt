=====
Gecko
=====

Gecko is a python based framework that gives users the ability to create a simple
IoT application with minimal development time.

### Using Gecko to run an applicaiton
Initialize your application with the `gecko init` command 
~~~
gecko init <your application name>
~~~

Follow the on screen prompts to define your attached sensors.

### Run your Gecko application
~~~
gecko run <your application name>
~~~

# I want to do something more advanced!
While the quickstart guide works well for a simple application, often times
an application will need to be a little smarter than just sending the voltage
from an analog pin every _n_ seconds.  In order to do this we will need to peel
a layer off of our gecko stack.  


# Using Gecko to Simulate data
Gecko can be used to simulate various data types.  The data types are defined 
in json format.  The following datatypes are currently supported:

 1. Linear
 2. Sinusoidal
 3. Random
 4. Weather ([openweathermap](http://openweathermap.org/))
 
All data object have the following characteristics:

 1. `name` -- Name of the data
 2. `report_rate` -- How often (In seconds) the data will be sent to Exosite
 3. `type` -- Type of data (See below)
 4. `data_characteristics` -- Characteristics of this particular datatype (See below)
 
Below is an example of an object representing a simulation of linear data:

~~~ Javascript
{ "simulated_data": {
    "name": "Linear Data",
    "report_rate": 1,
    "type": "linear",
    "data_characteristics": {
        "slope": 1,
        "offset": 4.5
    }
}
~~~
 
The type represented in the `type` key, determines what is in the `data_characteristics`
object.  

## Linear
The `data_characteristics` object of a `linear` data simulation has a `data_characteristics`
object that looks like the following:

~~~ Javascript
"data_characteristics": {
    "slope": 1,
    "offset": 4.5
}
~~~

 * `slope`
	 * Slope of the line in unit increments/second
 * `offset`
	 * The starting point of the data.

## Sinusoidal
The `data_characteristics` object of a `sinusoidal` data simulation has a `data_characteristics`
object that looks like the following:

~~~ Javascript
"data_characteristics": {
    "period": 1,
    "amplitude": 4.5,
    "offset": 12
}
~~~

 * `period`
	 * Period of the wave in seconds
 * `amplitude`
	 * Amplitude of the wave
 * `offset`
	 * offset of the wave off of zero

## Random
The `data_characteristics` object of a `random` data simulation has a `data_characteristics`
object that looks like the following:

~~~ Javascript
"data_characteristics": {
    "min": 1,
    "max": 4.5
}
~~~

 * `min`
	 * Minimum value of random data
 * `max`
	 * Maximum value of random data

## Weather (open_weather_map)
The `data_characteristics` object of an `open_weather_map` data simulation has a `data_characteristics`
object that looks like the following:

~~~ Javascript
"data_characteristics": {
    "city_id": 5037649,
    "api_key": "787e3af70cc1a7d2a3b370a6f856eba3",
    "units": "imperial"
}
~~~

 * `city_id`
	 * The city ID of the city you want temperature data for.  Openweathermap
	 	doesn't provide a searchable list for this, but 
		[here](https://openweathermap.desk.com/customer/portal/questions/11296443-city-id-s) 
		is a link for detail on how to find a city id.
 * `api_key`
	 * Your openweathermap api key (http://openweathermap.org/appid)
 * `units`
	 * The units you want temperature to be in (`imperial`, `metric`, or `kelvin`).


# Combining sensors into a single file to start your data simulation
Once you have all your sensors defined you can combine them into a single file
with the following format:

~~~ Javascript
{
    "sensor_auth": "12345abcde12345abcde12345abcde12345abcde",
    "sensors": [{
        "simulated_data": {
            "name": "Linear Data",
            "report_rate": 1,
            "type": "linear",
            "data_characteristics": {
                "slope": 1,
                "offset": 4.5
            }
        }
    }, {
        "simulated_data": {
            "name": "Sinusoidal Data",
            "report_rate": 100,
            "type": "sinusoidal",
            "data_characteristics": {
                "period": 8,
                "amplitude": 4,
                "offset": 4
            }
        }
    }, {
        "simulated_data": {
            "name": "Weather Data",
            "report_rate": 600,
            "type": "open_weather_map",
            "data_characteristics": {
                "city_id": 5037649,
                "api_key": "787e3af70cc1a7d2a3b370a6f856eba3",
                "units": "imperial"
            }
        }
    }, {
        "simulated_data": {
            "name": "Random Data",
            "report_rate": 100,
            "type": "random",
            "data_characteristics": {
                "min": 1.3,
                "max": 12
            }
        }
    }]
}
~~~

 * `sensor_auth`
	 * The Exosite CIK of the device you're simulating
 * `sensors`
	 * An array of sensors that you are simulating