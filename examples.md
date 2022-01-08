# Examples

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

