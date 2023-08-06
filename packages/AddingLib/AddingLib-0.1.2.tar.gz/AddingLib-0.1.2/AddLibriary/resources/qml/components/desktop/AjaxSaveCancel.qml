import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Item {
    width: parent.width
    height: 48

    property alias cancelArea: cancelArea
    property alias saveArea: saveArea

    property string saveText: tr.save
    property string cancelText: tr.cancel

    property alias cancelAreaText: cancelAreaText
    property alias saveAreaText: saveAreaText
    property var saveAreaColor: ui.colors.green1

    Rectangle {
        id: div
        width: 1
        height: parent.height - 2
        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        color: ui.colors.light1
        opacity: 0.05
    }

    Rectangle {
        id: divTop
        width: parent.width
        height: 1
        color: ui.colors.light1
        opacity: 0.05
        anchors.top: parent.top
    }

    MouseArea {
        id: saveArea
        width: parent.width / 2
        height: parent.height
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text {
            id: saveAreaText
            width: parent.width - 32
            anchors.centerIn: parent
            color: saveAreaColor
            font.family: roboto.name
            font.pixelSize: 14
            text: saveText
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
        }

        anchors.right: parent.right
    }

    MouseArea {
        id: cancelArea
        width: parent.width / 2
        height: parent.height
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text {
            id: cancelAreaText
            width: parent.width - 32
            anchors.centerIn: parent
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 14
            text: cancelText
            horizontalAlignment: Text.AlignHCenter
        }

        anchors.left: parent.left
    }
}