import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.MasterUser {
    id: masterUser

//  Photo of the user
    property alias image: masterUser.imageSource
//  Right icon visibility
    property alias rightIcon: rightIcon

//  Right icon clicked
    signal rightIconClicked

    color: ui.ds3.bg.highest

    atomTitle{
        anchors {
            right: rightIcon.left
            rightMargin: 16
        }
    }

    DS3.ButtonIcon {
        id: rightIcon

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        visible: false
        source: "qrc:/resources/images/Athena/common_icons/CrossCircle-M.svg"
        color: ui.ds3.figure.attention

        DS3.MouseArea {
            onClicked: rightIconClicked()
        }
    }
}
