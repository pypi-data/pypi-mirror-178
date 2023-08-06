import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

Item {
    id: deleg

    Item {
        width: parent.width - 60
        height: 34
        anchors {
            horizontalCenter: deleg.horizontalCenter
            verticalCenter: deleg.verticalCenter
        }

        Image {
            id: userSmallImage
            visible: false
            width: 30
            height: 30
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }

            source: {
                if (!user.small_images_link) {
                    return "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureSmall.png"
                }
                return user.small_images_link
            }
        }

        OpacityMask {
            anchors.fill: userSmallImage
            source: userSmallImage

            maskSource: Rectangle {
                width: 30
                height: 30
                radius: width / 2
                visible: false
            }
        }

        Text {
            id: userFullName
            font.family: roboto.name
            font.pixelSize: 14
            color: ui.colors.light1
            text: user.name  + " " + user.last_name
            elide: Text.ElideRight

            anchors {
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: -8
                left: userSmallImage.right
                leftMargin: 10
            }

            Component.onCompleted: {
                if (contentWidth > parent.width - userRoleLabel.width - 100) {
                    width = parent.width - userRoleLabel.width - 100
                }
            }
        }

        Rectangle {
            id: userRoleLabel
            height: 14
            width: roleText.contentWidth + 6
            radius: 2
            color: hub_role == "USER" ? "#9a9a9a" : "#60e3ab"

            visible: (hub_role == "USER" || hub_role == "MASTER" || hub_role == "PRO")

            Text {
                id: roleText
                font.family: roboto.name
                font.pixelSize: 12
                anchors.centerIn: parent
                text: {
                    if (hub_role == "USER") return tr.user
                    if (hub_role == "MASTER") return tr.admin
                    if (hub_role == "PRO") return tr.pro
                    return ""
                }
                opacity: 0.7
                color: "#484848"
            }

            anchors {
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: -8
                left: userFullName.right
                leftMargin: 10
            }
        }

        Text {
            id: userEmail
            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.white
            opacity: 0.5
            text: user.email

            anchors {
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: 8
                left: userSmallImage.right
                leftMargin: 10
            }
        }
    }

    property var nothing: {
        var link = user.small_image_link
        if (link == "" || link == "WRONG") {
            userSmallImage.source = "qrc:/resources/images/desktop/delegates/RoomPicture/RoomPictureSmall.png"
        } else {
            userSmallImage.source = link
        }
    }
}
