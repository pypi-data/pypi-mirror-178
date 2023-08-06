import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceNavigation {
    id: deviceNav

//  Button mini device spread component
    property alias firstSwitchDeviceSpread: firstSwitchDeviceSpread
//  Button mini device spread component
    property alias secondSwitchDeviceSpread: secondSwitchDeviceSpread

    height: Math.max(132, textColumn.height + spreadsColumn.height + 16)

    colorCheck: [secondSwitchDeviceSpread.switchControl]
    textColumn.anchors {
        top: deviceNav.top
        topMargin: 8
        verticalCenter: undefined
    }

    Column {
        id: spreadsColumn

        width: parent.width

        anchors {
            top: textColumn.bottom
            topMargin: 8
            right: parent.right
            rightMargin: 16
            left: parent.left
            leftMargin: 16
        }

        Rectangle {
            width: parent.width
            height: 1

            color: ui.ds3.bg.base
        }

        DS3.Spacing {
            height: 1
        }

        DS3.SwitchDeviceSpread {
            id: firstSwitchDeviceSpread

            atomTitle.titleItem.color: ui.ds3.figure.base
            color: deviceNav.color
        }

        Rectangle {
            width: parent.width
            height: 1

            color: ui.ds3.bg.base
        }

        DS3.Spacing {
            height: 1
        }

        DS3.SwitchDeviceSpread {
            id: secondSwitchDeviceSpread

            atomTitle.titleItem.color: ui.ds3.figure.base
            color: deviceNav.color
        }
    }
}