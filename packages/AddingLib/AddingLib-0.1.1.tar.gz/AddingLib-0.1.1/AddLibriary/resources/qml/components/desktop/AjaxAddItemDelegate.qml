import QtQuick 2.12
import QtQuick.Controls 2.2

Item {
    property string label: ""
    property alias mouseArea: mouseArea

    Item {
        anchors.centerIn: parent

        width: image.width + itemAdd.contentWidth + 15
        height: parent.height

        Image {
            id: image
            source: "qrc:/resources/images/desktop/icons/ic-hub-add@2x.png"
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            id: itemAdd
            text: label
            font.family: roboto.name
            font.pixelSize: 14
            font.weight: Font.Light
            color: ui.colors.green1

            anchors {
                verticalCenter: parent.verticalCenter
                left: image.right
                leftMargin: 10
            }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }
    }
}