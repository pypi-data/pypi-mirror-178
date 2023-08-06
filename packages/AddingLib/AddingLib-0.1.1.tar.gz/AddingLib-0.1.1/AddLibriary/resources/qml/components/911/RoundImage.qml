import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.13

Item {
    id: topLevel

    property var imageWidthHeight: imageWidthHeight
    property var imageRoundings: imageWidthHeight / 2
    property var imageSource: imageSource

    property alias objImage: objImage

    width: imageWidthHeight
    height: imageWidthHeight

    anchors {
        leftMargin: 4
        left: parent.left
        verticalCenter: parent.verticalCenter
    }

    Image {
        id: objImage

        visible: false

        source: {
            if (topLevel.imageSource == "WRONG") {
                return "qrc:/resources/images/icons/room-group-no-image.svg"
            } else {
                return topLevel.imageSource
            }
        }
        anchors.fill: parent
    }

    OpacityMask {
        anchors.fill: objImage
        source: objImage
        maskSource: Rectangle {
            width: topLevel.imageWidthHeight
            height: topLevel.imageWidthHeight
            radius: topLevel.imageRoundings
            visible: false
        }
    }
}