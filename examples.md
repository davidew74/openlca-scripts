# Examples

## How to display exchanges in a process


```python
# get object instance
process = util.get_process(process_dao, "a307239a-8570-4790-a19c-7e561adec7b8")
# get reference flow 
RefFlow = process.quantitativeReference
# loop thourgh the exchanges
for exch in process.exchanges:
  log_text("Exchange Flow name: '{0}'".format(exch.flow.name))
  log_text("Category: '{0}'".format(exch.flow.category.name))
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