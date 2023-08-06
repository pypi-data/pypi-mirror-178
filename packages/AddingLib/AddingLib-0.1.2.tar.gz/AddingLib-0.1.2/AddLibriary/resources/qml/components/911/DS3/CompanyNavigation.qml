import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterCompany {
    id: masterCompany

//  Right icon clicked
    signal rightIconClicked

    companyName.anchors.right: actionArrow.left

    color: ui.ds3.bg.highest

    DS3.ButtonIcon {
        id: actionArrow

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.svg"
        color: ui.ds3.figure.secondary

        onClicked: onClicked()
    }

    DS3.MouseArea {
        onClicked: rightIconClicked()
    }
}

