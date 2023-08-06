
import QtQuick 2.12
import QtQuick.Controls 2.2

Rectangle {
    id: imageRect
    width: 64
    height: 64

    color: "#3a3a3a"
    border.width: 1
    border.color: "#292929"

    property var sourceImage: null

    property bool uploadAvailable: false

    property alias uploadArea: uploadArea
    property alias deleteArea: deleteArea

    Image {
        id: objectImage
        anchors.fill: parent
        opacity: 0.4
        cache: false
        source: sourceImage == "WRONG" ? "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureMedium.png" : sourceImage
        sourceSize.width: 64
        sourceSize.height: 64
    }

    Image {
        id: newImageUpload
        visible: uploadAvailable
        anchors.centerIn: parent
        source: "qrc:/resources/images/desktop/icons/ic-popup-uploadphoto@2x.png"

        MouseArea {
            id: uploadArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }
    }

    Image {
        id: deleteIco
        visible: sourceImage != "WRONG" && uploadAvailable
        source: "qrc:/resources/images/desktop/icons/trash-ico.png"

        anchors {
            bottom: objectImage.bottom
            right: objectImage.right
            bottomMargin: -4
            rightMargin: -4
        }

        MouseArea {
            id: deleteArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }
    }
}