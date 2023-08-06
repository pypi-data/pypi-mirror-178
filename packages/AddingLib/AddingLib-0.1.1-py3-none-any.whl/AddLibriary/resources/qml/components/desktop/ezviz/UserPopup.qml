import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 270
    height: 302

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.account
        }

        Image {
            id: userImage
            visible: false
            width: 72
            height: 72
            source: "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"
            anchors {
                top: closeItem.bottom
                topMargin: 16
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
            font.pixelSize: 15

            text: ezviz.username
            width: parent.width - 64
            elide: Text.ElideRight
            horizontalAlignment: Text.AlignHCenter

            anchors {
                top: userImage.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Column {
            id: column
            width: popup.width
            anchors {
                top: userNameLabel.bottom
                topMargin: 24
                bottom: parent.bottom
            }

            Rectangle {
                width: parent.width - 2
                height: 1
                color: ui.colors.light1
                opacity: 0.1
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Item {
                id: addCamera
                width: parent.width
                height: 48

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        application.addEzvizCloudCamera()
                        popup.close()
                    }
                }


                Item {
                    height: parent.height
                    width: addIcon.width + addLabel.width + 8
                    anchors {
                        verticalCenter: parent.verticalCenter
                        horizontalCenter: parent.horizontalCenter
                    }

                    Image {
                        id: addIcon
                        visible: false
                        source: "qrc:/resources/images/icons/ic-hub-add@2x.png"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: -2
                        }
                    }

                    ColorOverlay {
                        anchors.fill: addIcon
                        source: addIcon
                        color: ui.colors.green1
                    }

                    Text {
                        id: addLabel
                        text: tr.add_camera
                        color: ui.colors.green1
                        font.family: roboto.name
                        font.pixelSize: 14
                        anchors {
                            left: addIcon.right
                            leftMargin: 8
                            verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }

            Rectangle {
                width: parent.width - 2
                height: 1
                color: ui.colors.light1
                opacity: 0.1
                anchors.horizontalCenter: parent.horizontalCenter
            }


            Item {
                id: quitEzviz
                width: parent.width
                height: 48

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        popup.close()
                        ezviz.logout()
                    }
                }

                Item {
                    height: parent.height
                    width: quitIcon.width + quitLabel.width + 8
                    anchors {
                        verticalCenter: parent.verticalCenter
                        horizontalCenter: parent.horizontalCenter
                    }

                    Image {
                        id: quitIcon
                        width: 20
                        height: 20
                        visible: true
                        source: "qrc:/resources/images/icons/ic-tooltip-signout@2x.png"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: -2
                        }
                    }

                    Text {
                        id: quitLabel
                        text: tr.account_settings_array_1
                        color: ui.colors.light1
                        opacity: 0.7
                        font.family: roboto.name
                        font.pixelSize: 13
                        anchors {
                            left: quitIcon.right
                            leftMargin: 8
                            verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }
        }
    }
}
