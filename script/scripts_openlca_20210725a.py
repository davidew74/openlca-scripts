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

import org.openlca.core.results.SystemProcess as SystemProcess
import org.openlca.core.results.UpstreamNode as UpstreamNode
import org.openlca.core.results.SimulationResult as SimulationResult

#import standard Python libraries to be used
import re
import csv
import imp
import datetime

#import util
util = imp.load_source('module.name', 'C:/Users/Davide Pederzoli/Documents/Python Scripts/util.py')


def log_text(text):
  log.info(text)

def refresh():
  Navigator.refresh()

class ElaboratioFlags(object):
  # flag to enable/disable data save
  Enable_getTotalResult = False
  Enable_SaveImpactCategoryResult = True
  Enable_SaveImpactAnalysis = False
  Enable_MonteCarloSimulation = False

# lambda function declaration
getImpactCategoryObj = lambda impactCategoryName, impactCategoryList : [_ for _ in impactCategoryList if _.name == impactCategoryName][0]
getImpactFactorCategory = lambda flowObj, impactCategoryObj : [_.value for _ in impactCategoryObj.impactFactors if _.flow.refId == flowObj.refId]
getDQSEntry = lambda flowObj, processObj : [_.dqEntry for _ in processObj.exchanges if _.flow.refId == flowObj.refId]

if __name__ == '__main__':

  dataAssocArray = util.LoadJSONfile("{0}{1}".format(util.Config_CLASS.json_path, "ecoinvent35.json"))

  db_dir = File("{0}{1}".format(util.Config_CLASS.db_path, dataAssocArray["ECOINVENT35_APOS_UP_REGIONALISED"]))
  # instantiate the object references
  db = DerbyDatabase(db_dir)
  flow_dao = FlowDao(db)
  fp_dao = FlowPropertyDao(db)
  process_dao = ProcessDao(db)
  param_dao = ParameterDao(db)
  category_dao = CategoryDao(db)
  impact_method_dao = ImpactMethodDao(db)
  product_system_dao = ProductSystemDao(db)
  cache = MatrixCache.createLazy(db)
  impact_category_dao = ImpactCategoryDao(db)
  DQS_dao = DQSystemDao(db)

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

  # ****************************************************************************
  # Impact Method refId
  method_id = 'b0f6a3ba-a0be-3bfe-ae43-4e23c241e4b6'
  # get method instance
  method = impact_method_dao.getForRefId(method_id)
  # Data Quality System
  DQS_id = "e7ac7cf6-5457-453e-99f9-d889826fffe8"
  DQS_Obj = DQS_dao.getForRefId(DQS_id)
  # ***********************************************************************************
  # data files from "scripts_openlca_20210714a.py"
  h2fcbus = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "h2fcbus.txt"))
  #
  Aberdeen_station_grid = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Aberdeen_station_grid.txt"))
  Antwerp_station_grid = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Antwerp_station_grid.txt"))
  Groningen_station_grid = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Groningen_station_grid.txt"))
  Sanremo_station_grid = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Sanremo_station_grid.txt"))
  #
  Aberdeen_station_re = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Aberdeen_station_re.txt"))
  Antwerp_station_re = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Antwerp_station_re.txt"))
  Groningen_station_re = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Groningen_station_re.txt"))
  Sanremo_station_re = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "Sanremo_station_re.txt"))
  #
  market_electricity_grid = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "market_electricity_grid.txt"))
  market_electricity_re = util.getDictionary("{0}{1}".format(util.Config_CLASS.json_path, "market_electricity_re.txt"))

  log_text("Block execution complete")


  processList = {
    "Hydrogen Station, Aberdeen - Grid" : Aberdeen_station_grid,
    "Hydrogen Station, Groningen - Grid" : Groningen_station_grid,
    "Hydrogen Station, Sanremo - Grid" : Sanremo_station_grid,
    "Hydrogen Station, Antwerp - Grid" : Antwerp_station_grid,
    "Hydrogen Station, Aberdeen - Re" : Aberdeen_station_re,
    "Hydrogen Station, Groningen - Re" : Groningen_station_re,
    "Hydrogen Station, Sanremo - Re" : Sanremo_station_re,
    "Hydrogen Station, Antwerp - Re" : Antwerp_station_re
    #"hydrogen fuel cell bus, end-of-life (recycling scenario) (NO HRS)" : h2fcbus
    #"market group for electricity, low voltage | electricity, low voltage | APOS,U" : market_electricity_grid,
    #"market for electricity, low voltage, label-certified | electricity, low voltage, label-certified | APOS,U" : market_electricity_re
  }

  tmp_impactCategoryResultFileList = util.LoadTextFilebyRow("{0}{1}".format(util.Config_CLASS.json_path, "impactCategoryResultFileList.txt"))
  impactCategoryResultFileList = dict(zip([_[0] for _ in tmp_impactCategoryResultFileList],
                                   [_[1] for _ in tmp_impactCategoryResultFileList]))

  tmp_customLevelProcessList = util.LoadTextFilebyRow("{0}{1}".format(util.Config_CLASS.json_path, "customLevelProcessList.txt"))
  customLevelProcessList = dict(zip([_[0] for _ in tmp_customLevelProcessList],
                                     [int(_[1]) for _ in tmp_customLevelProcessList]))

  # Main loop: loop through the process list
  for product_system_name in processList:
    # get process refId
    processRefId = processList[product_system_name]["processRefId"]
    # get process object instance
    processRefObj = util.get_process(process_dao, processRefId)
    log_text("processRefObj name = '{0}'".format(processRefObj.name))
    # ***********************************************************************************
    appCache = Cache.getAppCache()
    #
    key = "{0}_results".format(product_system_name)
    key_setup = "{0}_setup".format(product_system_name)
    key_DQS = "{0}_DQS".format(product_system_name)
    key_Sim = "{0}_Sim".format(product_system_name)
    #
    result = appCache.remove(key)
    setup = appCache.remove(key_setup)
    DQRes = appCache.remove(key_DQS)
    #
    # check returned value
    if result is None:
      log_text("Cache Empty")
      ProductSystemObj = util.create_product_system(db, processRefObj, product_system_name, processList[product_system_name]["amount"])
      util.auto_link_system(db, ProductSystemObj)
      # Redef Paramters
      # ***********************************************************************************
      if not processList[product_system_name]["paramRedefList"]:
        log_text("paramRedefList is empty")
      else:
        log_text("Redefine a process parameter")
        # process Context list
        processContextList = processList[product_system_name]["paramRedefList"]
        # loop through process refid list
        for processContextRefId in processContextList:
          # get object instance
          processContextObj = util.get_process(process_dao, processContextRefId)
          log_text("processContextObj name = '{0}'".format(processContextObj.name))
          # get param list
          paramRedefList = processList[product_system_name]["paramRedefList"][processContextRefId]
          # loop through the parameters list
          for pm_name in paramRedefList:
            # ***********************************************************************************
            param_redef_attribute_DICT = {}
            param_redef_attribute_DICT[util.ParameterRedef_CLASS.contextId] = processContextObj.id
            param_redef_attribute_DICT[util.ParameterRedef_CLASS.contextType] = util.ModelType_CLASS.ModelType_DICT[util.ModelType_CLASS.ModelType_PROCESS]
            pmRedef = util.add_parameter_redef(pm_name, processList[product_system_name]["paramRedefList"][processContextRefId][pm_name], param_redef_attribute_DICT)
            # ***********************************************************************************
            log_text("parameterRedef name: '{0}'".format(pmRedef.name))
            # adds parameter redefinition to the selected product system
            ProductSystemObj.parameterRedefs.add(pmRedef)
            # ***********************************************************************************
        # ***********************************************************************************
        parameterList = ProductSystemObj.parameterRedefs
        log_text("parameterRedefs len: {0}".format(len(parameterList)))
        # ***********************************************************************************
      # ***********************************************************************
      # update product system
      # ***********************************************************************
      product_system_dao.update(ProductSystemObj)
      # ***********************************************************************************
      log_text("Product System refId = '{0}'".format(ProductSystemObj.refId))
      setup = CalculationSetup(CalculationType.CONTRIBUTION_ANALYSIS, ProductSystemObj)
      log_text("setup OK")
      setup.impactMethod = Descriptors.toDescriptor(method)
      log_text("setup.impactMethod OK")
      setup.parameterRedefs.addAll(ProductSystemObj.parameterRedefs)
      log_text("setup.parameterRedefs.addAll OK")
      setup.allocationMethod = AllocationMethod.PHYSICAL
      log_text("setup.allocationMethod OK")
      calculator = SystemCalculator(cache, App.getSolver())
      log_text("calculator OK")
      DQSetup = util.get_DQS(ProductSystemObj, DQS_Obj)
      log_text("DQSetup OK")
      ContributionResult = calculator.calculateContributions(setup)
      log_text("calculateContributions OK")
      DQRes = DQResult.calculate(db, ContributionResult, DQSetup)
      log_text("DQRes OK")
      result = calculator.calculateFull(setup)
      log_text("calculateFull OK")
      log_text("Add result data to Cache")
      appCache.put(key, result)
      appCache.put(key_setup, setup)
      appCache.put(key_DQS, DQRes)
      log_text("open the result")
      # open the result
      inp = ResultEditorInput.create(setup, result).with(DQRes)
      Editors.open(inp, AnalyzeEditor.ID)
      #
      if ElaboratioFlags.Enable_getTotalResult:
        log_text("Save data to json file")
        util.getTotalResult(result, processList[product_system_name]["jsonFileName"])
      else:
        log_text("No save data to json file")
      #
    else:
      log_text("Cache OK")
      appCache.put(key, result)
      appCache.put(key_setup, setup)
      # workaround to recalculate the DQS assessment
      if DQRes is None:
        calculator = SystemCalculator(cache, App.getSolver())
        log_text("calculator OK")
        ContributionResult = calculator.calculateContributions(setup)
        log_text("calculateContributions OK")
        # get product system reference
        ProductSystemObj = product_system_dao.getForName(product_system_name)[0]
        log_text("get product system reference OK")
        DQSetup = util.get_DQS(ProductSystemObj, DQS_Obj)
        log_text("DQSetup OK")
        DQRes = DQResult.calculate(db, ContributionResult, DQSetup)
        log_text("DQRes OK")
      # ***************************************************************************
      appCache.put(key_DQS, DQRes)
      # ***********************************************************************
      # open the result
      # olca-app/olca-app/src/org/openlca/app/results/ResultEditor.java
      # https://github.com/GreenDelta/olca-app/blob/2c550df741a13592027ed6e1b7653cf7093e6e69/olca-app/src/org/openlca/app/results/ResultEditor.java
      #
      inp = ResultEditorInput.create(setup, result).with(DQRes)
      Editors.open(inp, AnalyzeEditor.ID)
      #
      # ***********************************************************************
      # Perform Monte Carlo Simulation
      # ***********************************************************************
      if ElaboratioFlags.Enable_MonteCarloSimulation:
        # get product system reference
        ProductSystemObj = product_system_dao.getForName(product_system_name)[0]
        log_text("Product System refId = '{0}'".format(ProductSystemObj.refId))
        setupSimulation = CalculationSetup(CalculationType.MONTE_CARLO_SIMULATION, ProductSystemObj)
        log_text("setupSimulation OK")
        setupSimulation.impactMethod = Descriptors.toDescriptor(method)
        log_text("setupSimulation.impactMethod OK")
        setupSimulation.parameterRedefs.addAll(ProductSystemObj.parameterRedefs)
        log_text("setupSimulation.parameterRedefs.addAll OK")
        setupSimulation.allocationMethod = AllocationMethod.PHYSICAL
        log_text("setupSimulation.allocationMethod OK")
        SimCalculator = Simulator.create(setupSimulation, cache, App.getSolver())
        log_text("SimCalculator OK")
        # ***********************************************************************
        # Open file to store results data
        SimulationImpactFilePath = "{0}{1}".format(util.Config_CLASS.json_path, "{0}_SimulationImpact.txt".format(processList[product_system_name]["ImpactFilePrefix"]))
        fileObj = open(SimulationImpactFilePath, mode = 'w')
        fileObj.write('\t'.join(["TimeStamp", "run", "Climate change"]) + "\n")
        #appCache.put(key_Sim, SimResult)
        # ***********************************************************************
        # Generates random numbers and calculates the product system. Returns the
      	# simulation result if the calculation in this run finished without errors,
      	# otherwise `null` is returned (e.g. when the resulting matrix was
      	# singular)
        # ***********************************************************************
        for i in range(3):
          SimResult = SimCalculator.nextRun()
          log_text("SimCalculator.getResult OK")
          SelectedImpactCategory = getImpactCategoryObj('Climate change', method.impactCategories)
          allImpactsList = SimResult.getTotalImpactResult(Descriptors.toDescriptor(SelectedImpactCategory))
          timeStampStr = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
          log_text("run no. [{0}] {1}: allImpactsList: '{2}' ".format(i, timeStampStr, allImpactsList))
          fileObj.write('\t'.join([timeStampStr, str(i), str(allImpactsList)]) + "\n")
        fileObj.close()
        #
      # ***********************************************************************
      # Save Impact Analysis Results
      # ***********************************************************************
      if ElaboratioFlags.Enable_SaveImpactAnalysis:
        # iterates over each impact category
        for impactCategoryResult in result.getTotalImpactResults():
          log_text("impactCategoryResult.impactCategory = '{0}'".format(impactCategoryResult.impactCategory.name.encode('utf-8')))
          # select only "Climante change" impact category
          #if impactCategoryResult.impactCategory.name == 'Climate change':
          # get impact category object reference
          SelectedImpactCategory = getImpactCategoryObj(impactCategoryResult.impactCategory.name, method.impactCategories)
          log_text("Selected Impact Category: '{0}' ".format(SelectedImpactCategory.name))
          # open file to write data
          ImpactFilePath = "{0}{1}".format(util.Config_CLASS.json_path, "{0}_ImpactAnalysis_{1}".format(processList[product_system_name]["ImpactFilePrefix"], impactCategoryResultFileList[impactCategoryResult.impactCategory.name]))
          fileObj = open(ImpactFilePath, mode = 'w')
          # get root element with total amount for that impact category
          treeObj = result.getTree(impactCategoryResult.impactCategory)
          rootElem = treeObj.root
          log_text("rootElem name = '{0}'".format(rootElem.provider.process.name.encode('utf-8')))
          log_text("rootElem amount = '{0}'".format(rootElem.result))
          total_amount = rootElem.result
          # iterate over each process contribution for the impact category
          for processContribution in result.getProcessContributions(impactCategoryResult.impactCategory).contributions:
            # select only value > 1%
            if (processContribution.amount / total_amount) > 0.01:
              log_text("processContribution.item.name = '{0}'".format(processContribution.item.name.encode('utf-8')))
              log_text("processContribution.amount = {0}".format(processContribution.amount))
              fileObj.write('\t'.join([impactCategoryResult.impactCategory.name.encode('utf-8'), processContribution.item.name.encode('utf-8'), str(processContribution.amount).replace('.',',')]) + "\n")
              # create list with non-zero flow contribution to current process in the selected impact category
              flowResList = [_ for _ in result.getFlowContributions(impactCategoryResult.impactCategory) if result.getDirectFlowResult(processContribution.item, _.flow) > 0.0]
              # iterate over each non-zero flow contribution for the selected impact category
              for flowRes in flowResList:
                flowContributionToProcessInImpactCategory = result.getDirectFlowResult(processContribution.item, flowRes.flow)
                log_text("flowRes.flow.name: '{0}' ".format(flowRes.flow.name))
                # get associated impact factor
                ImpactFactorValue = getImpactFactorCategory(flowRes.flow, SelectedImpactCategory)
                # check if impact factor is gretaer than 0.0
                if not ImpactFactorValue:
                  ImpactFactorValueChecked = 0.0
                else:
                  ImpactFactorValueChecked = ImpactFactorValue[0]
                  log_text("ImpactFactorValue: {0} ".format(ImpactFactorValueChecked))
                  log_text("processContribution.item.refId: '{0}' ".format(processContribution.item.refId))
                  # get Data Qaulity System value
                  processObj = process_dao.getForRefId(processContribution.item.refId)
                  DQSentry = getDQSEntry(flowRes.flow, processObj)[0]
                  if DQSentry is None:
                    DQSentry = "(5;5;5;5;5)"
                    # select exchange
                    ExchangeObj = util.get_exchange(processObj, flowRes.flow.refId)
                    # set DQS entry to the selected exchange
                    ExchangeObj.dqEntry = DQSentry
                    # update process
                    process_dao.update(processObj)
                  log_text("DQSentry: {0} ".format(DQSentry))
                  # save data to file
                  fileObj.write('\t'.join([impactCategoryResult.impactCategory.name.encode('utf-8'), processContribution.item.name.encode('utf-8'), flowRes.flow.name.encode('utf-8'), flowRes.flow.refId , str(flowContributionToProcessInImpactCategory).replace('.',','), str(ImpactFactorValueChecked).replace('.',','), DQSentry]) + "\n")
          # close file
          fileObj.close()
      # get product system reference
      ProductSystemObj = product_system_dao.getForName(product_system_name)[0]
      # Check Product System
      if not ProductSystemObj:
        log_text("Product System to be created")
        ProductSystemObj = util.create_product_system(db, processRefObj, product_system_name, processList[product_system_name]["amount"])
        util.auto_link_system(db, ProductSystemObj)
      else:
        log_text("Product System already present")
        #system = ProductSystemObj
      log_text("Product System refId = '{0}'".format(ProductSystemObj.refId))
    # ***********************************************************************
    # Save ImpactCategoryResult
    # ***********************************************************************
    if ElaboratioFlags.Enable_SaveImpactCategoryResult:
      # loop through the impact Category Results
      for impactCategoryResult in result.getTotalImpactResults():
        #impactCategoryResult.impactCategory
        log_text("impactCategoryResult.impactCategory = '{0}'".format(impactCategoryResult.impactCategory.name))
        fileName = "{0}{1}".format(processList[product_system_name]["ImpactFilePrefix"], impactCategoryResultFileList[impactCategoryResult.impactCategory.name])
        ImpactFilePath = "{0}{1}".format(util.Config_CLASS.json_path, fileName)
        fileObj = open(ImpactFilePath, mode = 'wb')
        treeObj = result.getTree(impactCategoryResult.impactCategory)
        rootElem = treeObj.root
        log_text("rootElem name = '{0}'".format(rootElem.provider.process.name.encode('utf-8')))
        log_text("rootElem amount = '{0}'".format(rootElem.result))
        lst = [rootElem.provider.process.name.encode('utf-8'), str(rootElem.result).encode('utf-8').replace('.',','), str(1.0).encode('utf-8').replace('.',',')]
        fileObj.write('\t'.join(lst) + "\n")
        util.getUpstreamTreeData3(fileObj, result, impactCategoryResult.impactCategory, rootElem, 5, customLevelProcessList, rootElem.result)
    # ***********************************************************************
  # ***********************************************************
  # Refreshes the application to update the navigation treeview
  App.runInUI('Refreshing', refresh)
