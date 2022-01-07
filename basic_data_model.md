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