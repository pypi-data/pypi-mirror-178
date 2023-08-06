import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

Item {
    width: parent.width
    height: 32

    Item {
        width: 264
        height: 24

        anchors {
            verticalCenter: parent.verticalCenter
            horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: manualIcon

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }

            width: 24
            height: 24
            source: "qrc:/resources/images/icons/ic-device-manual@2x.png"
        }

        Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: manualIcon.right
                leftMargin: 12
            }

            font.family: roboto.name
            font.weight: Font.Light
            font.pixelSize: 14
            color: ui.colors.green1
            text: tr.user_guide
        }


        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                var link = client.get_manual_link(device.device_id)
                Qt.openUrlExternally(link)
            }
        }
    }
}