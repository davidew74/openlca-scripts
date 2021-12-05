# openLCA scripts

openLCA includes Jython, an implementation of the Python programming language for Java platforms, from which a programmer can import all Java libraries, including those for openLCA. The Python application programming interface (API) for openLCA allows direct access to the openLCA software core, circumventing the graphical user interface. That means that an user can write a Python script for generating the product system and organising the results, rather than having to enter all data and structures by hand.

Under `Window > Developer tools > Python` you can find a small Python editor where you can write and execute Python scripts:

![Open Python editor](/images/olca_open_python_editor.png)

Here is a small example script that will show the information dialog below when you execute it in openLCA:

```python
from org.openlca.app.util import UI, Dialog
from org.openlca.app import App

def say_hello_world():
    Dialog.showInfo(UI.shell(), 'Hello World from Python (Jython)!')

if __name__ == '__main__':
    App.runInUI('say hello', say_hello_world)
  ```

To execute the script, click on the `Run` button in the toolbar of the Python editor:

![run a script](/images/olca_run_script.png)


Here is a minimum working example script that will show the information window:

![hello world example script execution](/images/olca_hello_world.png)

# The openLCA API
Jython allows you to directly access the openLCA Java API. you CAN interact with a Java class in the same way as with a Python class. The openLCA API starts with a set of classes that describe the basic data model, like `Flow`, `Process`, and `ProductSystem`. Such classes are in the ![olca-module repository](https://github.com/GreenDelta/olca-modules/tree/master/olca-core/src/main/java/org/openlca/core/model) by GreenDelta.