from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self, headers):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.headers = headers
        self.setColumnCount(len(headers))
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def _clear(self):
        self.setRowCount(0)
        self.clear()

    def _exsitsInColumn(self, fixed_col, val):
        rowCount = self.rowCount()
        itemRow = -1
        for row in range(rowCount):
            itemExists = self._exsits(row, fixed_col, val)
            if itemExists:
                itemRow = row
                break
      
        return itemRow

    def _exsits(self, row, col, val):
        ex = False
        item = self.item(row, col)
        if item != None:
            if isinstance(val, int):
                if int(item.text()) == val:
                    ex = True
            elif item.text() == val:
                ex = True
        return ex
                
    def _addRow(self, new_row):
        if len(new_row) == len(self.headers):
            col_index = 0
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            #self.setRowCount(rowCount + 1)
            for val in new_row:
                item = QTableWidgetItem(str(val))
                item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                self.setItem(rowCount, col_index, item)
                col_index += 1

    def _get_all_rows(self):
        rowCount = self.rowCount()
        rows = []
        for row in range(rowCount):
            row_data = tuple(self._getRow(row))
            rows.append(row_data)
        return rows

    def _get_col_values(self, col):
        rowCount = self.rowCount()
        values = []
        for row in range(rowCount):
            val = self._get_value(row, col)
            values.append({'row': row, 'value': val})
        return values

    def _get_value(self, row, col):
        return self.item(row, col).text()
        
    def _getRow(self, row):
        data = []
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item != None:
                data.append(item.text())
        return data

    def _checkRowChange(self, row, columns):
        for col in columns:
            item = self.item(row, col['index'])
            if item.text() != col['value']:
                item.setText(col['value'])

    def _setValue(self, row, col, value):
        item = self.item(row, col)
        item.setText(value)

    def _getByValue(self, col, value):
        rowCount = self.rowCount()
        rowToGet = self._exsitsInColumn(col, value)
        return self._getRow(rowToGet)

    def _removeRow(self, rowNum):
        if rowNum >= 0:
            self.removeRow(rowNum)

    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))
'''
name_item = QTableWidgetItem(comp[0])
dur_item = QTableWidgetItem(str(round(float(comp[1]))))
dur_item.setTextAlignment(Qt.AlignCenter)
fps_item = QTableWidgetItem(str(round(1 / float(comp[2]))))
fps_item.setTextAlignment(Qt.AlignCenter)
tableWidget.setItem(row, 0,name_item)
tableWidget.setItem(row, 1, dur_item)
tableWidget.setItem(row, 2, fps_item)
'''