from java.io import File
from java.util import UUID
from java.util import Date

import org.openlca.core.database.derby.DerbyDatabase as DerbyDatabase
import org.openlca.core.database.CategoryDao as CategoryDao
import org.openlca.core.database.Daos as Daos
import org.openlca.core.database.FlowDao as FlowDao
import org.openlca.core.database.FlowPropertyDao as FlowPropertyDao
import org.openlca.core.database.ImpactMethodDao as ImpactMethodDao
import org.openlca.core.database.ProcessDao as ProcessDao
import org.openlca.core.database.ProductSystemDao as ProductSystemDao
import org.openlca.core.database.ParameterDao as ParameterDao
import org.openlca.core.database.UnitGroupDao as UnitGroupDao
import org.openlca.core.database.LocationDao as LocationDao

import org.openlca.core.model as model
import org.openlca.core.model.FlowPropertyFactor as FlowPropertyFactor
import org.openlca.core.model.Parameter as Parameter
import org.openlca.core.model.ParameterScope as ParameterScope
import org.openlca.core.model.Category as Category
import org.openlca.core.model.ImpactMethod as ImpactMethod
import org.openlca.core.model.ImpactCategory as ImpactCategory
import org.openlca.core.model.ImpactFactor as ImpactFactor
import org.openlca.core.model.ModelType as ModelType
import org.openlca.core.model.ProcessType as ProcessType
import org.openlca.core.model.ProductSystem as ProductSystem
import org.openlca.core.model.descriptors.Descriptors as Descriptors
import org.openlca.core.model.Location as Location

import org.openlca.core.matrix.LinkingConfig as LinkingConfig
import org.openlca.core.matrix.LinkingConfig.DefaultProviders as DefaultProviders
import org.openlca.core.matrix.ProductSystemBuilder as ProductSystemBuilder
import org.openlca.core.matrix.cache.MatrixCache as MatrixCache
import org.openlca.core.matrix.solvers.DenseSolver as DenseSolver

import org.openlca.core.math.CalculationSetup as CalculationSetup
import org.openlca.core.math.CalculationType as CalculationType
import org.openlca.core.math.SystemCalculator as SystemCalculator

import org.openlca.util.KeyGen as KeyGen

import org.openlca.app.db.Cache as Cache
import org.openlca.app.App as App
import org.openlca.app.navigation.Navigator as Navigator

#import util

import imp
util = imp.load_source('module.name', 'C:/Users/Davide Pederzoli/Documents/Python Scripts/util.py')


def log_text(text):
  log.info(text)

def get_category(model_type, path):
  full_path = []
  full_path.append(model_type.name())
  for p in path:
    full_path.append(p)
  ref_id = KeyGen.get(full_path);
  return category_dao.getForRefId(ref_id)

def add_category(model_type, parent_category, name):
  category = Category()
  category.name = name
  category.refId = UUID.randomUUID().toString()
  category.modelType = model_type
  category.category = parent_category
  if not parent_category:
    return category_dao.insert(category)
  parent_category.childCategories.add(category)
  parent_category = category_dao.update(parent_category)
  for child in parent_category.childCategories:
    if child.name == name:
      return child

def create_product_system(ref_process, name, target_amount):
  system = ProductSystem.from(ref_process);
  system.name = name
  system.targetAmount = target_amount
  return product_system_dao.insert(system)

def auto_link_system(system):
  config = LinkingConfig()
  config.preferredType = ProcessType.UNIT_PROCESS
  config.providerLinking = DefaultProviders.PREFER
  builder = ProductSystemBuilder(cache, config)
  builder.autoComplete(system)
  return builder.saveUpdates(system)

def calculate(system, impact_method):
  setup = CalculationSetup(CalculationType.UPSTREAM_ANALYSIS, system)
  log_text("setup OK")
  setup.impactMethod = Descriptors.toDescriptor(impact_method)
  log_text("setup.impactMethod OK")
  calculator = SystemCalculator(cache, App.getSolver())
  log_text("calculator OK")
  result = calculator.calculateFull(setup)
  log_text("calculateFull OK")
  return result

def refresh():
  Navigator.refresh()

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
  	log_text("Root Class [{0}] Attribute: '{1}' = {2}".format(clsRef.__name__, attr, clsRef.__dict__[attr]))
  # loop innerClass class attributes
  for innerClass in get_class_obj(clsRef):
    log_text("Inner Class: '{0}'".format(innerClass))
    innerClassRef = clsRef.__dict__[innerClass]
    for attr in get_class_attr(innerClassRef):
      log_text("[{0}] Attribute: '{1}' = {2}".format(innerClass, attr, innerClassRef.__dict__[attr]))


if __name__ == '__main__':


  dataAssocArray = util.LoadJSONfile("{0}{1}".format(util.Config_CLASS.json_path, "ecoinvent35.json"))

  db_dir = File("{0}{1}".format(util.Config_CLASS.db_path, dataAssocArray["ECOINVENT35_APOS_UP_REGIONALISED"]))
  # instantiate the object references
  db = DerbyDatabase(db_dir)
  flow_dao = FlowDao(db)
  fp_dao = FlowPropertyDao(db)
  process_dao = ProcessDao(db)
  Param_dao = ParameterDao(db)
  category_dao = CategoryDao(db)
  impact_method_dao = ImpactMethodDao(db)
  product_system_dao = ProductSystemDao(db)
  cache = MatrixCache.createLazy(db)
  location_dao = LocationDao(db)

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

  Flow_DICT = {"Recyclied_Aluminium_scenario_3" : {"isInput" : False, "FlowProperty" : "Mass", "amount" : 0.0, "amountFormula" : "", "isQuantitativeReference" : False, "RefId" : "x"}}


  log_text("Loading category list")

  category_list = util.LoadCategoryFile("{0}{1}".format(util.Config_CLASS.json_path, util.Config_CLASS.category_list_file))

  add_category_list(util.ModelType_CLASS.ModelType_DICT[util.ModelType_CLASS.ModelType_PRODUCT_SYSTEM], util.ModelType_CLASS.ModelType_ROOT_ELEMENT_DICT[util.ModelType_CLASS.ModelType_PRODUCT_SYSTEM], category_list)
  add_category_list(util.ModelType_CLASS.ModelType_DICT[util.ModelType_CLASS.ModelType_PROCESS], util.ModelType_CLASS.ModelType_ROOT_ELEMENT_DICT[util.ModelType_CLASS.ModelType_PROCESS], category_list)
  add_category_list(util.ModelType_CLASS.ModelType_DICT[util.ModelType_CLASS.ModelType_FLOW], util.ModelType_CLASS.ModelType_ROOT_ELEMENT_DICT[util.ModelType_CLASS.ModelType_FLOW], category_list)

  log_text("Block execution complete")

  print_class(util.Process_CLASS)

  # Gets the file with the names of the processes to add Process_TEMPLATE_DICT3 Process_image_DICT

  jsonFileName = "Process_TEMPLATE_DICT4.json"
  jsonOutFileName = "Process_TEMPLATE_DICT_OUT4.json"

  processA_Obj = util.create_process_from_template(jsonFileName, jsonOutFileName)
  processB_Obj = util.create_process_from_template("Process_TEMPLATE_DICT_B.json", "Process_TEMPLATE_DICT_OUT_B.json")
  processC_Obj = util.create_process_from_template("Process_TEMPLATE_DICT_C.json", "Process_TEMPLATE_DICT_OUT_C.json")

  #processA_Obj = process_dao.getForRefId('a60a7628-ef54-4340-8d91-7d9e1c8046fb')

  refFlow_Obj = processA_Obj.quantitativeReference.flow
  log_text("Referece flow for Process '{0}' is: '{1}'".format(processA_Obj.name, refFlow_Obj.name))

  # create paramter object
  paramObj = util.add_parameter("carbon_dioxide_emissions_input", ParameterScope.PROCESS, util.set_parameter_attributes(True, 1.0, ""))
  # inserts the parameter into the database
  Param_dao.insert(paramObj)
  # Add parameter to the process
  processA_Obj.parameters.add(paramObj)

  ExchangeB = util.Exchange_TEMPLATE_CLASS(processB_Obj.quantitativeReference.flow, "True", 1.0, "", "Mass", "False", processB_Obj)
  ExchangeB_obj = util.get_exchangeObj(ExchangeB)

  processA_Obj.exchanges.add(ExchangeB_obj)

  CO2emissionsObj = flow_dao.getForRefId('643975a8-03da-44bb-873f-4fe8e7740fe6')
  ExchangeCO2emissionsObj = util.Exchange_TEMPLATE_CLASS(CO2emissionsObj, "False", 10.0, paramObj.name, "Mass", "False", None)
  ExchangeCO2_obj = util.get_exchangeObj(ExchangeCO2emissionsObj)

  processA_Obj.exchanges.add(ExchangeCO2_obj)

  process_dao.update(processA_Obj)

  util.create_template_from_process(processA_Obj, jsonOutFileName)


  App.runInUI('Refreshing', refresh)
