import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterCompany {
    id: masterCompany

//  Whether multiple selection or not
    property alias multiSelection: selectMulti.visible
//  Whether selected or not
    property bool checked: false
//  Whether clicked on item
    property var companyChecked: () => {checked = !checked}

    companyName.anchors.right: checkItem.left
    color: ui.ds3.bg.highest

    Item {
        id: checkItem

        width: 24
        height: 24

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        DS3.SelectMulti {
            id: selectMulti

            checked: masterCompany.checked
            visible: false
        }

        DS3.Icon {
            source: "qrc:/resources/images/Athena/common_icons/Check-M.svg"
            visible: masterCompany.checked && !selectMulti.visible
        }
    }

    DS3.MouseArea {
        id: clickedArea

        onClicked: companyChecked()
    }
}
