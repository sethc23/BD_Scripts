#!/usr/bin/python
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.api import users
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.docs.service
import gdata.auth
import gdata.docs
import gdata.docs.service
import gdata.service
import gdata.spreadsheet
import gdata.spreadsheet.service
import gdata.spreadsheet.text_db
import gdata.alt.appengine
import atom
import atom.service
import getopt
import sys
import string
import atom.http

class text_db_class:
    def __init__(self):
        self.dbClient = gdata.spreadsheet.text_db.DatabaseClient()
        try:
        	gdata.alt.appengine.run_on_appengine(self.dbClient, store_tokens=False, single_user_mode=True)
        	gdata.alt.appengine.run_on_appengine(self.dbClient._GetDocsClient(), store_tokens=False, single_user_mode=True)
        	gdata.alt.appengine.run_on_appengine(self.dbClient._GetSpreadsheetsClient(), store_tokens=False, single_user_mode=True)
        	self.dbClient.SetCredentials('seth.t.chase@gmail.com', 'F*rrari1')
        except:
            self.curr_key = 'None'
    def _MakeNewWorkbook(self, workbook):
        self.dbClient.CreateDatabase(workbook)
        try:
		    gdata.alt.appengine.run_on_appengine(self.dbClient)
        except:
            self.curr_key = 'None'

class gdata_service_class:
    def __init__(self):
        self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gdata.alt.appengine.run_on_appengine(self.gd_client, store_tokens=False, single_user_mode=True)
        self.gd_client.email = 'seth.t.chase@gmail.com'
        self.gd_client.password = 'F*rrari1'
        self.gd_client.service = 'wise'
        try:
            self.gd_client.ProgrammaticLogin()
            gdata.alt.appengine.run_on_appengine(self.gd_client, store_tokens=False, single_user_mode=True)
            self.curr_key = ''
            self.curr_wksht_id = ''
        except:
            self.curr_key = 'None'
    def _CheckForWorkbook(self, workbook):
        if self.curr_key == 'None':
            return 'run same again'
        try:
            feed = self.gd_client.GetSpreadsheetsFeed()
        except:
            return 'error on server'
        for i, entry in enumerate(feed.entry):
            if entry.title.text.find(workbook) != -1:
                id_parts = feed.entry[i].id.text.split('/')
                self.curr_key = id_parts[len(id_parts) - 1]
                return 'success'
            return "failure"
    def _GetAllWorksheets(self):
        if self.curr_key == 'None':
            return 'run same again'
        worksheets = []
        feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
        for i, entry in enumerate(feed.entry):
            worksheets.append(entry.title.text)
        return worksheets
    def _CheckForWorksheet(self, worksheet):
        if self.curr_key == 'None':
            return 'run same again'
        try:
            feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
        except:
            return 'error on server'
        for i, entry in enumerate(feed.entry):
            if entry.title.text.find(worksheet) != -1:
                id_parts = feed.entry[i].id.text.split('/')
                self.curr_wksht_id = id_parts[len(id_parts) - 1]
                return "success"
        return "failure"
    def _MakeNewWorksheets(self, WSlist, row_count, col_count):
        if self.curr_key == 'None':
            return 'run same again'
        if type(WSlist) == str:
            self.gd_client.AddWorksheet(WSlist, row_count, col_count, self.curr_key)
        else:
            for i in range(0, len(WSlist)):
                self.gd_client.AddWorksheet(WSlist[i], row_count, col_count, self.curr_key)
    def _CellsGetAction(self):
        if self.curr_key == 'None':
            return 'run same again'
        # Get the feed of cells
        feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
        self._PrintFeed(feed)
    def _CellsGetColumn(self, col_let):
        if self.curr_key == 'None':
            return 'run same again'
        col_data = [], []
        feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
        for i, entry in enumerate(feed.entry):
            pt = entry.title.text.find(col_let)
            pt1 = entry.title.text[pt + 1]
            if pt != -1:
                try:
                    type(eval(pt1))
                    if type(eval(pt1)) == int:
                        col_data[0].append(entry.title.text)
                        col_data[1].append(entry.content.text)
                except NameError:
                    pass
        return col_data
    def _CellsGetRow(self, row_num):
        if self.curr_key == 'None':
            return 'run same again'
        row_data = []
        feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
        for i, entry in enumerate(feed.entry):
            if entry.title.text.find(row_num) != -1:
                if entry.title.text.find(row_num) == (len(entry.title.text) - 1):
                    row_data.append('%s::%s' % (entry.title.text, entry.content.text))
        return row_data
    def _GetCellVersions(self, cellRefs):
        if self.curr_key == 'None':
            return 'run same again'
        cellRefKeys = []
        for i in range(0, len(cellRefs)):
            try:
                feed = self.gd_client.GetCellsFeed(key=self.curr_key, wksht_id=self.curr_wksht_id, cell=cellRefs[i])
                linkRef = feed.link[1].href
                cellRefKeys.append(linkRef[linkRef.rfind('/') + 1:])
            except:
                return 'run same again'
        return cellRefKeys
    def _SendBatchRequest(self, cellRefs, cellValues, batchStr):
        if self.curr_key == 'None':
            return 'run same again'
        if str(batchStr) == '':
            run = batch_service()
            if type(cellRefs) == list and type(cellValues) == list:
                batchStr = run._addMultiEntry(cellRefs, cellValues, batchStr)
            else:
                batchStr = run._addEntry(cellRefs, cellValues, batchStr)
        batchStr = batchStr.replace('SPREADSHEETKEY', str(self.curr_key))
        batchStr = batchStr.replace('WORKSHEETKEY', str(self.curr_wksht_id))
        batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeedFromString(batchStr)
        # for single or multi request    
        postLink = 'http://spreadsheets.google.com/feeds/cells/' + str(self.curr_key) + '/' + str(self.curr_wksht_id) + '/private/full/batch'
        updated = self.gd_client.ExecuteBatch(batchRequest, postLink, spreadsheet_key=self.curr_key, worksheet_id=self.curr_wksht_id)
        return 'success'

class batch_service:
    def __init__(self):
        pass
    def _addMultiEntry(self, cellRefs, cellValues, cellVerKeys, batchStr):
        if batchStr == None:
            batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
        else:
            batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeedFromString(batchStr)
        if type(cellRefs) == list and type(cellValues) == list:
            if len(cellRefs) == len(cellValues):
                for i in range(0, len(cellRefs)):
                    cellRow = cellRefs[i][cellRefs[i].find('R') + 1:cellRefs[i].find('C')]
                    cellCol = cellRefs[i][cellRefs[i].find('C') + 1:]
                    if type(cellValues[i]) == str:
                        cellInput = 'inputValue="' + cellValues[i] + '"'
                    else:
                        cellInput = 'numericValue="' + str(cellValues[i]) + '"'
                    test = str('<feed xmlns="http://www.w3.org/2005/Atom"' + 
                    ' xmlns:batch="http://schemas.google.com/gdata/batch"' + 
                    ' xmlns:gs="http://schemas.google.com/spreadsheets/2006"> ' + 
                    '<id>http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full</id>' + 
                    '<entry>' + 
                    '<batch:id>A1</batch:id>' + 
                    '<batch:operation type="update" />' + 
                    '<id>http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full/' + str(cellRefs[i]) + '</id>' + 
                    '<link rel="edit" type="application/atom+xml"' + 
                     ' href="http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full/' + str(cellRefs[i]) + '/' + str(cellVerKeys[i]) + '" />' + 
                    '<gs:cell row="' + str(cellRow) + '" col="' + str(cellCol) + '" ' + cellInput + ' />' + 
                    '</entry>' + 
                    '</feed>')
                    newCell = gdata.spreadsheet.SpreadsheetsCellsFeedFromString(test)
                    batchRequest.AddUpdate(newCell.entry[0])
            else:
                return 'error - cell references not match cell values'
        return batchRequest.__str__()
            
    def _addEntry(self, cellRef, cellValue, batchStr):
        if batchStr == None:
            batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
        else:
            batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeedFromString(batchStr)         
#        cell = self.gd_client.GetCellsFeed(key=self.curr_key, wksht_id=self.curr_wksht_id, cell=cellRef)
#        linkRef = cell.link[1].href
#        cellRefKey = linkRef[linkRef.rfind('/')+1:]
        cellRow = cellRef[cellRef.find('R') + 1:cellRef.find('C')]
        cellCol = cellRef[cellRef.find('C') + 1:]
        if type(cellValue) == str:
            cellInput = 'inputValue="' + cellValue + '"'
        else:
            cellInput = 'numericValue="' + str(cellValue) + '"'
        test = str('<feed xmlns="http://www.w3.org/2005/Atom"' + 
        ' xmlns:batch="http://schemas.google.com/gdata/batch"' + 
        ' xmlns:gs="http://schemas.google.com/spreadsheets/2006"> ' + 
        '<id>http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full</id>' + 
        '<entry>' + 
        '<batch:id>A1</batch:id>' + 
        '<batch:operation type="update" />' + 
        '<id>http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full/' + str(cellRef) + '</id>' + 
        '<link rel="edit" type="application/atom+xml"' + 
         ' href="http://spreadsheets.google.com/feeds/cells/' + 'SPREADSHEETKEY' + '/' + 'WORKSHEETKEY' + '/private/full/' + str(cellRef) + '/' + str(cellRefKey) + '" />' + 
        '<gs:cell row="' + str(cellRow) + '" col="' + str(cellCol) + '" ' + cellInput + ' />' + 
        '</entry>' + 
        '</feed>')
        newCell = gdata.spreadsheet.SpreadsheetsCellsFeedFromString(test)
        batchRequest.AddUpdate(newCell.entry[0])
        return batchRequest.__str__()

class gdata_spreadsheet_class:
    def __init__(self):
        self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gdata.alt.appengine.run_on_appengine(self.gd_client, store_tokens=False, single_user_mode=True)
        self.gd_client.email = 'seth.t.chase@gmail.com'
        self.gd_client.password = 'F*rrari1'
        self.gd_client.service = 'wise'
        try:
            self.gd_client.ProgrammaticLogin()
            gdata.alt.appengine.run_on_appengine(self.gd_client, store_tokens=False, single_user_mode=True)
            self.curr_key = ''
            self.curr_wksht_id = ''
        except:
            self.curr_key = 'None'
    def _CheckForWorkbook(self, workbook):
        if self.curr_key == 'None':
            return 'run same again'
        feed = self.gd_client.GetSpreadsheetsFeed()
        for i, entry in enumerate(feed.entry):
            if entry.title.text.find(workbook) != -1:
                id_parts = feed.entry[i].id.text.split('/')
                self.curr_key = id_parts[len(id_parts) - 1]
                return 'success'
            return "failure"
    def _SendBatchWorksheet(self, workbook, worksheets):
        if self.curr_key == 'None':
            return 'run same again'
        getWorkbookKey = gdata_spreadsheet_class._CheckForWorkbook(self, workbook)
        if getWorkbookKey == 'failure':
          return 'error - gdata_spreadsheet_class - cannot locate workbook'
        batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
        worksheet = self.gd_client.GetWorksheetsFeed(self.curr_key)
        return worksheet
        title = worksheets
        test = str('<feed xmlns="http://www.w3.org/2005/Atom"' + 
                   ' xmlns:batch="http://schemas.google.com/gdata/batch"' + 
                   ' xmlns:gs="http://schemas.google.com/spreadsheets/2006"> ' + 
                   '<id>http://spreadsheets.google.com/feeds/worksheets/' + str(self.curr_key) + '/private/full</id>' + 
                   '<entry>' + 
                   '<batch:id>A1</batch:id>' + 
                   '<batch:operation type="insert" />' + 
                   '<id>http://spreadsheets.google.com/feeds/worksheets/' + str(self.curr_key) + '/private/full</id>' + 
                   '<title>' + str(title) + '</title>' + 
                   "<link rel='http://schemas.google.com/g/2005#post' type='application/atom+xml' " + 
                   "href='http://spreadsheets.google.com/feeds/worksheets/" + str(self.curr_key) + "/private/full' />" + 
                   '<gs:rowCount>50</gs:rowCount>' + 
                   '<gs:colCount>10</gs:colCount>' + 
                   '</entry>' + 
                   '</feed>')
        newWKSH = gdata.spreadsheet.SpreadsheetsWorksheetsFeedFromString(test)
        batchRequest.AddInsert(newWKSH.entry[0])
        postLink = 'http://spreadsheets.google.com/feeds/worksheets/' + str(self.curr_key) + '/private/full/batch'
        updated = self.gd_client.ExecuteBatch(batchRequest, postLink, spreadsheet_key=self.curr_key)
        return 'success'

def main(self, process, variables):
  if str(process) == 'checkForWorkbook':
      workbook = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      return check
  if str(process) == 'makeWorkbook':
      workbook = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'failure':
          run2 = text_db_class()
          check = run2._MakeNewWorkbook(workbook)
          if check == 'run same again':
              return 'run same again'
      elif check == 'run same again':
          return 'run same again'
  elif str(process) == 'getWorksheets':
      workbook = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          allSheets = run._GetAllWorksheets()
          return allSheets
      else:
          return "error - gdata_spreadsheet - couldn't get workbook"
  elif str(process) == 'makeWorksheet':
      workbook, worksheets = variables
      WSlist, row_count, col_count = worksheets
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          makeSheet = run._MakeNewWorksheets(WSlist, row_count, col_count)
          return makeSheet
      else:
          return "error - gdata_spreadsheet - couldn't get workbook"
  elif str(process) == 'getRow':
      workbook, worksheet, row_num = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          Go2 = run._CheckForWorksheet(worksheet)
          if Go2 == 'error on server' or Go2 == 'run same again':
              return 'run same again'
          elif Go2 == 'success':
              headerRow = run._CellsGetRow(row_num)
              return headerRow
          else:
              return 'error: ' + str(process) + ' checking for ' + str(worksheet) + ' in ' + str(workbook)
      else:
          return 'error: ' + str(process) + ' checking in ' + str(workbook)
  elif str(process) == 'getCol':
      workbook, worksheet, head_col = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          Go2 = run._CheckForWorksheet(worksheet)
          if Go2 == 'error on server' or Go2 == 'run same again':
              return 'run same again'
          elif Go2 == 'success':
              headerCol = run._CellsGetColumn(head_col)
              return headerCol
          else:
              return 'error: ' + str(process) + ' checking for ' + str(worksheet) + ' in ' + str(workbook)
      else:
          return 'error: ' + str(process) + ' checking in ' + str(workbook)
  elif str(process) == 'addWKSHvalues':
      if len(variables) == 4:
          workbook, worksheet, cellRefs, cellValues = variables
          batchStr = None
      elif len(variables) == 5:
          workbook, worksheet, cellRefs, cellValues, batchStr = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          Go2 = run._CheckForWorksheet(worksheet)
          if Go2 == 'error on server' or Go2 == 'run same again':
              return 'run same again'
          elif Go2 == 'success':
              updateCells = run._SendBatchRequest(cellRefs, cellValues, batchStr)
              return updateCells
          else:
              return 'error: ' + str(process) + ' checking for ' + str(worksheet) + ' in ' + str(workbook)
      else:
          return 'error: ' + str(process) + ' checking in ' + str(workbook)
  elif str(process) == 'getCellVersions':
      workbook, worksheet, cellRefs, cellValues = variables
      run = gdata_service_class()
      check = run._CheckForWorkbook(workbook)
      if check == 'error on server' or check == 'run same again':
          return 'run same again'
      if check == 'success':
          Go2 = run._CheckForWorksheet(worksheet)
          if Go2 == 'error on server' or Go2 == 'run same again':
              return 'run same again'
          elif Go2 == 'success':
              cellVerKeys = run._GetCellVersions(cellRefs)
              if type(cellVerKeys) == list:
                  return cellVerKeys
              else:
                  return 'run same again'
          else:
              return 'error: ' + str(process) + ' checking for ' + str(worksheet) + ' in ' + str(workbook)
      else:
          return 'error: ' + str(process) + ' checking in ' + str(workbook)
  elif str(process) == 'makebatchStr':
      workbook, worksheet, cellRefs, cellValues, cellVerKeys, batchStr = variables
      run = batch_service()
      batchStr = run._addMultiEntry(cellRefs, cellValues, cellVerKeys, batchStr)
      return batchStr
    

