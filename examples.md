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

### How to 

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

