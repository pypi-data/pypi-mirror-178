import QtQuick 2.12
import QtQuick.Controls 2.13


ScrollBar {
    id: scrollBar

    function scrollTo(y) {
        scrollAnimation.to = y
        scrollAnimation.start()
    }

    height: parent.availableHeight

    anchors {
        right: parent.right
        top: parent.top
        bottom: parent.bottom
        margins: parent.objectName == "scrollView" ? 16 - width / 2 : 0
    }

    z: 30
    x: parent.width - width

    contentItem: Rectangle {
        implicitWidth: 6
        implicitHeight: 100
        radius: width / 2
        color: ui.colors.secondary
    }

    NumberAnimation on position {
        id: scrollAnimation
        duration: 400
    }
}