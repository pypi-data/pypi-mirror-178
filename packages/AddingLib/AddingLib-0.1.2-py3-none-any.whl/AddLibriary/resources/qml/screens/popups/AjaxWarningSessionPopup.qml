import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 320
    height: closeItem.height + 16 + contentItem.height + buttonGroup.height

    property var todo: null
    property var logoutText: null
    property var isTwoFa: false     // after todo function emit open 2fa popup signal

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        focus: true

        Keys.onEnterPressed: {
            save.clicked(true)
        }

        Keys.onReturnPressed: {
            save.clicked(true)
        }

        Custom.PopupHeader {
            id: closeItem

            width: parent.width
            height: 64
            radius: parent.radius
            title: tr.warning
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.top: closeItem.bottom
        }

        Item {
            id: contentItem

            width: parent.width
            height: 205 + 16 + contentText.height + 32
            anchors {
                top: closeItem.bottom
                topMargin: 16
            }

            Image {
                id: phoneImage

                sourceSize.width: 113
                sourceSize.height: 205
                source: "qrc:/resources/images/desktop/phone_illustration.svg"
                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Image {
                id: contentImage

                sourceSize.width: 50
                sourceSize.height: 50
                source: "qrc:/resources/images/desktop/icons/icons_sign_out.svg"
//                z: 10

                anchors {
                    top: phoneImage.top
                    topMargin: 80
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Text {
                id: contentText

                text: logoutText
                width: parent.width - 64
                height: contentHeight
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 14
                opacity: 0.8
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: phoneImage.bottom
                    topMargin: 16
                    horizontalCenter: parent.horizontalCenter
                }
            }
        }

        Item {
            id: buttonGroup

            width: parent.width - 48
            height: 72

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }

            Custom.Button {
                id: cancelButton

                width: 130
                height: 40
                color: ui.colors.light3
                transparent: true

                text: tr.cancel

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    popup.close()
                }
            }

            Custom.Button {
                id: nextButton

                width: 130
                height: 40
                transparent: true

                text: tr.continue_android

                anchors {
                    left: cancelButton.right
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    popup.todo()
                    if (isTwoFa) {
                        openSecondStepTwoFaPopupSignal()
                    }
                }
            }
        }
    }

    Connections {
        target: app.security_module

        onActionSuccess: {
            app.security_module.get_sessions()
            popup.close()
        }
    }
}
