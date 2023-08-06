import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0


Item {
    id: delegateItem
    width: parent.width
    height: 56

    property var mainText: ""
    property var miniText: ""
    property alias mouseArea: delegateArea

    MouseArea {
        id: delegateArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }

    Rectangle {
        anchors.fill: parent
        color: delegateArea.containsMouse ? "#373737" : "transparent"
    }

    Rectangle {
        width: parent.width - 2
        height: 1
        color: ui.colors.light1
        opacity: delegateArea.containsMouse ? 0.0 : 0.1
        anchors {
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }
    }

    Rectangle {
        width: parent.width - 2
        height: 1
        color: ui.colors.light1
        opacity: delegateArea.containsMouse ? 0.0 : 0.1
        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }
    }

    Rectangle {
        width: 4
        height: parent.height
        color: ui.colors.green1
        visible: delegateArea.containsMouse
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
    }

    Item {
        id: textItem
        width: parent.width - 100
        height: parent.height
        anchors {
            left: parent.left
            leftMargin: 36
            verticalCenter: parent.verticalCenter
        }

        Text {
            id: mainTextItem
            text: delegateItem.mainText
            color: ui.colors.light1
            opacity: 1
            font.family: roboto.name
            font.pixelSize: 15
            font.letterSpacing: 1
            width: parent.width
            elide: Text.ElideRight
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: miniText == "" ? 0 : -10
            }
        }

        Rectangle {
            id: miniTextRect
            color: delegateArea.containsMouse ? "#60e3ab" : "#373737"
            width: miniTextItem.paintedWidth + 16
            height: 18
            radius: 4
            visible: delegateItem.miniText != ""
            anchors {
                left: parent.left
                leftMargin: -2
                top: mainTextItem.bottom
                topMargin: 4
            }

            Text {
                id: miniTextItem
                text: miniText
                color: delegateArea.containsMouse ? "#373737" : "#fdfdfd"
                opacity: delegateArea.containsMouse ? 1 : 0.8
                font.family: roboto.name
                font.pixelSize: 12
                font.letterSpacing: 1
                elide: Text.ElideRight
                anchors.centerIn: parent
            }
        }
    }

    Image {
        id: arrow
        width: 22
        height: 22
        rotation: 180
        source: "qrc:/resources/images/desktop/icons/ic-back-arrow@2x.png"

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }
    }
}
