import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups

Popup {
    id: topLevel
    width: 241
    height: 325

    x: application.width - width - 16
    y: 62
    modal: false
    focus: true

    padding: 0

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Item {}

    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }


    Rectangle {
        anchors.fill: parent
        color: "#212121"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999

        Image {
            id: userImage
            visible: false
            width: 72
            height: 72
            source: appUser.medium_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png" : appUser.medium_image_link
            anchors {
                top: parent.top
                topMargin: 31
                horizontalCenter: parent.horizontalCenter
            }
        }

        OpacityMask {
            anchors.fill: userImage
            source: userImage

            maskSource: Rectangle {
                width: 72
                height: 72
                radius: width / 2
                visible: false
            }
        }

        Text {
            id: userNameLabel
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 14

            text: appUser.name
            width: parent.width - 64
            elide: Text.ElideRight
            horizontalAlignment: Text.AlignHCenter

            anchors {
                top: userImage.bottom
                topMargin: 19
                horizontalCenter: parent.horizontalCenter
            }
        }

        Text {
            id: userEmailLabel
            color: ui.colors.light1
            opacity: 0.4
            font.family: roboto.name
            font.pixelSize: 10

            text: appUser.email

            anchors {
                top: userNameLabel.bottom
                topMargin: 12
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            id: settingsItem
            height: 12
            width: settingsIcon.width + 6 + settingsLabel.width

            anchors {
                top: userEmailLabel.bottom
                topMargin: 28
                horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                id: mouseAreaSettings
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    topLevel.close()
                    Popups.user_settings_popup()
                }
            }

            Image {
                id: settingsIcon
                source: "qrc:/resources/images/icons/ic-tooltip-settings@2x.png"

                height: 20
                width: 20

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }
            }

            Text {
                id: settingsLabel
                text: tr.account
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 12

                anchors {
                    left: settingsIcon.right
                    leftMargin: 6
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        Item {
            id: videoSurveillance
            width: parent.width - 30
            height: 48
            anchors {
                horizontalCenter: parent.horizontalCenter
                top: settingsItem.bottom
                topMargin: 22
            }

            Rectangle {
                anchors.fill: parent
                color: "transparent"
                border.width: 2
                border.color: ui.colors.green1
                opacity: 0.9
            }

            MouseArea {
                id: mouseAreaVideoSurveillance
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    topLevel.close()
                    Popups.video_surveillance_settings()
                }
            }

            Item {
                id: videoSurveillanceItem
                width: videoSurveillanceIcon.width + 6 + videoSurveillanceLabel.width
                height: parent.height
                anchors.centerIn: parent

                Image {
                    id: videoSurveillanceIcon
                    source: "qrc:/resources/images/icons/ic-menu-camera.png"
                    sourceSize.height: 38
                    sourceSize.width: 38
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }
                }

                Text {
                    id: videoSurveillanceLabel
                    text: tr.video_surveillance
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 12

                    anchors {
                        left: videoSurveillanceIcon.right
                        leftMargin: 6
                        verticalCenter: parent.verticalCenter
                    }
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.light1
            opacity: 0.1
            anchors {
                bottom: parent.bottom
                bottomMargin: 41
            }
        }

        Item {
            id: quitRect
            width: parent.width
            height: 41

            anchors {
                bottom: parent.bottom
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    topLevel.close()
                    client.logout(false)
                }
            }

            Item {
                height: 16
                width: quitIcon.width + quitLabel.width + 6
                anchors {
                    verticalCenter: parent.verticalCenter
                    horizontalCenter: parent.horizontalCenter
                }
                Image {
                    id: quitIcon
                    source: "qrc:/resources/images/icons/ic-tooltip-signout@2x.png"
                }
                Text {
                    id: quitLabel
                    text: tr.account_settings_array_1
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 12
                    anchors {
                        left: quitIcon.right
                        leftMargin: 6
                    }
                }
            }
        }
    }
}
