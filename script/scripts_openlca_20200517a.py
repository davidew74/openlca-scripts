from java.io import File
from java.util import UUID
from java.util import Date

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
import org.openlca.util.Strings as Strings
import org.openlca.util.Categories as Categories

# https://github.com/GreenDelta/olca-app/tree/master/olca-app/src/org/openlca/app/db
import org.openlca.app.db.Cache as Cache
import org.openlca.app.db.Database as Database
import org.openlca.app.App as App
import org.openlca.app.navigation.Navigator as Navigator

import org.openlca.core.results.SystemProcess as SystemProcess

#import util

import re

import imp
util = imp.load_source('module.name', 'C:/Users/Davide Pederzoli/Documents/Python Scripts/util.py')

"""

"""
def log_text(text):
  log.info(text)
"""

"""
def get_category(model_type, path):
  full_path = []
  full_path.append(model_type.name())
  for p in path:
    full_path.append(p)
  ref_id = KeyGen.get(full_path);
  return category_dao.getForRefId(ref_id)
"""

"""
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
"""

"""
def create_product_system(ref_process, name, target_amount):
  system = ProductSystem.from(ref_process)
  system.name = name
  system.targetAmount = target_amount
  return product_system_dao.insert(system)
"""

"""
def auto_link_system(system):
  config = LinkingConfig()
  config.preferredType = ProcessType.UNIT_PROCESS
  config.providerLinking = DefaultProviders.PREFER
  builder = ProductSystemBuilder(cache, config)
  builder.autoComplete(system)
  return builder.saveUpdates(system)
"""

"""
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
"""

"""
def refresh():
  Navigator.refresh()
"""

"""
def add_category_list(model_type,root_category, category_list):
  # check if category_list variable is a list, if not it is converted into a list datatype
  category_list = category_list if type(category_list) == list else [category_list]
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
"""

"""
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

set_underscore = lambda x : x.replace(" ", "_").replace(",", "_")

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
  impact_category_dao = ImpactCategoryDao(db)
  location_dao = LocationDao(db)

  product_system_dao = ProductSystemDao(db)
  cache = MatrixCache.createLazy(db)

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

  FlowProperty_DICT = {"Mass" : mass, "Items" : items, "Energy" : energy, "Volume" : volume, "Good Transport": good_transport, "Area" : area}

  # ****************************************************************************
  # Impact Method refId
  method_id = 'b0f6a3ba-a0be-3bfe-ae43-4e23c241e4b6'
  # get method instance
  method = impact_method_dao.getForRefId(method_id)
  # ***********************************************************************************
  # process refId
  process_id = "e0f53058-ce21-4ab4-8e9b-5391ceb33cb0"
  # get object instance
  process = util.get_process(process_dao, process_id)
  # Product System Name
  product_system_name = 'lithium ion battery'
  # Inventory Process Name
  inventory_process_name = "lithium ion battery inventory"
  # json file name
  jsonFileName = "lithium_ion_battery_results_ALL_IMPACTS_DICT.json"
  # manages the cache area for the result object
  key = "lithium_ion_battery_resultKey"
  # ***********************************************************************************
  appCache = Cache.getAppCache()
  result = appCache.remove(key)
  # checks if result object in the cache memory
  if result is None:
    log_text("Cache Empty")
    system = create_product_system(process, product_system_name, 1)
    auto_link_system(system)
    log_text("Product System refId = '{0}'".format(system.refId))
    result = calculate(system, method)
    log_text("Results OK")
    appCache.put(key, result)
    log_text("Add result data to Cache")
    util.getTotalResult(result, jsonFileName)
  else:
    log_text("Cache OK")
    appCache.put(key, result)
    ProductSystemObj = product_system_dao.getForName(product_system_name)[0]
    # Check Prodcut System
    if not ProductSystemObj:
      log_text("Product System to be created")
      system = create_product_system(process, product_system_name, 1)
      auto_link_system(system)
    else:
      log_text("Product System already present")
      system = ProductSystemObj
    log_text("Product System refId = '{0}'".format(system.refId))
    inventoryProcessObj = process_dao.getForName(inventory_process_name)[0]
    # Check inventory Process
    if not inventoryProcessObj:
      log_text("inventory Process to be created")
      setup = CalculationSetup(CalculationType.UPSTREAM_ANALYSIS, system)
      log_text("setup OK")
      setup.impactMethod = Descriptors.toDescriptor(method)
      inventoryProcessObj = SystemProcess.createWithMetaData(Database.get(), setup, result, inventory_process_name)
      inventoryProcessObj = process_dao.insert(inventoryProcessObj)
    else:
      log_text("inventory Process already present")
    log_text("inventory Process refId = '{0}'".format(inventoryProcessObj.refId))
  # **********************************************************************
  util.getTotalResult(result, jsonFileName)

  # Refreshes the application to update the navigation treeview
  App.runInUI('Refreshing', refresh)
