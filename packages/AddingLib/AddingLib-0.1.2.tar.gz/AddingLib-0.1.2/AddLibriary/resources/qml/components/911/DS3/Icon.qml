import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13


// Icon has size as source image
Item {
//  Color of the overlay
    property alias color: colorOverlay.color
//  Source of the image
    property alias source: imageItem.source

    width: imageItem.sourceSize.width
    height: imageItem.sourceSize.height

    Component.onCompleted: {
        imageItem.sourceSize.width = imageItem.sourceSize.width
        imageItem.sourceSize.height = imageItem.sourceSize.height
    }

    Image {
        id: imageItem

        antialiasing: true
        visible: !color.a
    }

    ShaderEffect {
        id: colorOverlay

        property variant source: imageItem
        property color color: "#00000000"

        anchors.fill: imageItem

        visible: !!color.a
        //fragmentShader: util.shaders.color
    }
}
