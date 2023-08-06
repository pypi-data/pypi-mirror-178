import QtQuick 2.12
import QtGraphicalEffects 1.13


Loader {
    anchors.fill: parent

    onSourceChanged: animation.running = true

    NumberAnimation {
        id: animation
        target: screenLoader.item
        property: "opacity"
        from: 0
        to: 1
        duration: 200
        easing.type: Easing.InExpo
    }
}