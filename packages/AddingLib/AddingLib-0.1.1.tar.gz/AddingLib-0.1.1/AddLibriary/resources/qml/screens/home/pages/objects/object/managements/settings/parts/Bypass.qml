import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    width: parent.width
    height: visible ? 40 : 0

    opacity: enabled ? 1.0 : 0.4
    enabled: devEnable

    visible: {
        if (device.obj_type == "14" || device.obj_type == "1b") {
            return device.bypass_available
        }
        return hub.firmware_version_dec >= 208107
    }

    Item {
        width: 284
        height: 24

        anchors {
            verticalCenter: parent.verticalCenter
            horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: bypassIcon

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }

            mipmap: true

            width: 40
            height: 40
            sourceSize.width: 40
            sourceSize.height: 40
            source: "qrc:/resources/images/Athena/settings_icons/TemporaryDeactivationSettings-L.svg"
        }

        DS3.Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: bypassIcon.right
                leftMargin: 12
            }

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.interactive
            text: tr.bypass_mode
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                testLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/Bypass.qml")
                popup.width = 722
            }
        }
    }
}
