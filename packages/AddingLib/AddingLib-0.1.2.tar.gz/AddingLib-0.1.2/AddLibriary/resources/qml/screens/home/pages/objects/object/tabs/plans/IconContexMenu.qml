import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13


Rectangle {
    property var colorDots: "#d8d8d8"
    width: 40
    height: 40
    anchors {
        top: parent.top
        right: parent.right
    }
    color: "transparent"

    Rectangle {
        width: 30
        height: 30
        color: ui.colors.dark1
        radius: height / 2
        anchors {
            centerIn: parent
        }

        Rectangle {
            width: 3
            height: 17
            anchors.centerIn: parent
            color: "transparent"
            Rectangle {
                width: 3
                height: 3
                color: colorDots
                anchors.top: parent.top
            }
            Rectangle {
                width: 3
                height: 3
                color: colorDots
                anchors.top: parent.children[0].bottom
                anchors.topMargin: 4
            }
            Rectangle {
                width: 3
                height: 3
                color: colorDots
                anchors.top: parent.children[1].bottom
                anchors.topMargin: 4
            }
        }
    }
}