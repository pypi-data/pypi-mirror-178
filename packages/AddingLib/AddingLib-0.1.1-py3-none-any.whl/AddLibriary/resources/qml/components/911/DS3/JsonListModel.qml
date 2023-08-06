import QtQuick 2.12
import QtQuick.Controls 2.13


ListModel {
    id: jsonListModel

//  Json list with data
    property var data: []

    onDataChanged: {
        jsonListModel.clear()
        data.forEach((obj) => jsonListModel.append(obj))
    }
}
