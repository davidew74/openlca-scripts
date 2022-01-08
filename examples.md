# Examples

## How to import openLAC modules

```python
from java.io import File
from java.util import UUID
from java.util import Date
from java.math import RoundingMode

import org.openlca.core.database.derby.DerbyDatabase as DerbyDatabase
import org.openlca.core.database.CategoryDao as CategoryDao
import org.openlca.core.database.Daos as Daos
import org.openlca.core.database.FlowDao as FlowDao
import org.openlca.core.database.FlowPropertyDao as FlowPropertyDao
import org.openlca.core.database.ImpactMethodDao as ImpactMethodDao
import org.openlca.core.database.ImpactCategoryDao as ImpactCategoryDao
import org.openlca.core.database.ProcessDao as ProcessDao
import org.openlca.core.database.ProductSystemDao as ProductSystemDao
import org.openlca.core.database.ParameterDao as ParameterDao
import org.openlca.core.database.UnitGroupDao as UnitGroupDao
import org.openlca.core.database.ImpactCategoryDao as ImpactCategoryDao
import org.openlca.core.database.DQSystemDao as DQSystemDao

import org.openlca.core.model as model
import org.openlca.core.model.FlowPropertyFactor as FlowPropertyFactor
import org.openlca.core.model.Parameter as Parameter
import org.openlca.core.model.ParameterScope as ParameterScope
import org.openlca.core.model.ParameterRedef as ParameterRedef
import org.openlca.core.model.AllocationMethod as AllocationMethod

import org.openlca.core.model.Category as Category
import org.openlca.core.model.ImpactMethod as ImpactMethod
import org.openlca.core.model.ImpactCategory as ImpactCategory
import org.openlca.core.model.ImpactFactor as ImpactFactor
import org.openlca.core.model.ModelType as ModelType
import org.openlca.core.model.ProcessType as ProcessType
import org.openlca.core.model.ProductSystem as ProductSystem
import org.openlca.core.model.descriptors.Descriptors as Descriptors

import org.openlca.core.matrix.LinkingConfig as LinkingConfig
import org.openlca.core.matrix.LinkingConfig.DefaultProviders as DefaultProviders
import org.openlca.core.matrix.ProductSystemBuilder as ProductSystemBuilder
import org.openlca.core.matrix.cache.MatrixCache as MatrixCache
import org.openlca.core.matrix.solvers.DenseSolver as DenseSolver

import org.openlca.core.math.CalculationSetup as CalculationSetup
import org.openlca.core.math.CalculationType as CalculationType
import org.openlca.core.math.SystemCalculator as SystemCalculator
import org.openlca.core.math.Simulator as Simulator

import org.openlca.core.math.data_quality.Aggregation as Aggregation
import org.openlca.core.math.data_quality.AggregationType as AggregationType
import org.openlca.core.math.data_quality.DQCalculationSetup as DQCalculationSetup
import org.openlca.core.math.data_quality.DQCalculator as DQCalculator
import org.openlca.core.math.data_quality.DQData as DQData
import org.openlca.core.math.data_quality.DQResult as DQResult
import org.openlca.core.math.data_quality.DQStatistics as DQStatistics
import org.openlca.core.math.data_quality.ProcessingType as ProcessingType

import org.openlca.core.results.SystemProcess as SystemProcess
import org.openlca.core.results.UpstreamNode as UpstreamNode
import org.openlca.core.results.SimulationResult as SimulationResult

import org.openlca.util.KeyGen as KeyGen
import org.openlca.util.Strings as Strings
import org.openlca.util.Categories as Categories

import org.openlca.app.db.Cache as Cache
import org.openlca.app.db.Database as Database
import org.openlca.app.App as App
import org.openlca.app.navigation.Navigator as Navigator

from org.openlca.app.editors import Editors
from org.openlca.app.results import ResultEditorInput
from org.openlca.app.results.analysis import AnalyzeEditor

# import standard Python libraries
import re
import csv
import imp
import datetime
# import util
util = imp.load_source('module.name', '<path to the utility file>/util.py')

# log info in the console
def log_text(text):
  log.info(text)
# refresh the Navigator
def refresh():
  Navigator.refresh()
```

### How to load Ecoinvent database and create Data Access Object (DAO) references

```python
if __name__ == '__main__':
    # load ecoinvent database list
    dataAssocArray = util.LoadJSONfile("{0}{1}".format(util.Config_CLASS.json_path, "ecoinvent35.json"))
    # get the selected ecoinvent database path
    db_dir = File("{0}{1}".format(util.Config_CLASS.db_path, dataAssocArray["ECOINVENT35_APOS_UP_REGIONALISED"]))
    # instantiate the object references
    db = DerbyDatabase(db_dir)
    # create data access object
    flow_dao = FlowDao(db)
    fp_dao = FlowPropertyDao(db)
    process_dao = ProcessDao(db)
    Param_dao = ParameterDao(db)
    category_dao = CategoryDao(db)
    impact_method_dao = ImpactMethodDao(db)
    impact_category_dao = ImpactCategoryDao(db)
    product_system_dao = ProductSystemDao(db)
    impact_category_dao = ImpactCategoryDao(db)
    DQS_dao = DQSystemDao(db)
    # create cache object
    cache = MatrixCache.createLazy(db)
```

## How to display exchanges in a process

```python
# get object instance
processObj = process_dao.getForRefId("a307239a-8570-4790-a19c-7e561adec7b8")
# get reference flow 
RefFlow = processObj.quantitativeReference
# loop thourgh the exchanges
for exch in processObj.exchanges:
  log_text("Exchange Flow name: '{0}'".format(exch.flow.name))
  log_text("Category: '{0}'".format(Strings.join(Categories.path(exch.flow.category), '/')))
  log_text("Exchange [{0}] amount: '{1}'".format(exch.flow.name, exch.amount))
  log_text("Exchange [{0}] amountFormula: '{1}'".format(exch.flow.name, exch.amountFormula))
  log_text("Exchange [{0}] Unit: '{1}'".format(exch.flow.name, exch.unit.name))
  log_text("Exchange [{0}] isInput: '{1}'".format(exch.flow.name, exch.isInput))
  log_text("Exchange [{0}] refId: '{1}'".format(exch.flow.name, exch.flow.refId))
  log_text("Exchange [{0}] unitGroup: '{1}'".format(exch.flow.name, exch.flow.referenceFlowProperty.unitGroup.name))
  log_text("Exchange [{0}] unitGroup category: '{1}'".format(exch.flow.name, Strings.join(Categories.path(exch.flow.referenceFlowProperty.unitGroup.category), '/')))
  log_text("Exchange [{0}] unit name: '{1}'".format(exch.flow.name, exch.flow.referenceFlowProperty.name))
  log_text("Exchange [{0}] default provider id: '{1}'".format(exch.flow.name, exch.defaultProviderId))
  log_text("Exchange [{0}] isQuantitativeReference: '{1}'".format(exch.flow.name, "True" if exch.flow.refId == RefFlow.flow.refId else "False"))
```

## How to delete a parameter from a process

Before deleting, we have to search a paramater via its name. We can use the function `get_parameter`:

```python
def get_parameter(process, parameter_name):
    for parameter in process.parameters:
        if parameter.name == parameter_name:
            return parameter
    return None
```
If the function returns a non empty object reference, then we can effectively delete the parameters. The task comprises three distinct step. The first is to remove parameter's object from the parameter's list of the process; the second is to delete object reference from parameter's database; and the last is to update the process

```python
param_obj = get_parameter(processObj, "Prova")
# if the function returns a valid object reference
if param_obj:
    log_text("parameter name: '{0}' found".format(param_obj.name))
    # remove parameter's object from parameter's list of the process
    processObj.parameters.remove(param_obj)
    # delete object reference from parameter's database
    Param_dao.delete(param_obj)
    # update process
    process_dao.update(processObj)
```

## How to delete an exchange from a process

```python
listExchangeFlowRefId = [_.flow.refId for _ in processObj.exchanges]
flowRefId = "f80416c8-f598-4c5d-8723-e3ca751de5ba"
if flowRefId in listExchangeFlowRefId:
log_text("There are {0} occurance of the selected flow".format(listExchangeFlowRefId.count(flowRefId)))
for exch in [_ for _ in processObj.exchanges if _.flow.refId == flowRefId]:
    Exchange_obj = util.get_exchange(process, exch.flow.refId)
    log_text("Exchange [{0}] found".format(Exchange_obj.flow.name))
    log_text("Exchange [{0}] default provider id: '{1}'".format(Exchange_obj.flow.name, Exchange_obj.defaultProviderId))
    # get default provider object reference
    defaultProviderObj = util.find_byId(db, model.processObj, Exchange_obj.defaultProviderId)
    log_text("default provider name: '{0}'".format(defaultProviderObj.name))
    # remove exchange's object from parameter's list
    processObj.exchanges.remove(Exchange_obj)
    # update process
    process_dao.update(processObj)
```


## How to delete a process

```python
processObj = process_dao.getForRefId("55053797-3f28-4930-b48e-9cd75b159e1a")
if processObj:
    process_dao.delete(processObj)
else:
    log_text("process is not in the database")
```

## How to add parameters according to a defined schema


```json
{"LIB_iron_steel_eol_waste": {"IsInputParameter": "True", "value": 38.63636364, "formula": "", "description": ""}, "LIB_iron_steel_recovery_rate": {"IsInputParameter": "True", "value": 0.95, "formula": "", "description": ""}, "LIB_iron_steel_recycling_rate": {"IsInputParameter": "True", "value": 1.0, "formula": "", "description": ""}, "LIB_iron_steel_to_closed_loop_rate_input": {"IsInputParameter": "True", "value": 0.5, "formula": "", "description": ""},...}
```

```python
processList = {"9ea8a1fe-4856-4fae-ae08-f5dbf8493fa4" : ["PARMETERS_FILE_NAME.json",...],...}


for processRefId in processList.keys():
    # get object instance
    processRefObj = util.get_process(process_dao, processRefId)
    log_text("processRefObj name = '{0}'".format(processRefObj.name))
    # loop thorugh the json files
    for jsonFile in processList[processRefId]:
      # open parameters file
      ParamAssocArray = util.openJSONfile("{0}{1}".format(util.Config_CLASS.json_path, jsonFile))
      # loop through the parameter list
      for param in ParamAssocArray.keys():
        log_text("param name = '{0}'".format(param))
        paramObj = util.get_parameter(processRefObj, param)
        if paramObj:
          log_text("update paramter's Value")
          # update paramter's Value
          paramObj.value = ParamAssocArray[param]["value"]
          paramObj.formula = ParamAssocArray[param]["formula"]
          # update database
          Param_dao.update(paramObj)
        else:
          log_text("create parameter object")
          # create paramter object
          paramObj = util.add_parameter(param, ParameterScope.PROCESS, ParamAssocArray[param])
          # inserts the parameter into the database
          Param_dao.insert(paramObj)
          # Add parameter to the process
          processRefObj.parameters.add(paramObj)
          # update database
          process_dao.update(processRefObj)

App.runInUI('Refreshing', refresh)
```

## How to save a process as a JSON file

```python
```

## How to create a process from a JSON file template

```json
    {
      "name": "PROCESS A",
      "RefId": "",
      "Category": "HIGHVLOCity Project/Hydrogen Production",
      "LocationCode": "RER",
      "LocationRefId": "d66c264e-1dbd-33e6-911d-3ffc70908e8e",
      "Exchange_DICT": [
        {
          "amount": 1,
          "isInput": "False",
          "amountFormula": "functional_unit_amount",
          "defaultProvider": {
            "defaultProviderLocationRefId": "",
            "defaultProviderLocationCode": "",
            "defaultProviderName": "",
            "defaultProviderRefId": ""
          },
          "FlowProperty": "Mass",
          "flow": {
            "description": "",
            "flowtype": "FlowType_PRODUCT_FLOW",
            "name": "FLOW A",
            "referenceFlowProperty": "Mass",
            "refId": "",
            "category": ""
          },
          "isQuantitativeReference": "True"
        }
      ],
      "Reference_Flow_DICT": {
        "name": "FLOW A",
        "ReferenceFlowProperty": "Mass",
        "refId": ""
      },
      "Input_Parameter_DICT": {
        "functional_unit_input": {
          "IsInputParameter": "True",
          "description": "",
          "name": "functional_unit_input",
          "formula": "",
          "value": 1
        },
        "functional_unit_amount": {
          "IsInputParameter": "False",
          "description": "",
          "name": "functional_unit_amount",
          "formula": "functional_unit_input",
          "value": 1
        }
      }
    }

```


```python
def create_process_from_template2(process_DICT):
  db = Database.get()
  process_dao = ProcessDao(db)
  Param_dao = ParameterDao(db)
  location_dao = LocationDao(db)
  flow_dao = FlowDao(db)
  fp_dao = FlowPropertyDao(db)

  # mass = util.find(db, model.FlowProperty, 'Mass')
  mass = fp_dao.getForName('Mass')[0]
  #items = util.find(db, model.FlowProperty, 'Mass')
  items = fp_dao.getForName('Number of items')[0]
  #energy = util.find(db, model.FlowProperty, 'Energy')
  energy = fp_dao.getForName('Energy')[0]
  #volume = util.find(db, model.FlowProperty, 'Volume')
  volume = fp_dao.getForName('Volume')[0]
  #good_transport = util.find(db, model.FlowProperty, 'Goods transport (mass*distance)')
  good_transport = fp_dao.getForName('Goods transport (mass*distance)')[0]
  #area = util.find(db, model.FlowProperty, 'Area')
  area = fp_dao.getForName('Area')[0]
  #length = util.find(db, model.FlowProperty, 'Length')
  length = fp_dao.getForName('Length')[0]
  #volume = util.find(db, model.FlowProperty, 'Volume')
  volume = fp_dao.getForName('Volume')[0]

  FlowProperty_DICT = {"Mass" : mass, "Items" : items, "Energy" : energy, "Volume" : volume, "Good Transport": good_transport, "Area" : area, "Length" : length, "Volume" : volume}

  proc_name = process_DICT[Process_CLASS.Name_KEY]
  log_text("Process: '{0}'".format(proc_name))
  # *************************************************************
  # Add Process
  # *************************************************************
  # First of all checks if the process name is in the database
  if not process_DICT[Process_CLASS.RefId_KEY]:
    process_ref = model.Process()
    # Sets the process name
    process_ref.name = proc_name
    # *************************************************************
    # Gets category ref
    # *************************************************************
    # Builds the category list
    process_category_path = process_DICT[Process_CLASS.Category_Process_KEY].split("/")
    parent_process_category = get_category(ModelType.PROCESS, process_category_path)
    # check if the category path exist, otherwise it creates it for PROCESS and FLOW
    if parent_process_category is None:
      add_category_list(ModelType_CLASS.ModelType_DICT[ModelType_CLASS.ModelType_PROCESS], ModelType_CLASS.ModelType_ROOT_ELEMENT_DICT[ModelType_CLASS.ModelType_PROCESS], [process_category_path])
      add_category_list(ModelType_CLASS.ModelType_DICT[ModelType_CLASS.ModelType_FLOW], ModelType_CLASS.ModelType_ROOT_ELEMENT_DICT[ModelType_CLASS.ModelType_FLOW], [process_category_path])
      parent_process_category = get_category(ModelType.PROCESS, process_category_path)
    # Sets the parent category
    process_ref.category = parent_process_category
    # Sets the universally unique identifier (UUID) to the process
    process_ref.refId = UUID.randomUUID().toString()
    # get location RefId
    locationObj = location_dao.getForRefId(process_DICT[Process_CLASS.LocationRefId_KEY])
    process_ref.location = locationObj
    # update process refId
    process_DICT[Process_CLASS.RefId_KEY] = process_ref.refId
    # Inserts the process into the database
    insert(db, process_ref)
    # *************************************************************
    # Add paramenters
    # *************************************************************
    log_text("Add paramenters")
    Input_Parameter_DICT = process_DICT[Process_CLASS.Parameter_DICT_KEY]
    # loops through the parameters dictionary
    for paramItem in Input_Parameter_DICT.keys():
      log_text("Parameter Name: '{0}'".format(paramItem))
      # Gets the paraments reference
      param = add_parameter(paramItem, ParameterScope.PROCESS, Input_Parameter_DICT[paramItem])
      # Inserts the parameter into the database
      Param_dao.insert(param)
      # Add parameter to the process
      process_ref.parameters.add(param)
    # *************************************************************
    # Add Reference flow
    # *************************************************************
    # gets the parent category
    # The refernce flow category must be the same as the process one
    parent_flow_category = get_category(ModelType.FLOW, process_category_path)
    #**************************************************************
    log_text("checks if the object reference is valid")
    # checks if the object reference is valid
    log_text("add Reference flow")
    # creates the reference flow from using the data stored in the "Reference_Flow_DICT"
    if process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.RefId]:
      log_text("get Reference flow from existing RefId")
      proc_output_flow = flow_dao.getForRefId(process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.RefId])
    else:
      log_text("Create a new Reference flow")
      tmpFlow_DICT = {}
      tmpFlow_DICT[Flow_dict_CLASS.Name_KEY] = process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.name]
      tmpFlow_DICT[Flow_dict_CLASS.FlowProperty_KEY] = FlowProperty_DICT[process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.referenceFlowProperty]]
      tmpFlow_DICT[Flow_dict_CLASS.category_KEY] = parent_flow_category
      # A Reference Flow must be PRODUCT FLOW type
      tmpFlow_DICT[Flow_dict_CLASS.FlowType_KEY] = FlowType_CLASS.FlowType_DICT[FlowType_CLASS.FlowType_PRODUCT_FLOW]
      proc_output_flow = add_flow(db, tmpFlow_DICT)
    #**************************************************************
    log_text("Reference flow RefId: '{0}'".format(proc_output_flow.refId))
    # *************************************************************
    # Update reference Flow RefId
    # *************************************************************
    log_text("Update reference Flow RefId in 'Reference_Flow_DICT'")
    process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.RefId] = proc_output_flow.refId
    # look for quantitativeReference flow.
    Flow_DICT = process_DICT[Process_CLASS.Exchange_DICT_KEY]
    indexes = [i for i, _ in enumerate(Flow_DICT) if toBool(_[Process_CLASS.Flow_CLASS.isQuantitativeReference])]
    if len(indexes) > 0:
      log_text("Update reference Flow RefId in 'Flow_DICT'")
      # Get the reference flow name
      QuantitativeReferenceIndex = indexes[0]
      # Update reference Flow RefId
      Flow_DICT[QuantitativeReferenceIndex][Process_CLASS.Exchange_CLASS.flow][Process_CLASS.Reference_Flow_CLASS.RefId] = proc_output_flow.refId
    else:
      log_text("There are no reference Flow in 'Flow_DICT'")
    #process_DICT[Process_CLASS.Flow_DICT_KEY][][Process_CLASS.Reference_Flow_CLASS.RefId] = proc_output_flow.refId
    # *************************************************************
    # Create exchange Reference flow
    # *************************************************************
    log_text("add Exchange Reference flow")
    # Gets the exchange reference from the reference flow previously created
    proc_exchange = add_exchange(proc_output_flow, Flow_DICT[QuantitativeReferenceIndex])
    # Add reference flow to the process exchange
    process_ref.exchanges.add(proc_exchange)
    # Set the procress quantitativeReference
    process_ref.quantitativeReference = proc_exchange
    # *************************************************************
    # Adds input and emissions exchanges
    # *************************************************************
    log_text("add Exchange flows")
    # Gets the "FLOW_DICT" dictionary
    Flow_DICT = process_DICT[Process_CLASS.Exchange_DICT_KEY]
    # Loops through the Flow_DICT
    # Selects flows with a not empty dafaultProviderRefId string
    # Selected_keys = [_ for _ in Flow_DICT if _[Process_CLASS.Exchange_CLASS.defaultProvider][Process_CLASS.DefaultProvider_CLASS.defaultProviderRefId]]
    indexes = [i for i, _ in enumerate(Flow_DICT) if not toBool(_[Process_CLASS.Exchange_CLASS.isQuantitativeReference])]
    log_text("there are {0} flows...".format(len(indexes)) if len(indexes) > 0 else "no flows available...")

    for exchangeIndex in indexes:
      log_text("Exchange flow: '{0}'".format(Flow_DICT[exchangeIndex][Process_CLASS.Exchange_CLASS.flow][Process_CLASS.Flow_CLASS.name]))
      # check is there is a valid refId
      if Flow_DICT[exchangeIndex][Process_CLASS.Exchange_CLASS.flow][Process_CLASS.Flow_CLASS.refId]:
        # Gets the the flow reference
        flow_ref = find_byRefId(db, model.Flow, Flow_DICT[exchangeIndex][Process_CLASS.Exchange_CLASS.flow][Process_CLASS.Flow_CLASS.refId])
        # Adds the exchange flow with the associated flow dictiorary with attributes
        proc_exchange = add_exchange(flow_ref, Flow_DICT[exchangeIndex])
        # check is there is a valid defaultProviderRefId
        if Flow_DICT[exchangeIndex][Process_CLASS.Exchange_CLASS.defaultProvider][Process_CLASS.DefaultProvider_CLASS.defaultProviderRefId]:
          # get dafault provider reference
          defaultProviderRef = process_dao.getForRefId(Flow_DICT[exchangeIndex][Process_CLASS.Exchange_CLASS.defaultProvider][Process_CLASS.DefaultProvider_CLASS.defaultProviderRefId])
          log_text("defaultProviderId: {0}".format(str(defaultProviderRef.id)))
          # Sets the default provider Id to the selected exchange
          proc_exchange.defaultProviderId = defaultProviderRef.id
        # Adds exchange flow to the process
        process_ref.exchanges.add(proc_exchange)
    # *************************************************************
    # update database
    # *************************************************************
    process_dao.update(process_ref)
  else:
    log_text("Process: '{0}' already exists. RefId = '{1}'".format(proc_name, process_DICT[Process_CLASS.RefId_KEY]))
    process_ref = process_dao.getForRefId(process_DICT[Process_CLASS.RefId_KEY])
  return process_ref
```