import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Item {
    width: parent.width
    height: 48

    property alias backArea: backArea

    Rectangle {
        id: divTop
        width: parent.width
        height: 1
        color: "#fdfdfd"
        opacity: 0.1
        anchors.top: parent.top
    }

    MouseArea {
        id: backArea
        width: parent.width
        height: parent.height
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text {
            anchors.centerIn: parent
            color: "#fdfdfd"
            font.family: roboto.name
            font.pixelSize: 14
            text: tr.start
        }

        anchors.left: parent.left
    }
}