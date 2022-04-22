# Motion Planning Application

This project is created from a python template for testing out some Motion Planning Algorithms. The template was created
with Python `3.7.8`.

The template was extended and updated with improvements to the template and the algorithms itself. The development was
done with Python `3.10.3` and the [dependencies](requirements.txt) were updated to this state.

### Description

This project was created within a lecture of __Datastructures and Algorithms__. It implements several functions like
__Collision Detection__ and __Motion Planning__ with calculations in the several spaces.

## Installation

You should create a virtual environment (`venv`) and install the required packages with the following commands:

Windows:

```shell
python -m venv env
.\env\Scripts\activate    
(env) $ pip install -r requirements.txt
```

Linux:

```shell
python3 -m venv env
source env/bin/activate
(env) $ pip install -r requirements.txt
```

## Run

In order to run it make sure that your `venv` is installed.

Windows:

```shell
.\env\Scripts\activate 
(env) $ python app.py
```

Linux:

```shell
source env/bin/activate
(env) $ python app.py
```

## Architecture

```
              app.py
                |
    ------- controller ----------   
    |           |               |
workspace   configspace   collisionspace
```

<details>
  <summary>Explanation</summary>

* [app.py](app.py) = start the application and the UI
* [controller.py](controller.py) = manages all the spaces below
* [workspace.py](workspace.py) = handles graphical display of algorithms and collision-detection
* [configspace.py](configspace.py) = handles the motion-planning algorithms
* [collisionspace.py](collisionspace.py) = calculates and shows collision-space

</details>