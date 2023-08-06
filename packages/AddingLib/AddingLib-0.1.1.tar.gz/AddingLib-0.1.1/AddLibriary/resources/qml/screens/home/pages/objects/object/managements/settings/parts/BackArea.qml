import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

Item {
    width: 64
    height: 32

    property alias backArea: backArea

    z: 100
    Image {
        sourceSize.width: 16
        sourceSize.height: 16
        anchors.centerIn: parent
        source: "qrc:/resources/images/icons/back.svg"
    }
    MouseArea {
        id: backArea

        width: parent.width
        height: parent.height

        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        anchors.left: parent.left
    }
}