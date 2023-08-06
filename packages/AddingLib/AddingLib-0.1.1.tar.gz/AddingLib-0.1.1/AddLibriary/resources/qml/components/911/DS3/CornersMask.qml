import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
    id: cornersMask

    property int maskRadius: 12

    anchors.fill: parent

    clip: true

    Rectangle {
        anchors {
            fill: parent
            margins: -cornersMask.maskRadius
        }

        color: ui.ds3.figure.transparent
        radius: cornersMask.maskRadius * 2
        border {
            width: cornersMask.maskRadius
            color: ui.ds3.bg.lowest
        }
    }
}
