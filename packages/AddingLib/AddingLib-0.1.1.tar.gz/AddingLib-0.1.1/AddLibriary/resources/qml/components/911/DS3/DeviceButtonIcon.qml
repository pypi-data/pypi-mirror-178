import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
//  Settings type of operator
    property var operator: DeviceRegular.OperatorType.ButtonIcon
//  buttonMini source
    property var buttonIconSource: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
    property var badgeCounter
//  On back settings clicked
    signal rightControlClicked

    smallImage: true
    hasOnlineTextMessage: true

    DS3.BadgeAttention {
        id: badge

        anchors {
            left: parent.left
            top: parent.top
            topMargin: 12
        }

        text: badgeCounter || 0
        visible: !!text && text > 0
        opacity: enabled ? 1 : 0.3
    }

    DS3.ButtonIcon {
        id: buttonIcon

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: operator == DeviceRegular.OperatorType.ButtonIcon
        source: buttonIconSource
        opacity: enabled ? 1 : 0.3

        onClicked: rightControlClicked()
    }

    DS3.MouseArea {
        width: buttonIcon.width + 32
        height: parent.height

        anchors {
            fill: undefined
            right: parent.right
        }

        onClicked: rightControlClicked()
    }
}
