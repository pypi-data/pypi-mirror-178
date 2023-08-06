import QtQuick 2.12
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterCompany {
//  Component is selected
    property alias selected: mark.visible
//  Callback on selection
    property var onSelectedCallback: () => selected = !selected

    companyName.anchors.rightMargin: 56
    color: ui.ds3.bg.high

    DS3.Icon {
        id: mark

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        source: "qrc:/resources/images/Athena/common_icons/Check-M.svg"
    }

    DS3.MouseArea {
        onClicked: onSelectedCallback()
    }
}
