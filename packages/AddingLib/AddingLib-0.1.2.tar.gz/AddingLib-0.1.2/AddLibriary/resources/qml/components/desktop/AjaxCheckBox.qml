import QtQuick 2.7
import QtQuick.Controls 2.1

CheckBox {
    id: topLevel
    checked: false
    font.family: roboto.name
    font.pixelSize: 12

    height: body.contentHeight

    property var horizontalAlignment: Text.AlignHCenter
    property var verticalAlignment: Text.AlignVCenter

    indicator: Rectangle {
        implicitWidth: 16
        implicitHeight: 16
        x: topLevel.leftPadding
        y: parent.height / 2 - height / 2
        radius: 2
        border.color: "#949494"
        color: "transparent"

        Rectangle {
            width: 10
            height: 10
            x: 3
            y: 3
            radius: 1
            color: ui.colors.green1
            visible: topLevel.checked
        }
    }

    contentItem: Text {
        id: body
        width: parent.width
        wrapMode: Text.WordWrap
        text: topLevel.text
        font: topLevel.font
        opacity: 0.5
        color: ui.colors.light1
        horizontalAlignment: topLevel.horizontalAlignment
        verticalAlignment: topLevel.verticalAlignment
        leftPadding: topLevel.indicator.width + topLevel.spacing

        onLinkActivated: Qt.openUrlExternally(link)
    }
}