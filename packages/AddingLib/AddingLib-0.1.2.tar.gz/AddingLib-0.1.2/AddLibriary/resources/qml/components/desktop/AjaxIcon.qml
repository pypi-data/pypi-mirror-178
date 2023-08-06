import QtQuick 2.7
import QtGraphicalEffects 1.12

Item {
    implicitWidth: 24
    implicitHeight: 24

// PROPS:
//  source of the icon
    property var iconSource: ""
//  color of the icon
    property var iconColor: ""
//  strength of the color overlay
    property var colorOverlayOpacity: 1

    Image {
        id: icon

        source: iconSource
        sourceSize.width: parent.width
        sourceSize.height: parent.height
        anchors.centerIn: parent
        visible: false
    }

    ColorOverlay {
        anchors.fill: icon
        opacity: colorOverlayOpacity
        source: icon
        color: iconColor
        visible: true
    }
}
