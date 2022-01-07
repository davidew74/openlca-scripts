# The openLCA data model
The basic data model of openLCA is defined in the package `org.openlca.core.model` of the [olca-core module](https://github.com/GreenDelta/olca-modules). This repository is the starting point whewnever you have to deal with data in openLCA. In this section, we introduce the basic data types and their hierarchical classification. Each type is basically a Java class which represents the set of properties or methods that are common to all objects of one type. You can easily access individual Java class just like a normal Python class from Jython.

Here is how you would typically _import_, then _invoke_ a method within a Python program:

```python
# import the model package...
import org.openlca.core.model as model

#...then create a class instance of Process type...
process_ref = model.Process()

 #...and then set the process name, invoking the method name as required.
process_ref.name = "PROCESS_NAME_STRING"
```

A collection of related functions makes up a module. In openLCA, we can identify five core modules: `database`, `math`, `matrix`, `model`,  and `result`:

<img src="https://github.com/davidew74/openlca-scripts/blob/main/images/python_model_structure.png" width="750">


# The basic inventory model
The openLCA data model is built around a basic inventory model which has the following components:

<img src="https://github.com/davidew74/openlca-scripts/blob/main/images/openlca_object_model.png">

In this simplified model, `processes` are the basic building blocks that describe the production of a material or energy, treatment of waste, provision of a service, etc. Each process has a set of `exchanges` that contain the inputs and outputs of flows like products, wastes, resources, and related emissions. The `product flows` (since openLCA 1.7 also waste flows) can be linked in a product system to specify the `provider` of a product or service - the functional unit of that product system. Such product systems are then used to calculate inventory and impact assessment results.