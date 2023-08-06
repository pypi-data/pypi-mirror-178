import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups

Item {
    width: 64
    height: 64

    Image {
        id: additionalImage
        visible: false
        source: appUser.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png" : appUser.small_image_link
        onStatusChanged: {
            if (status == Image.Error || status == Image.Null || status == Image.Loading) {
                image.source = "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"
            } else {
                image.source = appUser.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png" : appUser.small_image_link
            }
        }
    }

    Image {
        id: image
        visible: false
        width: 40
        height: 40
        anchors.centerIn: parent
        source: appUser.small_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png" : appUser.small_image_link
    }

    OpacityMask {
        id: mask
        anchors.fill: image
        source: image

        maskSource: Rectangle {
            width: 40
            height: 40
            radius: width / 2
            visible: false
        }
    }

    Rectangle {
        id: rect
        color: "transparent"
        width: 42
        height: 42
        radius: 21
        anchors.centerIn: parent
        border.width: 2
        border.color: ui.colors.green1
        opacity: 0

        Behavior on opacity { NumberAnimation { duration: 200 } }
    }

    MouseArea {
        anchors.fill: image
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onEntered: {
            rect.opacity = 0.8
        }

        onExited: {
            rect.opacity = 0.0
        }

        onClicked: {
            Popups.user_popup()
        }
    }
}