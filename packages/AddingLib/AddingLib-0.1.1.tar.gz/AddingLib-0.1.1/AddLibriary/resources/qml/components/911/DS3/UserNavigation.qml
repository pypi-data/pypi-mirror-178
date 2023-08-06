import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterUser {
    id: masterUser

//  Photo of the user
    property alias image: masterUser.imageSource

//  Right icon clicked
    signal rightIconClicked

    color: ui.ds3.bg.highest

    atomTitle {
        anchors {
            right: actionArrow.left
            rightMargin: 16
        }
    }

    DS3.ButtonIcon {
        id: actionArrow

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.svg"
        color: ui.ds3.figure.nonessential
        visible: enabled
    }

    DS3.MouseArea {
        onClicked: rightIconClicked()
    }
}
