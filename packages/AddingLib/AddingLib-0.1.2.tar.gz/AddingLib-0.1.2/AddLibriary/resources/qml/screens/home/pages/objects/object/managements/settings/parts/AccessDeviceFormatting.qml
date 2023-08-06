import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12


Item {
    width: parent.width
    height: 32

    opacity: enabled ? 1.0 : 0.4
    enabled: devEnable

//    visible: device.volume_test_available // TODO

    Item {
        width: 264
        height: 24

        anchors {
            verticalCenter: parent.verticalCenter
            horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: accesDeviceFormattingIcon

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }

            mipmap: true

            width: 24
            height: 24
            source: "qrc:/resources/images/Athena/views_icons/access-device-formatting@2x.png"
        }

        ColorOverlay {
            anchors.fill: accesDeviceFormattingIcon
            source: accesDeviceFormattingIcon
            color: ui.colors.green1
        }

        Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: accesDeviceFormattingIcon.right
                leftMargin: 12
            }

            font.family: roboto.name
            font.weight: Font.Light
            font.pixelSize: 14
            color: ui.colors.green1
            text: 'Access Device Formatting'
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                console.log('AccessDeviceFormatting') // TODO
            }
        }
    }
}