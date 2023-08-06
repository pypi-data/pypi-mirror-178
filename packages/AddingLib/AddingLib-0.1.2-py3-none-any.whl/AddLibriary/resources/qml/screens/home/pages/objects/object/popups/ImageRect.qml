
import QtQuick 2.12
import QtQuick.Controls 2.2

Rectangle {
    id: imageRect
    width: 64
    height: 64

    color: "#3a3a3a"
    border.width: 1
    border.color: "#292929"

    property alias uploadImage: uploadImage
    property alias mouseArea: mouseArea

    property alias image: image

    property var nothing: null

    Image {
        id: image
        anchors.fill: parent
        opacity: 0.4
        cache: false

        sourceSize.width: 64
        sourceSize.height: 64

        onStatusChanged: {
            if (status == Image.Error) {
                source = "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png"
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }

    Image {
        id: uploadImage
        visible: true
        anchors.centerIn: parent
        source: "qrc:/resources/images/icons/ic-popup-uploadphoto@2x.png"
    }
}