import xlrd

xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

class XLSReader:
    def __init__(self, path):
        print("XLSReader init --- method invoked")
        self.path = path
        self.readXLS = xlrd.open_workbook(path)

    def getCellData(self, sheetname, rowNum, colNum):
        print("XLSReader getCellData --- method invoked")
        sheet = self.readXLS.sheet_by_name(sheetname)
        return sheet.cell_value(rowNum, colNum)

    def getCellDataByColName(self, sheetname, rowNum, colName):
        print("XLSReader getCellDataByColName --- method invoked")
        sheet = self.readXLS.sheet_by_name(sheetname)
        for cNum in range(0, sheet.ncols):
            extractedColName = sheet.cell_value(0, cNum)
            if (extractedColName == colName):
                cellData = sheet.cell_value(rowNum, cNum)
                if (cellData != ''):
                    return cellData
                else:
                    return ''

    def checkEmptyCell(self, sheetname, rowNum, colNum):
        print("XLSReader checkEmptyCell --- method invoked")
        sheet = self.readXLS.sheet_by_name(sheetname)
        cellType = sheet.cell_type(rowNum, colNum)
        if (cellType == xlrd.XL_CELL_EMPTY):
            return True
        else:
            return False

    def rowCount(self, sheetname):
        print("XLSReader rowCount --- method invoked")
        sheet = self.readXLS.sheet_by_name(sheetname)
        return sheet.nrows

    def colCount(self, sheetname):
        print("XLSReader colCount --- method invoked")
        sheet = self.readXLS.sheet_by_name(sheetname)
        return sheet.ncols