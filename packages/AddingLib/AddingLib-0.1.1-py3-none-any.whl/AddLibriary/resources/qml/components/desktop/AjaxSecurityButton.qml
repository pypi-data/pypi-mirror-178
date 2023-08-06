import QtQuick 2.7
import QtQuick.Controls 2.1
import "qrc:/resources/qml/components/911/" as Custom

Rectangle {

    property var sourceImage: ""
    property var colorBorderText: ui.colors.middle1
    property alias mouseArea: mouseArea
    property alias textButtonId: textButtonId

    width: 206
    height: 40

    color: "transparent"
    radius: 20

    border {
        color: colorBorderText
        width: 1
    }

    Image {
        width: 24
        height: 24
        sourceSize.width: 24
        sourceSize.height: 24
        source: sourceImage
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            leftMargin: 11
        }
    }

    Text {
        id: textButtonId
        anchors.centerIn: parent
        font.pixelSize: 14
        font.family: roboto.name
        font.bold: false
        color: colorBorderText
    }

    Custom.HandMouseArea {
        id: mouseArea
        anchors.fill: parent
    }
}
