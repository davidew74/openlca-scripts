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


def log_text(text):
  log.info(text)

def refresh():
  Navigator.refresh()

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
  #length = util.find(db, model.FlowProperty, 'Length')
  length = fp_dao.getForName('Length')[0]
  #volume = util.find(db, model.FlowProperty, 'Volume')
  volume = fp_dao.getForName('Volume')[0]

  FlowProperty_DICT = {"Mass" : mass, "Items" : items, "Energy" : energy, "Volume" : volume, "Good Transport": good_transport, "Area" : area, "Length" : length, "Volume" : volume}

  # get object instance (FOR TEST PURPOSES)
  # hydrogen fuel cell bus, end-of-life (recycling scenario) (copy)
  process = util.get_process(process_dao, "8e87feb3-14db-4025-a20c-b37ee7ce7248")

  """
    delete a parameter from a process
  """
  param_obj = util.get_parameter(process, "Prova")
  if param_obj:
    log_text("parameter name: '{0}' found".format(param_obj.name))
    # remove parameter's object from parameter's list
    process.parameters.remove(param_obj)
    # delete object reference from parameter's database
    Param_dao.delete(param_obj)
    # update process
    process_dao.update(process)
  """
    delete an exchange from a process
  """
  listExchangeFlowRefId = [_.flow.refId for _ in process.exchanges]
  flowRefId = "f80416c8-f598-4c5d-8723-e3ca751de5ba"
  if flowRefId in listExchangeFlowRefId:
    # https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
    log_text("There are {0} occurance of the selected flow".format(listExchangeFlowRefId.count(flowRefId)))
    for exch in [_ for _ in process.exchanges if _.flow.refId == flowRefId]:
      Exchange_obj = util.get_exchange(process, exch.flow.refId)
      log_text("Exchange [{0}] found".format(Exchange_obj.flow.name))
      log_text("Exchange [{0}] default provider id: '{1}'".format(Exchange_obj.flow.name, Exchange_obj.defaultProviderId))
      # get default provider object reference
      defaultProviderObj = util.find_byId(db, model.Process, Exchange_obj.defaultProviderId)
      log_text("default provider name: '{0}'".format(defaultProviderObj.name))
      # remove exchange's object from parameter's list
      process.exchanges.remove(Exchange_obj)
      # update process
      process_dao.update(process)
  """
    delete an a process
  """
  process = util.get_process(process_dao, "55053797-3f28-4930-b48e-9cd75b159e1a")
  if process:
    process_dao.delete(process)
  else:
      log_text("process is not in the database")

  App.runInUI('Refreshing', refresh)
