import org.openlca.core.database.Daos as Daos
import org.openlca.core.model as model
import org.openlca.core.model.ModelType as ModelType
import org.openlca.core.model.Parameter as Parameter
import org.openlca.core.model.Category as Category
import org.openlca.core.model.ParameterScope as ParameterScope
import org.openlca.core.model.ParameterRedef as ParameterRedef
import org.openlca.core.model.ImpactMethod as ImpactMethod
import org.openlca.core.model.ImpactCategory as ImpactCategory
import org.openlca.core.model.ImpactFactor as ImpactFactor
import org.openlca.expressions.FormulaInterpreter as FormulaInterpreter
import org.openlca.core.model.ProductSystem as ProductSystem
import org.openlca.core.model.AllocationMethod as AllocationMethod
import org.openlca.core.model.ProcessType as ProcessType
import org.openlca.core.model.descriptors.Descriptors as Descriptors

import org.openlca.app.db.Database as Database

import org.openlca.core.database.LocationDao as LocationDao
import org.openlca.core.database.ProcessDao as ProcessDao
import org.openlca.core.database.ParameterDao as ParameterDao
import org.openlca.core.database.CategoryDao as CategoryDao
import org.openlca.core.database.FlowDao as FlowDao
import org.openlca.core.database.FlowPropertyDao as FlowPropertyDao
import org.openlca.core.database.FlowPropertyDao as FlowPropertyDao
import org.openlca.core.database.ImpactMethodDao as ImpactMethodDao
import org.openlca.core.database.ImpactCategoryDao as ImpactCategoryDao
import org.openlca.core.database.ProductSystemDao as ProductSystemDao

import org.openlca.core.matrix.LinkingConfig as LinkingConfig
import org.openlca.core.matrix.LinkingConfig.DefaultProviders as DefaultProviders
import org.openlca.core.matrix.ProductSystemBuilder as ProductSystemBuilder
import org.openlca.core.matrix.cache.MatrixCache as MatrixCache
import org.openlca.core.matrix.solvers.DenseSolver as DenseSolver

import org.openlca.core.math.data_quality.Aggregation as Aggregation
import org.openlca.core.math.data_quality.AggregationType as AggregationType
import org.openlca.core.math.data_quality.DQCalculationSetup as DQCalculationSetup
import org.openlca.core.math.data_quality.DQCalculator as DQCalculator
import org.openlca.core.math.data_quality.DQData as DQData
import org.openlca.core.math.data_quality.DQResult as DQResult
import org.openlca.core.math.data_quality.DQStatistics as DQStatistics
import org.openlca.core.math.data_quality.ProcessingType as ProcessingType

import org.openlca.core.math.CalculationSetup as CalculationSetup
import org.openlca.core.math.CalculationType as CalculationType
import org.openlca.core.math.SystemCalculator as SystemCalculator

import org.openlca.util.KeyGen as KeyGen
import org.openlca.util.Strings as Strings
import org.openlca.util.Categories as Categories

import org.openlca.core.results.SystemProcess as SystemProcess
import org.openlca.core.results.UpstreamNode as UpstreamNode

# https://github.com/GreenDelta/olca-app/tree/master/olca-app/src/org/openlca/app/db
import org.openlca.app.db.Cache as Cache
import org.openlca.app.db.Database as Database
import org.openlca.app.App as App
import org.openlca.app.navigation.Navigator as Navigator

from java.util import UUID, Date
from java.math import RoundingMode

import org.apache.log4j.Level as Level
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

import csv
import sys
import json
import io
import re

class ModelType_CLASS(object):

  ModelType_UNKNOWN = "ModelType_UNKNOWN"
  ModelType_PROJECT = "ModelType_PROJECT"
  ModelType_IMPACT_METHOD = "ModelType_IMPACT_METHOD"
  ModelType_IMPACT_CATEGORY = "ModelType_IMPACT_CATEGORY"
  ModelType_PRODUCT_SYSTEM = "ModelType_PRODUCT_SYSTEM"
  ModelType_PROCESS = "ModelType_PROCESS"
  ModelType_FLOW = "ModelType_FLOW"
  ModelType_FLOW_PROPERTY = "ModelType_FLOW_PROPERTY"
  ModelType_UNIT_GROUP = "ModelType_UNIT_GROUP"
  ModelType_UNIT = "ModelType_UNIT"
  ModelType_ACTOR = "ModelType_ACTOR"
  ModelType_SOURCE = "ModelType_SOURCE"
  ModelType_CATEGORY = "ModelType_CATEGORY"
  ModelType_LOCATION = "ModelType_LOCATION"
  ModelType_NW_SET = "ModelType_NW_SET"
  ModelType_SOCIAL_INDICATOR = "ModelType_SOCIAL_INDICATOR"
  ModelType_CURRENCY = "ModelType_CURRENCY"
  ModelType_PARAMETER = "ModelType_PARAMETER"
  ModelType_DQ_SYSTEM = "ModelType_DQ_SYSTEM"
  ModelType_GLOBAL_PARAMETER = "ModelType_GLOBAL_PARAMETER"

  ModelType_DICT = {ModelType_UNKNOWN : ModelType.UNKNOWN,
  ModelType_PROJECT : ModelType.PROJECT,
  ModelType_IMPACT_METHOD : ModelType.IMPACT_METHOD,
  ModelType_IMPACT_CATEGORY : ModelType.IMPACT_CATEGORY,
  ModelType_PRODUCT_SYSTEM : ModelType.PRODUCT_SYSTEM,
  ModelType_PROCESS : ModelType.PROCESS,
  ModelType_FLOW : ModelType.FLOW,
  ModelType_FLOW_PROPERTY : ModelType.FLOW_PROPERTY,
  ModelType_UNIT_GROUP : ModelType.UNIT_GROUP,
  ModelType_UNIT : ModelType.UNIT,
  ModelType_ACTOR : ModelType.ACTOR,
  ModelType_SOURCE : ModelType.SOURCE,
  ModelType_CATEGORY : ModelType.CATEGORY,
  ModelType_LOCATION : ModelType.LOCATION,
  ModelType_NW_SET : ModelType.NW_SET,
  ModelType_SOCIAL_INDICATOR : ModelType.SOCIAL_INDICATOR,
  ModelType_CURRENCY : ModelType.CURRENCY,
  ModelType_PARAMETER : ModelType.PARAMETER,
  ModelType_DQ_SYSTEM : ModelType.DQ_SYSTEM}

  ModelType_ROOT_ELEMENT_DICT = {
  ModelType_PROJECT : ['Projects'],
  ModelType_IMPACT_METHOD : ['Impact assessment methods'],
  ModelType_PRODUCT_SYSTEM : ['Product Systems'],
  ModelType_PROCESS : ['Processes'],
  ModelType_FLOW : ['Flows'],
  ModelType_UNIT_GROUP : ['Unit groups'],
  ModelType_ACTOR : ['Actors'],
  ModelType_SOURCE : ['Sources'],
  ModelType_LOCATION : ['Locations'],
  ModelType_GLOBAL_PARAMETER : ['Global parameters']}

class FlowType_CLASS(object):
  FlowType_ELEMENTARY_FLOW = "FlowType_ELEMENTARY_FLOW"
  FlowType_PRODUCT_FLOW = "FlowType_PRODUCT_FLOW"
  FlowType_WASTE_FLOW = "FlowType_WASTE_FLOW"

  FlowType_DICT = {
  FlowType_ELEMENTARY_FLOW : model.FlowType.ELEMENTARY_FLOW,
  FlowType_PRODUCT_FLOW : model.FlowType.PRODUCT_FLOW,
  FlowType_WASTE_FLOW : model.FlowType.WASTE_FLOW}

  def getFlowTypeName(self, flowTypeObj):
    return  {v: k for k, v in self.FlowType_DICT.items()}[flowTypeObj]


class Flow_dict_CLASS(object):
  Name_KEY = "name"
  FlowProperty_KEY = "FlowProperty"
  category_KEY = "category"
  FlowType_KEY = "FlowType"

class Config_CLASS(object):
  base_path = 'C:/Users/Davide Pederzoli/Documents/Python Scripts/'
  json_path = 'F:/SANDISK_32/DOTTORATO UNIGE/PUBBLICAZIONE ARTICOLO/OpenLCA/'
  db_path = 'C:/Users/Davide Pederzoli/openLCA-data-1.4/databases/'
  category_list_file = 'CATEGORY_LIST.txt'
  process_list_file = 'process_list_dict.txt'
  global_warming_regexp_pattern = '^(Global|Climate|GWP|CO2)[\(\)0-9a-zA-Z\s-]+$'
  impact_method_file = "Impact_methods_DICT.json"

class Process_CLASS(object):
  Parameter_DICT_KEY = "Input_Parameter_DICT"
  Flow_DICT_KEY = "Flow_DICT"
  Exchange_DICT_KEY = "Exchange_DICT"
  Reference_Flow_DICT_KEY = "Reference_Flow_DICT"
  Category_Process_KEY = "Category"
  RefId_KEY = "RefId"
  Name_KEY = "name"
  LocationCode_KEY = "LocationCode"
  LocationRefId_KEY = "LocationRefId"

  class Parameter_CLASS(object):
    IsInputParameter = "IsInputParameter"
    value = "value"
    description = "description"
    formula = "formula"
    name = "name"

  class Flow_CLASS(object):
    name = "name"
    isInput = "isInput"
    FlowProperty = "FlowProperty"
    amount = "amount"
    amountFormula = "amountFormula"
    isQuantitativeReference = "isQuantitativeReference"
    refId = "refId"
    defaultProviderRefId = "defaultProviderRefId"
    defaultProviderName = "defaultProviderName"
    defaultProviderLocationRefId = "defaultProviderLocationRefId"
    defaultProviderLocationCode = "defaultProviderLocationCode"
    category = "category"

  class Exchange_CLASS(object):
    #name = "name"
    flow = "flow"
    isInput = "isInput"
    FlowProperty = "FlowProperty"
    amount = "amount"
    amountFormula = "amountFormula"
    isQuantitativeReference = "isQuantitativeReference"
    #refId = "refId"
    defaultProvider = "defaultProvider"

  class DefaultProvider_CLASS(object):
    defaultProviderRefId = "defaultProviderRefId"
    defaultProviderName = "defaultProviderName"
    defaultProviderLocationRefId = "defaultProviderLocationRefId"
    defaultProviderLocationCode = "defaultProviderLocationCode"

  class Reference_Flow_CLASS(object):
    referenceFlowProperty = "ReferenceFlowProperty"
    amount = "amount"
    amountFormula = "amountFormula"
    isInput = "isInput"
    name = "name"
    RefId = "refId"
    category = "category"

class ParameterRedef_CLASS(object):
    contextId = "contextId"
    contextType = "contextType"

class Flow_TEMPLATE_CLASS(object):
  def __init__(self, name, flowtype, referenceFlowProperty, refId, description = "", category = ""):
    self.name = name
    self.flowtype = flowtype #FlowType_CLASS.FlowType_DICT[flowtype]
    self.referenceFlowProperty = referenceFlowProperty
    self.refId = refId
    self.description = description
    self.category = category

class ReferenceFlow_TEMPLATE_CLASS(object):
  def __init__(self, name, isInput, referenceFlowProperty, amount, amountFormula, refId):
    self.name = name
    self.isInput = isInput
    self.referenceFlowProperty = referenceFlowProperty
    self.amount = amount
    self.amountFormula = amountFormula
    self.refId = refId
    #self.description = description

class Parameter_TEMPLATE_CLASS(object):
  def __init__(self, name, isInputParameter, value, formula, description):
    self.name = name
    self.isInputParameter = isInputParameter
    self.value = value
    self.formula = formula
    self.description = description

class Exchange_TEMPLATE_CLASS(object):
  def __init__(self, flowObj, isInput, amount, amountFormula, referenceFlowProperty,
  isQuantitativeReference,
  defaultProviderObj):
    self.flow = flowObj
    self.isInput = isInput
    self.amount = amount
    self.amountFormula = amountFormula
    self.referenceFlowProperty = referenceFlowProperty
    self.isQuantitativeReference = isQuantitativeReference
    self.defaultProviderObj = defaultProviderObj

class DefaultProvider_TEMPLATE_CLASS(object):
  def __init__(self,
  defaultProviderName,
  defaultProviderRefId,
  defaultProviderLocationCode,
  defaultProviderLocationRefId):
    self.defaultProviderName = defaultProviderName
    self.defaultProviderRefId = defaultProviderRefId
    self.defaultProviderLocationCode = defaultProviderLocationCode
    self.defaultProviderLocationRefId = defaultProviderLocationRefId

def Obj2dict(clsRef):
  # helper functions
  get_class_all_item = lambda x : [a for a in dir(x) if not a.startswith('__')]
  get_class_obj = lambda x: [a for a in dir(x) if not a.startswith('__') and callable(getattr(x, a))]
  get_class_attr = lambda x: list(set(get_class_all_item(x)) - set(get_class_obj(x)))
  # loop root class attributes
  return {attr: clsRef.__dict__[attr] for attr in get_class_attr(clsRef)}

def get_exchangeObj(ExchangeB):
  ExchangeB_obj = add_exchange(ExchangeB.flow, Obj2dict(ExchangeB))
  ExchangeB_obj.defaultProviderId = ExchangeB.defaultProviderObj.id if ExchangeB.defaultProviderObj is not None else 0
  return ExchangeB_obj

def set_parameter_attributes(IsInputParameter, value, formula, description = ""):
  param_attribute_DICT = {}
  param_attribute_DICT[Process_CLASS.Parameter_CLASS.IsInputParameter] = IsInputParameter
  param_attribute_DICT[Process_CLASS.Parameter_CLASS.value] = value
  param_attribute_DICT[Process_CLASS.Parameter_CLASS.formula] = formula
  param_attribute_DICT[Process_CLASS.Parameter_CLASS.description] = description
  return param_attribute_DICT

def testlog():
  log_text("update parameters")

def log_text(msg):
  log = LoggerFactory.getLogger('org.openlca.davide')
  log.info(msg)

def count_iterable(iterable):
  """
  # https://stackoverflow.com/questions/3345785/getting-number-of-elements-in-an-iterator-in-python
  # Edit: Using list() will read the whole iterable into memory at once, which may be undesirable.
  # That will avoid keeping it in memory.
  #
  # GOOGLE: underscore variable python
  # https://hackernoon.com/understanding-the-underscore-of-python-309d1a029edc
  # The underscore (_) is special in Python
  # Single Leading Underscore: _var
  # Single Trailing Underscore: var_
  # Double Leading Underscore: __var
  # Double Leading and Trailing Underscore: __var__
  # Single Underscore: _
  # a single standalone underscore is sometimes used as a name to indicate that a variable is temporary or insignificant.
  """
  return sum(1 for _ in iterable)

def get_class_iterable(db, clazz):
  return Daos.base(db, clazz).getAll()

def count_class_iterable(db, clazz):
  return count_iterable(get_class_iterable(db, clazz))

def get_nth_iterable(iterable, index):
  # https://stackoverflow.com/questions/2300756/get-the-nth-item-of-a-generator-in-python
  return next((x for i,x in enumerate(iterable) if i == index), None)

def toBool(val):
  """
  converts string boolean value into a boolean value
  """
  if isinstance(val, bool):
    return val
  else:
    # https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python/18472142
    # The JSON parser is also useful for in general converting strings to reasonable python types.
    return val if isinstance(val.lower(), bool) else json.loads(val.lower())

def add_parameter_redef(pname, pvalue, redef_attribute_DICT):
  pmRedef = ParameterRedef()
  pmRedef.name = pname
  pmRedef.value = pvalue
  pmRedef.contextId = redef_attribute_DICT[ParameterRedef_CLASS.contextId] #process.id or None
  pmRedef.contextType = redef_attribute_DICT[ParameterRedef_CLASS.contextType] #ModelType.PROCESS or None
  return pmRedef

def getInputGlobalParameterList(db):
  pmList = get_class_iterable(db, model.Parameter)
  return [_ for _ in pmList if _.scope is ParameterScope.GLOBAL] #and _.isInputParameter is True

def evalute_parameter_formula(strFormula):
  interpreter = FormulaInterpreter()
  # lopp through all GLOBAL paramters
  for pmObj in getInputGlobalParameterList(Database.get()):
    # bind the values to the parameters name
    interpreter.bind(pmObj.name, str(pmObj.value))
  # evaluate paramter formula
  pvale = interpreter.eval(strFormula)
  return pvale

def add_parameter(pname, scope, param_attribute_DICT):
  param = Parameter()
  param.scope = scope
  param.name = pname
  param.refId = UUID.randomUUID().toString()
  param.isInputParameter = toBool(param_attribute_DICT[Process_CLASS.Parameter_CLASS.IsInputParameter])
  param.description = param_attribute_DICT[Process_CLASS.Parameter_CLASS.description]
  param.formula = param_attribute_DICT[Process_CLASS.Parameter_CLASS.formula]
  #
  if param.isInputParameter is False:
    if param.scope is ParameterScope.GLOBAL:
      # valid for GLOBAL paramters
      # assing the calculated value to the parameter
      param.value = evalute_parameter_formula(param.formula)
      # end GLOBAL parameter
    else:
      param.value = param_attribute_DICT[Process_CLASS.Parameter_CLASS.value]
  else:
    param.value = param_attribute_DICT[Process_CLASS.Parameter_CLASS.value]
  return param

def update_process_parameters(processObj):
  log_text("START Process DEPENDENT parameters")
  get_all_parameters = lambda x : x.parameters
  get_all_input_parameters = lambda x : [_ for _ in get_all_parameters(x) if _.isInputParameter is True]
  get_all_dependent_parameters = lambda x : list(set(get_all_parameters(x)) - set(get_all_input_parameters(x)))
  # get FormulaInterpreter object reference
  interpreter = FormulaInterpreter()
  # loop through all GLOBAL paramters
  log_text("get all GLOBAL parameters")
  for pmObj in getInputGlobalParameterList(Database.get()):
    # bind the values to the parameters name
    interpreter.bind(pmObj.name, str(pmObj.value))
  # loop through all INPUT paramters
  log_text("get all INPUT parameters")
  for pmObj in get_all_input_parameters(processObj):
    interpreter.bind(pmObj.name, str(pmObj.value))
  # loop through all DEPENDENT paramters
  log_text("Update all Process DEPENDENT parameters")
  for pmObj in get_all_dependent_parameters(processObj):
    pmObj.value = interpreter.eval(pmObj.formula)

def update_process_parameters_test(processObj):
  log_text("START Process DEPENDENT parameters")
  get_all_parameters = lambda x : x.parameters
  get_all_input_parameters = lambda x : [_ for _ in get_all_parameters(x) if _.isInputParameter is True]
  get_all_dependent_parameters = lambda x : list(set(get_all_parameters(x)) - set(get_all_input_parameters(x)))
  # get FormulaInterpreter object reference
  interpreter = FormulaInterpreter()
  # loop through all GLOBAL paramters
  log_text("get all GLOBAL parameters")
  for pmObj in getInputGlobalParameterList(Database.get()):
    # bind the values to the parameters name
    interpreter.bind(pmObj.name, str(pmObj.value))
  # loop through all INPUT paramters
  log_text("get all INPUT parameters")
  for pmObj in get_all_input_parameters(processObj):
    interpreter.bind(pmObj.name, str(pmObj.value))
  # loop through all INPUT paramters
  log_text("get all DEPENDENT parameters")
  for pmObj in get_all_dependent_parameters(processObj):
    interpreter.bind(pmObj.name, str(pmObj.formula))
  # loop through all DEPENDENT paramters
  log_text("Update all Process DEPENDENT parameters")
  for pmObj in get_all_dependent_parameters(processObj):
    #pmObj.value = interpreter.eval(pmObj.formula)
    log_text("Dependent param [{0}] amount: '{1}'".format(pmObj.name, interpreter.eval(pmObj.formula)))

def get_parameters_list(processObj, verbose = False):
  # initialize paramter dictionary
  param_DICT = {}
  if verbose:
    log_text("START Process DEPENDENT parameters")
  get_all_parameters = lambda x : x.parameters
  get_all_input_parameters = lambda x : [_ for _ in get_all_parameters(x) if _.isInputParameter is True]
  get_all_dependent_parameters = lambda x : list(set(get_all_parameters(x)) - set(get_all_input_parameters(x)))
  # get FormulaInterpreter object reference
  interpreter = FormulaInterpreter()
  # loop through all GLOBAL paramters
  if verbose:
    log_text("get all GLOBAL parameters")
  for pmObj in getInputGlobalParameterList(Database.get()):
    # bind the values to the parameters name
    interpreter.bind(pmObj.name, str(pmObj.value))
  # loop through all INPUT paramters
  if verbose:
    log_text("get all INPUT parameters")
  for pmObj in get_all_input_parameters(processObj):
    interpreter.bind(pmObj.name, str(pmObj.value))
    # set value to paramter dictionary
    param_DICT[pmObj.name] = pmObj.value
  # loop through all INPUT paramters
  if verbose:
    log_text("get all DEPENDENT parameters")
  for pmObj in get_all_dependent_parameters(processObj):
    interpreter.bind(pmObj.name, str(pmObj.formula))
  # loop through all DEPENDENT paramters
  if verbose:
    log_text("Update all Process DEPENDENT parameters")
  for pmObj in get_all_dependent_parameters(processObj):
    # set value to paramter dictionary
    param_DICT[pmObj.name] = interpreter.eval(pmObj.formula)
    #pmObj.value = interpreter.eval(pmObj.formula)
    if verbose:
      log_text("Dependent param [{0}] amount: '{1}'".format(pmObj.name, param_DICT[pmObj.name]))
  return param_DICT

def add_exchange(flow_ref, flow_attribute_DICT):
  proc_exchange = model.Exchange()
  proc_exchange.isInput = toBool(flow_attribute_DICT[Process_CLASS.Flow_CLASS.isInput])
  proc_exchange.flow = flow_ref
  proc_exchange.unit = flow_ref.referenceFlowProperty.unitGroup.referenceUnit
  proc_exchange.amount = flow_attribute_DICT[Process_CLASS.Flow_CLASS.amount]
  proc_exchange.amountFormula = flow_attribute_DICT[Process_CLASS.Flow_CLASS.amountFormula]
  proc_exchange.flowPropertyFactor = flow_ref.getReferenceFactor()
  return proc_exchange

def insert(db, value):
    Daos.base(db, value.getClass()).insert(value)

def update(db, value):
    return Daos.base(db, value.getClass()).update(value)

def delete_all(db, clazz):
    dao = Daos.base(db, clazz)
    dao.deleteAll()

def find(db, clazz, name):
    """ Find something by name"""
    dao = Daos.base(db, clazz)
    for item in dao.getAll():
        if item.name == name:
            return item
    return None

def find_byRefId(db, clazz, RefId):
    """ Find something by RefId"""
    dao = Daos.base(db, clazz)
    for item in dao.getAll():
        if item.refId == RefId:
            return item
    return None

def find_byId(db, clazz, id):
    """ Find something by id"""
    dao = Daos.base(db, clazz)
    return dao.getForId(id)

def printList2csv(out_file_name, iterableList):
    f = open(out_file_name, 'wb')
    writer = csv.writer(f)#, lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='', delimiter='\t')
    for item in iterableList:
        # https://stackoverflow.com/questions/4048964/printing-tab-separated-values-of-a-list/4048974
        lst = []
        for elem in item:
          lst.append(str(elem).encode('utf-8').replace('.',','))
        writer.writerow(['\t'.join(lst)])
    #sys.stdout.write("prova")
    f.close()

def print2csv(db, clazz, out_file_name, tmplog):
    """ print to csv file """
    # 'C:/Users/Davide Pederzoli/Documents/Python Scripts/outfile.txt'
    f = open(out_file_name, 'wb')
    writer = csv.writer(f)
    dao = Daos.base(db, clazz)
    for item in dao.getAll():
        """strRow =  item.name + " " + item.getRefId()"""
        #loc = item.location
        locName = "" if item.location is None else item.location.name
        locCode = "" if item.location is None else item.location.code
        locRefId = "" if item.location is None else item.location.refId
        strCat = ""
        #strCat = item.category
        #for cat in item.category.name:
            #strCat = cat  + "\"
        #childcat =  item.category.childCategories
        #loc_name = loc("name")
        #tmplog.info(item.name.encode('utf-8'))
        # https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
        writer.writerow([item.name.encode('utf-8'), item.category, item.refId, locName.encode('utf-8'), locCode, locRefId])
    #sys.stdout.write("prova")
    f.close()

def printProcess2csv(db, RefId, out_file_name):
    """ print to csv file """
    #"C:/Users/Davide Pederzoli/Documents/Python Scripts/{0}".format(out_file_name)
    f = open(out_file_name, 'wb')
    writer = csv.writer(f)
    process_ref = find_byRefId(db, model.Process, RefId)
    exchangeList = process_ref.exchanges
    for item in exchangeList:
        """strRow =  item.name + " " + item.getRefId()"""
        fl = item.flow
        fl_name = fl.name
        fl_RefId = fl.refId
        fl_isInput = item.isInput
        fl_amount = item.amount
        fl_amountFormula = item.amountFormula
        fl_unit = item.unit.name
        writer.writerow([fl_name, fl_isInput, fl_unit, fl_amount, fl_amountFormula, fl_RefId])
    f.close()

def getJSONfile(file_name):
    #"F:/DOTTORATO UNIGE/PUBBLICAZIONE ARTICOLO/OpenLCA/{0}".format(file_name)
    fin = open(file_name, 'r')
    json_string = fin.readlines()[0][:-1]
    json_string = json_string.replace("True", "true").replace("False", "false")
    data = json.loads(json_string)
    return data

def LoadJSONfile(file_name, debugMode = False):
  data = {}
  try:
    fin = open(file_name, 'r')
    if debugMode:
      tmpLines = fin.readlines()
      log_text(tmpLines[0])
      json_string = tmpLines[0]
    else:
      json_string = fin.readlines()[0]
      data = json.loads(json_string)
  except OSError as err:
    log_text("OS error: {0}".format(err))
  return data

def LoadCategoryFile(file_name):
  with open(file_name, 'r') as csv_in:
    csv_reader = csv_in.readlines()
    lst = []
    for line in csv_reader:
      catList = line.rstrip("\n").rstrip("\t").split("\t")
      lst.append(catList)
    csv_in.close()
  return lst

def LoadTextFilebyRow(file_name):
  with open(file_name, 'r') as csv_in:
    csv_reader = csv_in.readlines()
    lst = []
    for line in csv_reader:
      catList = line.rstrip("\n").rstrip("\t").split("\t")
      if len(catList) > 0:
        lst.append(catList)
    csv_in.close()
  return lst

def writeJSONfile(file_name, data):
  # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
  fin = open(file_name, 'w')
  json.dump(data, fin)
  fin.close()

def openJSONfile(file_name):
  fin = open(file_name, 'r')
  data = json.load(fin)
  fin.close()
  return data

def getParamRedefList(ListArray):
  ProcessRefIdList = list(set([_[0] for _ in ListArray]))
  jsonDict = {}
  for ProcessRefIdLItem in ProcessRefIdList:
    k = [_[1] for _ in ListArray if _[0] == ProcessRefIdLItem]
    v = [float(_[2]) for _ in ListArray if _[0] == ProcessRefIdLItem]
    jsonDict[ProcessRefIdLItem] = dict(zip(k, v))
  return jsonDict

def convert2file(dictionary, fileName):
  # ************************************************************************
  # Task 1. From dict to list of list, e.g. {k : v,...} -> [[k, v], ...]
  toList = [[x, y] for x,y in dictionary.items()]
  # Task 2. Save list to file
  printList2csv(fileName, toList)
  # Task 3. Load file
  tmp_list = LoadTextFilebyRow(fileName)
  # Task 4. From file to dict
  tmp_dict = dict(zip([_[0] for _ in tmp_list], [_[1] for _ in tmp_list]))
  # Tast 5. Convert string values to typed data
  tmp_dict['amount'] = int(tmp_dict['amount'])
  # https://stackoverflow.com/questions/45396799/convert-string-to-variable-in-python
  tmp_dict['paramRedefList'] = json.loads(tmp_dict['paramRedefList']) if tmp_dict['paramRedefList'][0] == '{' and tmp_dict['paramRedefList'][-1] == '}' else tmp_dict['paramRedefList']
  # ************************************************************************
  return tmp_dict

def paramRedefList2File(paramRedefList, fileName):
  toList = [[[k, x, y] for x,y in paramRedefList[k].items()] for k in paramRedefList.keys()][0]
  printList2csv(fileName, toList)

def getDictionary(fileName):
  # Task 3. Load file
  tmp_list = LoadTextFilebyRow(fileName)
  if tmp_list:
	  # Task 4. From file to dict
	  tmp_dict = dict(zip([_[0] for _ in tmp_list], [_[1] for _ in tmp_list]))
	  #print(tmp_dict)
	  # Tast 5. Convert string values to typed data
	  tmp_dict['amount'] = float(tmp_dict['amount'])
	  # https://stackoverflow.com/questions/45396799/convert-string-to-variable-in-python
	  tmp_dict['paramRedefList'] = json.loads(tmp_dict['paramRedefList']) if tmp_dict['paramRedefList'][0] == '{' and tmp_dict['paramRedefList'][-1] == '}' else getParamRedefList(LoadTextFilebyRow("{0}{1}".format(Config_CLASS.json_path, tmp_dict['paramRedefList'])))
	  # ************************************************************************
  else:
	  tmp_dict = {}
  return tmp_dict

def find_or_create(db, clazz, name, fn):
    obj = find(db, clazz, name)
    return obj if obj is not None else fn()

def add_flow(db, flow_dict):
  name = flow_dict[Flow_dict_CLASS.Name_KEY]
  flow_property = flow_dict[Flow_dict_CLASS.FlowProperty_KEY]
  category = flow_dict[Flow_dict_CLASS.category_KEY]
  flow_type = flow_dict[Flow_dict_CLASS.FlowType_KEY]
  return create_flow_nofind(db, name, flow_property, category, flow_type)

def create_flow_nofind(db, name, flow_property, category, flow_type=model.FlowType.PRODUCT_FLOW):
    flow = model.Flow()
    flow.flowType = flow_type
    flow.name = name
    flow.referenceFlowProperty = flow_property
    flow.refId = UUID.randomUUID().toString()
    flow.category = category
    fp_factor = model.FlowPropertyFactor()
    fp_factor.flowProperty = flow_property
    fp_factor.conversionFactor = 1.0
    flow.flowPropertyFactors.add(fp_factor)
    insert(db, flow)
    #FlowDao(db).insert(flow)
    return flow

def create_flow(db, name, flow_property, category, flow_type=model.FlowType.PRODUCT_FLOW):
    flow = find(db, model.Flow, name)
    if flow is not None:
        return flow
    flow = model.Flow()
    flow.flowType = flow_type
    flow.name = name
    flow.referenceFlowProperty = flow_property
    flow.refId = UUID.randomUUID().toString()
    flow.category = category
    fp_factor = model.FlowPropertyFactor()
    fp_factor.flowProperty = flow_property
    fp_factor.conversionFactor = 1.0
    flow.flowPropertyFactors.add(fp_factor)
    insert(db, flow)
    return flow

def create_exchange(flow, amount=1.0, is_input=False):
    e = model.Exchange()
    e.input = is_input
    e.flow = flow
    e.unit = flow.referenceFlowProperty.unitGroup.referenceUnit
    e.amountValue = amount
    e.flowPropertyFactor = flow.getReferenceFactor()
    return e

def find_exchange(flow, process):
    for e in process.exchanges:
        if e.flow == flow:
            return e

def get_process(pr_dao, ref_id):
  return pr_dao.getForRefId(ref_id)

def get_exchange(process, flow_ref_id):
  for exchange in process.exchanges:
    if exchange.flow and exchange.flow.refId == flow_ref_id:
      return exchange

def get_parameter(process, parameter_name):
  for parameter in process.parameters:
    if parameter.name == parameter_name:
      return parameter
  return None

def create_product_system(db, ref_process, name, target_amount):
  system = ProductSystem.from(ref_process);
  system.name = name
  system.targetAmount = target_amount
  return ProductSystemDao(db).insert(system)

def auto_link_system(db, system):
  config = LinkingConfig()
  config.preferredType = ProcessType.UNIT_PROCESS
  config.providerLinking = DefaultProviders.PREFER
  cache = MatrixCache.createLazy(db)
  builder = ProductSystemBuilder(cache, config)
  builder.autoComplete(system)
  return builder.saveUpdates(system)

def calculate(db, system, impact_method, allocation = AllocationMethod.NONE):
  cache = MatrixCache.createLazy(db)
  setup = CalculationSetup(CalculationType.UPSTREAM_ANALYSIS, system)
  log_text("setup OK")
  setup.impactMethod = Descriptors.toDescriptor(impact_method)
  log_text("setup.impactMethod OK")
  setup.parameterRedefs.addAll(system.parameterRedefs)
  log_text("setup.parameterRedefs.addAll OK")
  setup.allocationMethod = allocation
  log_text("setup.allocationMethod OK")
  calculator = SystemCalculator(cache, App.getSolver())
  log_text("calculator OK")
  result = calculator.calculateFull(setup)
  log_text("calculateFull OK")
  return [setup, result]
  
def get_DQS(ProductSystemObj, DQS_Obj, tmpAggregationType = AggregationType.WEIGHTED_AVERAGE, tmpRoundingMode = RoundingMode.CEILING, tmpProcessingType = ProcessingType.EXCLUDE):
  DQSetup = DQCalculationSetup()
  DQSetup.productSystemId = ProductSystemObj.id
  DQSetup.aggregationType = tmpAggregationType
  DQSetup.roundingMode = tmpRoundingMode
  DQSetup.processingType = tmpProcessingType
  DQSetup.processDqSystem = DQS_Obj
  DQSetup.exchangeDqSystem = DQS_Obj
  return DQSetup

def get_category(model_type, path):
  full_path = []
  full_path.append(model_type.name())
  for p in path:
    full_path.append(p)
  ref_id = KeyGen.get(full_path);
  return CategoryDao(Database.get()).getForRefId(ref_id)

def add_category(model_type, parent_category, name):
  category = Category()
  category.name = name
  category.refId = UUID.randomUUID().toString()
  category.modelType = model_type
  category.category = parent_category
  if not parent_category:
    return CategoryDao(Database.get()).insert(category)
  parent_category.childCategories.add(category)
  parent_category = CategoryDao(Database.get()).update(parent_category)
  for child in parent_category.childCategories:
    if child.name == name:
      return child

def add_category_list(model_type,root_category, category_list):
  for catItem in category_list:
    tmpLst = []
    i = 0
    for cat in catItem:
      tmpLst.append(cat)
      log_text("Category[{0}]: {1}".format(i, cat))
      flow_category = get_category(model_type, tmpLst)
      if flow_category is None:
        if i == 0:
          log_text("select root category")
          root_flow_category = get_category(model_type, root_category)
          log_text("add at root category")
          add_category(model_type, root_flow_category, cat)
        else:
          log_text("select parent category")
          parent_flow_category = get_category(model_type, tmpLst[:i])
          log_text("num of parent category is {0}".format(len(tmpLst[:i])))
          log_text("add category")
          add_category(model_type, parent_flow_category, cat)
      else:
        log_text("already exisits, OK")
      i = i + 1

def print_class(clsRef):
  # helper functions
  get_class_all_item = lambda x : [a for a in dir(x) if not a.startswith('__')]
  get_class_obj = lambda x: [a for a in dir(x) if not a.startswith('__') and callable(getattr(x, a))]
  get_class_attr = lambda x: list(set(get_class_all_item(x)) - set(get_class_obj(x)))
  # loop root class attributes
  for attr in get_class_attr(clsRef):
  	log_text("Root Class Attribute: '{0}' = {1}".format(attr, clsRef.__dict__[attr]))
  # loop innerClass class attributes
  for innerClass in get_class_obj(clsRef):
    log_text("Inner Class: '{0}'".format(innerClass))
    innerClassRef = clsRef.__dict__[innerClass]
    for attr in get_class_attr(innerClassRef):
      log_text("[{0}] Attribute: '{1}' = {2}".format(innerClass, attr, innerClassRef.__dict__[attr]))

def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None

def create_process_from_template(jsonFileIn, jsonFileOut):
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


  jsonFilePath = "{0}{1}".format(Config_CLASS.json_path, jsonFileIn)

  process_DICT = openJSONfile(jsonFilePath)

  """
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

  """

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
      # save the updated process_DICT.
      jsonFilePath = "{0}{1}".format(Config_CLASS.json_path, jsonFileOut)
      writeJSONfile(jsonFilePath, process_DICT)
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
    #Selected_keys = [_ for _ in Flow_DICT if _[Process_CLASS.Exchange_CLASS.defaultProvider][Process_CLASS.DefaultProvider_CLASS.defaultProviderRefId]]
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

def create_template_from_process(processObj, jsonFileOut):
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

  FlowProperty_DICT = {"Mass" : mass, "Items" : items, "Energy" : energy, "Volume" : volume, "Good Transport": good_transport}

  """
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

  """
  # ****************************************************************************
  process_DICT = {}
  # set empty values in the dictionary and in the Exchange list
  process_DICT[Process_CLASS.Parameter_DICT_KEY] = {}
  process_DICT[Process_CLASS.Exchange_DICT_KEY] = []
  process_DICT[Process_CLASS.Reference_Flow_DICT_KEY] = {}
  process_DICT[Process_CLASS.Category_Process_KEY] = ""
  process_DICT[Process_CLASS.RefId_KEY] = ""
  process_DICT[Process_CLASS.Name_KEY] = ""
  process_DICT[Process_CLASS.LocationCode_KEY] = ""
  process_DICT[Process_CLASS.LocationRefId_KEY] = ""
  # ****************************************************************************
  FlowTypeObj = FlowType_CLASS()
  # ****************************************************************************
  process_category_path = Strings.join(Categories.path(processObj.category), '/')
  # ****************************************************************************
  log_text("Processs name: '{0}'".format(processObj.name))
  log_text("Processs category: '{0}'".format(process_category_path))
  # ****************************************************************************
  if processObj.location is None:
    log_text("Location is empty, adding default 'RER' location code...")
    RER_RefId = 'd66c264e-1dbd-33e6-911d-3ffc70908e8e'
    locationRER_Obj = location_dao.getForRefId(RER_RefId)
    processObj.location = locationRER_Obj
    process_DICT[Process_CLASS.LocationCode_KEY] = locationRER_Obj.code
    process_DICT[Process_CLASS.LocationRefId_KEY] = locationRER_Obj.refId
  else:
    log_text("Location name: '{0}'".format(processObj.location.name))
    process_DICT[Process_CLASS.LocationCode_KEY] = processObj.location.code
    process_DICT[Process_CLASS.LocationRefId_KEY] = processObj.location.refId
  # ****************************************************************************
  # STEP 1: PROCESS DEFINITION
  # ****************************************************************************
  # Process object attributes
  process_DICT[Process_CLASS.Name_KEY] = processObj.name
  process_DICT[Process_CLASS.Category_Process_KEY] = process_category_path
  process_DICT[Process_CLASS.RefId_KEY] = processObj.refId
  process_DICT[Process_CLASS.LocationCode_KEY] = processObj.location.code
  process_DICT[Process_CLASS.LocationRefId_KEY] = processObj.location.refId
  # ****************************************************************************
  # STEP 2: REFERENCE PROCESS DEFINITION
  # ****************************************************************************
  RefFlowObj = processObj.quantitativeReference
  log_text("Reference Flow name: '{0}'".format(RefFlowObj.flow.name))
  log_text("Reference Flow refId: '{0}'".format(RefFlowObj.flow.refId))
  log_text("Reference Flow category: '{0}'".format(RefFlowObj.flow.category.name))
  log_text("Reference Flow Property: '{0}'".format(RefFlowObj.flow.referenceFlowProperty.name))
  # Sets values into the dictionary
  process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.name] = RefFlowObj.flow.name
  process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.RefId] = RefFlowObj.flow.refId
  process_DICT[Process_CLASS.Reference_Flow_DICT_KEY][Process_CLASS.Reference_Flow_CLASS.referenceFlowProperty] = RefFlowObj.flow.referenceFlowProperty.name
  # ****************************************************************************
  # STEP 3: EXCHANGE FLOWS DEFINITION
  # ****************************************************************************
  exchange_list = processObj.exchanges
  # loop through the exchange list
  for exch in exchange_list:
    Exchange_DICT = {}
    log_text("Exchange Flow name: '{0}'".format(exch.flow.name))
    log_text("Category: '{0}'".format(exch.flow.category.name)) #toString()
    log_text("Exchange [{0}] amount: '{1}'".format(exch.flow.name, exch.amount))
    log_text("Exchange [{0}] amountFormula: '{1}'".format(exch.flow.name, exch.amountFormula))
    log_text("Exchange [{0}] Unit: '{1}'".format(exch.flow.name, exch.unit.name))
    log_text("Exchange [{0}] isInput: '{1}'".format(exch.flow.name, exch.isInput))
    log_text("Exchange [{0}] refId: '{1}'".format(exch.flow.name, exch.flow.refId))
    log_text("Exchange [{0}] unitGroup: '{1}'".format(exch.flow.name, exch.flow.referenceFlowProperty.unitGroup.name))
    log_text("Exchange [{0}] unit name: '{1}'".format(exch.flow.name, exch.flow.referenceFlowProperty.name))
    log_text("Exchange [{0}] default provider id: '{1}'".format(exch.flow.name, exch.defaultProviderId))
    log_text("Exchange [{0}] isQuantitativeReference: '{1}'".format(exch.flow.name, "True" if exch.flow.refId == RefFlowObj.flow.refId else "False"))
    # Sets values into the dictionary
    # ****************************************************************************
    # STEP 3.1: SET FLOW OBJECT REFERENCE TO EXCHANGE
    # ****************************************************************************
    log_text("Exchange [{0}] flow type: '{1}'".format(exch.flow.name, FlowTypeObj.getFlowTypeName(exch.flow.flowType)))
    ExchangeFlowObj = Flow_TEMPLATE_CLASS(exch.flow.name,
    FlowTypeObj.getFlowTypeName(exch.flow.flowType),
    exch.flow.referenceFlowProperty.name,
    exch.flow.refId,
    "" if exch.flow.description is None else exch.flow.description,
    Strings.join(Categories.path(exch.flow.category), '/'))
    #****************************************************************************
    Exchange_DICT[Process_CLASS.Exchange_CLASS.flow] = Obj2dict(ExchangeFlowObj)
    # ****************************************************************************
    Exchange_DICT[Process_CLASS.Exchange_CLASS.isInput] = "True" if exch.isInput else "False"
    Exchange_DICT[Process_CLASS.Exchange_CLASS.FlowProperty] = exch.flow.referenceFlowProperty.name
    Exchange_DICT[Process_CLASS.Exchange_CLASS.amount] = exch.amount
    Exchange_DICT[Process_CLASS.Exchange_CLASS.amountFormula] = exch.amountFormula
    Exchange_DICT[Process_CLASS.Exchange_CLASS.isQuantitativeReference] = "True" if exch.flow.refId == RefFlowObj.flow.refId else "False"
    # ****************************************************************************
    # STEP 3.2: SET DEFAULT PROVIDER TO EXCHANGE
    # ****************************************************************************
    # defualt provider object reference
    Exchange_DICT[Process_CLASS.Exchange_CLASS.defaultProvider] = {}
    # define empty DefaultProvider_DICT
    DefaultProvider_DICT = {}
    # get default provider object reference
    defaultProviderObj = find_byId(db, model.Process, exch.defaultProviderId)
    if defaultProviderObj is None:
      log_text("####Exchange [{0}] default provider empty".format(exch.flow.name))
    else:
      log_text("####Exchange [{0}] default provider name: '{1}'".format(exch.flow.name, defaultProviderObj.name))
      log_text("####Exchange [{0}] default provider Location Code: '{1}'".format(exch.flow.name, "" if defaultProviderObj.location is None else defaultProviderObj.location.code))
    # assign values to DefaultProvider_DICT
    DefaultProvider_DICT[Process_CLASS.DefaultProvider_CLASS.defaultProviderName] = "" if defaultProviderObj is None else defaultProviderObj.name
    DefaultProvider_DICT[Process_CLASS.DefaultProvider_CLASS.defaultProviderRefId] = "" if defaultProviderObj is None else defaultProviderObj.refId
    DefaultProvider_DICT[Process_CLASS.DefaultProvider_CLASS.defaultProviderLocationCode] = "" if defaultProviderObj is None else "" if defaultProviderObj.location is None else defaultProviderObj.location.code
    DefaultProvider_DICT[Process_CLASS.DefaultProvider_CLASS.defaultProviderLocationRefId] = "" if defaultProviderObj is None else "" if defaultProviderObj.location is None else defaultProviderObj.location.refId
    # set DefaultProvider_DICT to exchange dictionary
    Exchange_DICT[Process_CLASS.Exchange_CLASS.defaultProvider] = DefaultProvider_DICT
    #log_text("There are no default provider for the selected flow")
    # add the the Exchange_DICT object to the flows list
    process_DICT[Process_CLASS.Exchange_DICT_KEY].append(Exchange_DICT)
  # ****************************************************************************
  # STEP 4: INPUT PARAMETERS DEFINITION
  # ****************************************************************************
  param_list = processObj.parameters
  # loop through the parameter list
  for pm in param_list:
    parameter_DICT = {}
    log_text("parameter name: {0} = {1}, formula = '{2}'".format(pm.name, pm.value, pm.formula))
    log_text("parameter name: {0}, description = '{1}'".format(pm.name, pm.description))
    log_text("parameter name: {0}, isInputParameter = {1}".format(pm.name, pm.isInputParameter))
    # Sets values into the dictionary
    parameter_DICT[Process_CLASS.Parameter_CLASS.IsInputParameter] = "True" if pm.isInputParameter else "False"
    parameter_DICT[Process_CLASS.Parameter_CLASS.value] = pm.value
    parameter_DICT[Process_CLASS.Parameter_CLASS.description] = pm.description
    parameter_DICT[Process_CLASS.Parameter_CLASS.formula] = pm.formula
    # set the parameter_DICT to the process_DICT
    process_DICT[Process_CLASS.Parameter_DICT_KEY][pm.name] = parameter_DICT
  # ****************************************************************************
  # STEP 5: SAVE JSON FILE TO DISK
  # ****************************************************************************
  jsonFilePath = "{0}{1}".format(Config_CLASS.json_path, jsonFileOut)
  writeJSONfile(jsonFilePath, process_DICT)

def getTotalResult(result, jsonOutFileName):
  db = Database.get()
  process_dao = ProcessDao(db)
  Param_dao = ParameterDao(db)
  location_dao = LocationDao(db)
  flow_dao = FlowDao(db)
  fp_dao = FlowPropertyDao(db)
  impact_method_dao = ImpactMethodDao(db)
  impact_category_dao = ImpactCategoryDao(db)
  location_dao = LocationDao(db)

  # calculates the number of flow result from the elaboration.
  countTotalFlowResults = count_iterable(result.getTotalFlowResults())
  countINPUT_FlowResults = sum(1 for _ in result.getTotalFlowResults() if _.input is True)
  log_text("Number of FlowResult: {0}".format(countTotalFlowResults))
  log_text("Number of INPUT FlowResult: {0}".format(countINPUT_FlowResults))
  log_text("Number of OUTPUT FlowResult: {0}".format(countTotalFlowResults - countINPUT_FlowResults))
  # **********************************************************************
  # TASK 1
  # builds list with the total flow results flow.name, flow.refId, flow.value
  FlowResultsList = {}
  for FlowResultElement in result.getTotalFlowResults():
    FlowResultsList[FlowResultElement.flow.refId] = FlowResultElement.value
  # **********************************************************************
  # TASK 2
  # builts list with the impact factor associated to the selected impact category
  jsonFilePath = "{0}{1}".format(Config_CLASS.json_path, Config_CLASS.impact_method_file)
  methods_list = openJSONfile(jsonFilePath)
  # **********************************************************************
  # TASK 3
  # builds the dictiorary with the selectd impact category
  mth = {}
  for methodItem in methods_list.keys():
    impCat = {}
    for impactCategory in methods_list[methodItem].keys():
      ic_refId = methods_list[methodItem][impactCategory] # Gets the impact category refId
      impactCatObj = impact_category_dao.getForRefId(ic_refId) # Gets the impact category object reference
      # Checks if the impact category satisfies the requested conditions:
      # 1. regular expression for string searching
      # 2. the unit has to be equal to "kg CO2 eq"
      log_text("methodItem [{0}], icObj.referenceUnit: [{1}]".format(methodItem, impactCatObj.referenceUnit))
      #if bool(re.match(Config_CLASS.global_warming_regexp_pattern, impactCategory)) and "kg CO2 eq" in impactCatObj.referenceUnit:
        #log_text("Impact Category OK: {0}".format(impactCategory.name))
        # Assigns the refId to the impact category
      impCat[impactCategory] = ic_refId
      # Assigns the impCat dictionary to the method dictionary of the selected key
      mth[methodItem] = impCat
    #log_text("Mehod: {0}, impactFactorList len is: {1}".format(methodItem, len(impCat.keys())))
  # **********************************************************************
  # TASK 4
  # selects the methods that satisfy the selection criteria
  selected_method_list = [m for m in mth.keys() if len(mth[m].keys()) > 0]
  # just prints the select methods list
  for method_item in selected_method_list:
    log_text("Mehod: {0}, impact category List len is: {1}".format(method_item, len(mth[method_item].keys())))
  # **********************************************************************
  # TASK 5
  # loops through the method lists to perform the calculations
  # Initializes the result dictiornary
  results_DICT = {}
  for method_item in selected_method_list:
    # TASK 5.1: loops thorugh the categories of the selected method
    # initialize the impact category dictionary
    impactCat_DICT = {}
    for cc in mth[method_item].keys():
      log_text("Mehod: {0}, impact category: {1}".format(method_item, cc))
      # TASK 5.2: gets the object reference of the selected impact category via refId
      impactCatObj = impact_category_dao.getForRefId(mth[method_item][cc])
      # TASK 5.3 builts list with the impact factor associated to the selected impact category
      impactFactorList = {} # initializes the dictiornary
      # Loops through the impact factors in the selected impact category
      for impactFactor in impactCatObj.impactFactors:
        # Assigns the the impact factor value to the dictionary with the corresponding flow refId
        impactFactorList[impactFactor.flow.refId] = impactFactor.value
      log_text("impactFactorList len is: {0}".format(len(impactFactorList.keys())))
      # TASK 5.4: performs the calculations and gets the result value
      cc_result = sum(FlowResultsList[flowrefId] * impactFactorList[flowrefId] for flowrefId in FlowResultsList.keys() if flowrefId in impactFactorList.keys())
      log_text("{0} [{1}] = {2}".format(impactCatObj.name, impactCatObj.referenceUnit, cc_result))
      """
      Assings:

        1 the category referenceUnit with Key "referenceUnit"
        2 the result value with Key "result"

       to the 'impactCat_DICT' dictionary
      """
      impactCat_DICT[cc] = {"referenceUnit" : impactCatObj.referenceUnit, "result" : cc_result}
      # Assigns the impact dictionary to the reults dictionary
      results_DICT[method_item] = impactCat_DICT
  # **********************************************************************
  # TASK 6: Saves the result dictionary to a file
  jsonFilePath = "{0}{1}".format(Config_CLASS.json_path, jsonOutFileName)
  writeJSONfile(jsonFilePath, results_DICT)

def getUpstreamTreeData3(fileObj, resultObj, impactCategoryObj, UpStreamNodeObj, level, customLevel, parentAmount = 1.0, indent = 1):
  level = customLevel[UpStreamNodeObj.provider.process.name] if UpStreamNodeObj.provider.process.name in customLevel.keys() else level
  if level > 0:
    for itemNodeObj in resultObj.getTree(impactCategoryObj).childs(UpStreamNodeObj):
      log_text(indent * "\t" + "UpStreamNodeObj.item.name = '{0}'".format(itemNodeObj.provider.process.name.encode('utf-8')))
      log_text(indent * "\t" + "UpStreamNodeObj.result = '{0}', share: {1} [%]".format(itemNodeObj.result, (0.0 if parentAmount == 0.0 else itemNodeObj.result / parentAmount) * 100.0))
      lst = [itemNodeObj.provider.process.name.encode('utf-8'), str(itemNodeObj.result).encode('utf-8').replace('.',','), str(0.0 if parentAmount == 0.0 else itemNodeObj.result / parentAmount).encode('utf-8').replace('.',',')]
      fileObj.write(indent * "\t" + '\t'.join(lst) + "\n")
      getUpstreamTreeData3(fileObj, resultObj, impactCategoryObj, itemNodeObj, level - 1, customLevel, itemNodeObj.result, indent + 1)

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


  """
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

  """

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
