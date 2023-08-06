import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: imageItem

    width: size
    height: size

    property var size: 0
    property var radius: 0
    property var deleteSize: 0
    property var editable: false

    property var trueImage: ""
    property var trueImageId: ""
    property var defaultImage: ""

    property var text: ""
    property var defaultTextColor: ui.colors.middle1
    property var defaultBackgroundColor: ui.colors.dark4

    property alias deleteArea: deleteArea

    Rectangle {
        radius: imageItem.radius
        visible: originalImage.source == ""
        color: imageItem.defaultBackgroundColor

        anchors.fill: parent

        Desktop.NormalText {
            text: imageItem.text ? imageItem.text.charAt(0).toUpperCase() : "..."

            width: parent.width
            size: imageItem.size / 2
            color: imageItem.defaultTextColor
            horizontalAlignment: Text.AlignHCenter

            anchors.centerIn: parent
        }
    }

    Image {
        id: additionalImage

        mipmap: true
        visible: false
        source: imageItem.trueImage ? imageItem.trueImage : imageItem.defaultImage

        onStatusChanged: {
            if (status == Image.Error || status == Image.Null || status == Image.Loading) {
                originalImage.source = imageItem.defaultImage
            } else {
                originalImage.source = imageItem.trueImage ? imageItem.trueImage : imageItem.defaultImage
            }
        }
    }

    Image {
        id: originalImage

        width: imageItem.width
        height: imageItem.height

        anchors.fill: parent

        mipmap: true
        visible: false
        source: imageItem.defaultImage
    }

    OpacityMask {
        source: originalImage
        anchors.fill: originalImage

        visible: originalImage.source != ""

        maskSource: Rectangle {
            width: imageItem.width
            height: imageItem.height
            radius: imageItem.radius
            visible: false
        }
    }

    Image {
        id: deleteImage

        visible: imageItem.editable && originalImage.source != ""

        width: imageItem.deleteSize
        height: imageItem.deleteSize

        sourceSize {
            width: imageItem.deleteSize
            height: imageItem.deleteSize
        }

        source: "qrc:/resources/images/icons/control-a-minus-button.svg"

        anchors {
            top: parent.top
            topMargin: 12
            right: parent.right
            rightMargin: 12
        }

        Custom.HandMouseArea {
            id: deleteArea
        }
    }
}
