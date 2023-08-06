import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
    id: deviceSelection

//  Whether selected or not
    property bool checked: false
//  Whether clicked on item
    property alias clickedArea: clickedArea

    textColumn {
        anchors.right: checkItem.left
        anchors.rightMargin: 16
    }
    smallImage: true

    Item {
        id: checkItem

        width: 24
        height: 24

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        DS3.Icon {
            source: "qrc:/resources/images/Athena/common_icons/Check-M.svg"
            visible: deviceSelection.checked
            opacity: enabled ? 1 : 0.3
        }
    }

    DS3.MouseArea {
        id: clickedArea
    }
}
