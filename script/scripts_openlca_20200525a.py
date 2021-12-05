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

  FlowProperty_DICT = {"Mass" : mass, "Items" : items, "Energy" : energy, "Volume" : volume, "Good Transport": good_transport, "Area" : area}

  # process refId
  inventory_id = '606b41ee-3cef-4341-84c6-969db7165589'

  inventory = util.get_process(process_dao, inventory_id)

  # Impact Method refId
  method_id = 'b0f6a3ba-a0be-3bfe-ae43-4e23c241e4b6'
  # Climate change [kg CO2 eq] -- refId = b3c4cee1-4bdf-3289-b1b1-14c48189462d -- id = 4517284
  impcat_id = 'b3c4cee1-4bdf-3289-b1b1-14c48189462d'

  method = impact_method_dao.getForRefId(method_id)
  impactCatObj = impact_category_dao.getForRefId(impcat_id)

  log_text(method.name)

  # calculates the number of flow result from the elaboration.
  countTotalFlowResults = util.count_iterable(inventory.exchanges)
  countINPUT_FlowResults = sum(1 for _ in inventory.exchanges if _.isInput is True)
  log_text("Number of FlowResult: {0}".format(countTotalFlowResults))
  log_text("Number of INPUT FlowResult: {0}".format(countINPUT_FlowResults))
  log_text("Number of OUTPUT FlowResult: {0}".format(countTotalFlowResults - countINPUT_FlowResults))
  # builds list with the total flow results flow.name, flow.refId, flow.value
  FlowResultsList = {}
  for FlowResultElement in inventory.exchanges:
    FlowResultsList[FlowResultElement.flow.refId] = FlowResultElement.amount
  # builts list with the impact factor associated to the selected impact category
  impactFactorList = {}
  for impactFactor in impactCatObj.impactFactors:
    impactFactorList[impactFactor.flow.refId] = impactFactor.value
  log_text("impactFactorList len is: {0}".format(len(impactFactorList.keys())))
  # performs the calculations and gets the result value
  cc_result = sum(FlowResultsList[flowrefId] * impactFactorList[flowrefId] for flowrefId in FlowResultsList.keys() if flowrefId in impactFactorList.keys())
  log_text("{0} = {1}".format(impactCatObj.name, cc_result))
