import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


ScrollBar {
    id: scrollBar

//  Wether scrollBar has padding inside parent
    property bool hasPadding: parent.objectName == "scrollView"
//  Scroll animation element for manual scroll animation control
    property alias scrollAnimation: scrollAnimation

    function scrollTo(y) {
        if (parent) {
            scrollAnimation.to = Math.min(Math.max((y - 20) / parent.contentHeight, 0), 1 - scrollBar.size)
            scrollTimer.start()
        }
    }

    Timer {
        id: scrollTimer

        interval: 1

        onTriggered: {
            scrollAnimation.start()
        }
    }

    height: parent.availableHeight

    anchors {
        right: parent.right
        top: parent.top
        bottom: parent.bottom
    }

    padding: 0
    minimumSize: 0.1

    contentItem: Item {
        implicitWidth: hasPadding ? indicator.width + 8 : 4
        implicitHeight: 100

        Rectangle {
            id: indicator

            width: area.containsMouse ? 8 : 4
            height: parent.height

            anchors {
                top: parent.top
                bottom: parent.bottom
                right: parent.right
                margins: hasPadding ? 8 : 0
            }

            radius: width / 2
            color: ui.ds3.figure.secondary

            Behavior on width {
                NumberAnimation {
                    duration: 100
                }
            }
        }
    }

    NumberAnimation on position {
        id: scrollAnimation

        duration: 400
    }

    DS3.MouseArea {
        id: area

        cursorShape: Qt.ArrowCursor

        onPressed: mouse.accepted = false
    }
}
