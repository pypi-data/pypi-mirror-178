import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
//  buttonMini source
    property var buttonMiniSource
//  If spinner is visible
    property bool hasSpinner: false

//  On back settings clicked
    signal rightControlClicked

    smallImage: true
    hasOnlineTextMessage: true

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: !hasSpinner
        opacity: enabled ? 1 : 0.3
        source: buttonMiniSource || "qrc:/resources/images/Athena/views_icons/Photo-S.svg"

        onClicked: rightControlClicked()
    }

    DS3.Spinner {
        size: DS3.Spinner.ImageSize.M

        anchors.centerIn: buttonMiniControl

        visible: hasSpinner
    }

    DS3.MouseArea {
        width: buttonMiniControl.width + 32
        height: parent.height

        anchors {
            fill: undefined
            right: parent.right
        }

        onClicked: rightControlClicked()
    }
}
