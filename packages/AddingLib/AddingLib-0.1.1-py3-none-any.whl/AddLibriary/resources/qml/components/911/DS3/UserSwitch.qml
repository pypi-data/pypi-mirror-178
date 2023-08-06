import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterUser {
    id: masterUser

//  Photo of the user
    property alias image: masterUser.imageSource
//  If this users switch is on
    property alias checked: userSwitch.checked

//  Signal on the even of the switch being switched
    signal switched

    implicitWidth: parent.width

    color: ui.ds3.bg.highest

    atomTitle {
        anchors {
            right: userSwitch.left
            rightMargin: 16
        }
    }

    DS3.Switch {
        id: userSwitch

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        cancelBinding: false

        onToggle: () => switched()
    }
}
