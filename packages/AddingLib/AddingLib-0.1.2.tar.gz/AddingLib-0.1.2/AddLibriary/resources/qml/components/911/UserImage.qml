import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13


Item {
    id: userImage
    width: 48
    height: 48

    property var imageSource: ""
    property var userName: ""
    property var color: ui.colors.dark4
    property var fontSize: 14
    property var editing: false
    property var radius: null
    property alias imageItem: imageItem

    Rectangle {
        id: noImageRect
        anchors.fill: parent
        radius: userImage.radius ? userImage.radius : height / 2
        color: userImage.color
        visible: userImage.imageSource == ""

        FontText {
            text: {
                if (userImage == null) return ""
                return util.get_image_letters(userImage.userName)
            }
            color: ui.colors.white
            opacity: 0.6
            font.pixelSize: userImage.fontSize
            anchors.centerIn: parent
            font.capitalization: Font.AllUppercase
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Image {
        id: imageItem
        anchors.fill: parent
        source: userImage.imageSource
        visible: false
        asynchronous: true
    }

    OpacityMask {
        anchors.fill: imageItem
        source: imageItem
        maskSource: noImageRect
        visible: !noImageRect.visible

        Rectangle {
            anchors.fill: parent
            radius: userImage.radius ? userImage.radius : height / 2
            color: ui.colors.black
            opacity: 0.5
            visible: userImage.editing
        }

        Image {
            visible: userImage.editing
            source: "qrc:/resources/images/temporary/change-photo.png"
            width: 32
            height: 32
            anchors.centerIn: parent
        }
    }
}