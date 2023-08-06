import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
    id: deviceSelectionMulti

//  Whether selected or not
    property bool checked: false
//  Whether clicked on item
    property alias clickedArea: clickedArea

    textColumn {
        anchors.right: selectMulti.left
        anchors.rightMargin: 16
    }
    smallImage: true

    DS3.SelectMulti {
        id: selectMulti

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        checked: deviceSelectionMulti.checked
        opacity: enabled ? 1 : 0.3
    }

    DS3.MouseArea {
        id: clickedArea
    }
}
