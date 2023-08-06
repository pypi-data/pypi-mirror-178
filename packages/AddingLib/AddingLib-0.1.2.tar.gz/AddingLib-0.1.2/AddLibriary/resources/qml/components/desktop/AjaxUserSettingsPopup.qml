import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 320
    height: 430

    signal reChangeUserEmailSuccess(variant data)
    signal reChangeUserPasswordSuccess(variant data)
    signal reChangeUserPhoneSuccess(variant data)

    signal reNewImageReady(variant url, variant specialUrl, variant obj)
    signal reNewImageUploaded(variant token, variant obj)

    onReChangeUserEmailSuccess: {
        Popups.enter_codes(data)
    }

    onReChangeUserPasswordSuccess: {
        Popups.enter_codes(data)
    }

    onReChangeUserPhoneSuccess: {
        Popups.enter_codes(data)
    }

    onReNewImageReady: {
        if (obj != "user") return
        var objectData = {"objectType": "22", "objectId": appUser.user_id, "partNum": "00"}
        client.save_new_image(url, objectData, obj)
    }

    onReNewImageUploaded: {
        if (obj != "user") return
        client.save_user_base_setting(appUser, userNameField.fieldText, langField.data.codes[langField.currentIndex], token)
    }

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        Keys.onEnterPressed: {
            save.clicked(true)
        }

        Keys.onReturnPressed: {
            save.clicked(true)
        }

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.account
        }

        Image {
            id: userImage
            visible: false
            width: 72
            height: 72
            source: appUser.medium_image_link == "WRONG" ? "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png" : appUser.medium_image_link
            anchors {
                top: closeItem.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            property var imageData: null

            onImageDataChanged: {
                if (imageData) {
                    client.process_image(imageData, "user")
                    imageData = null
                }
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

        Image {
            anchors.centerIn: userImage
            source: "qrc:/resources/images/icons/ic-popup-uploadphoto-96.png"

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    imageFileDialog.target = userImage
                    imageFileDialog.open()
                }
            }
        }

        Image {
            id: deleteIco
            visible: appUser.medium_image_link == "WRONG" ? false : true
            source: "qrc:/resources/images/icons/trash-ico.png"

            anchors {
                bottom: userImage.bottom
                right: userImage.right
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    client.save_user_base_setting(appUser, userNameField.fieldText, langField.data.codes[langField.currentIndex], "00000000")
                }
            }
        }

        Column {
            id: column
            width: popup.width
            anchors {
                top: userImage.bottom
                topMargin: 16
                bottom: buttonGroup.top
            }

            Item {
                width: parent.width
                height: userNameField.height + 6

                AjaxSettingsTextField {
                    id: userNameField
                    width: parent.width
                    field.text: appUser.name
                    miniText: tr.name
                    readOnly: true
                    changeIcon: true

                    anchors.centerIn: parent

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            Popups.change_user_name_popup(userNameField, userNameField.field.text)
                        }
                    }
                }
            }


            Item {
                width: parent.width
                height: emailField.height + 6

                AjaxSettingsTextField {
                    id: emailField
                    width: parent.width
                    fieldText: appUser.email
                    miniText: tr.email
                    readOnly: true
                    changeIcon: true

                    anchors.centerIn: parent

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            Popups.change_user_email_popup()
                        }
                    }
                }
            }

            Item {
                width: parent.width
                height: passwordField.height + 6

                AjaxSettingsTextField {
                    id: passwordField
                    width: parent.width
                    fieldText: "password"
                    miniText: tr.password
                    readOnly: true
                    password: true
                    changeIcon: true

                    anchors.centerIn: parent

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            Popups.change_user_password_popup()
                        }
                    }
                }
            }

            Item {
                width: parent.width
                height: phoneField.height + 6

                AjaxSettingsTextField {
                    id: phoneField
                    width: parent.width
                    fieldText: appUser.phone
                    miniText: tr.phone
                    readOnly: true
                    changeIcon: true

                    anchors.centerIn: parent

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            Popups.change_user_phone_popup()
                        }
                    }
                }
            }

            Item {
                width: parent.width
                height: langField.height + 6

                AjaxSettingsCombobox {
                    id: langField
                    smallAndBright: true
                    property var data: tr.get_sms_locales()
                    width: parent.width
                    miniText: tr.language_alt
                    anchors.centerIn: parent
                    model: data.languages
                    currentIndex: data.codes.indexOf(appUser.locale)
                }
            }
        }

        Item {
            id: buttonGroup
            width: parent.width
            height: 48

            anchors.bottom: parent.bottom

            Rectangle {
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 48
                }
                width: parent.width
                height: 1
                color: ui.colors.light1
                opacity: 0.1
            }

            MouseArea {
                width: parent.width / 2
                height: parent.height
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                anchors.left: parent.left

                Text {
                    anchors.centerIn: parent
                    text: tr.cancel
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 14
                }

                onClicked: {
                    popup.close()
                }
            }

            MouseArea {
                id: save
                width: parent.width / 2
                height: parent.height
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                anchors.right: parent.right

                Text {
                    anchors.centerIn: parent
                    text: tr.save
                    color: ui.colors.green1
                    font.family: roboto.name
                    font.pixelSize: 14
                }

                onClicked: {
                    client.save_user_base_setting(appUser, userNameField.field.text, langField.data.codes[langField.currentIndex], "")
                }
            }
        }
    }

    Connections {
        target: client

        onActionSuccess: {
            popup.close()
        }
    }

    Component.onCompleted: {
        client.changeUserEmailSuccess.connect(reChangeUserEmailSuccess)
        client.changeUserPasswordSuccess.connect(reChangeUserPasswordSuccess)
        client.changeUserPhoneSuccess.connect(reChangeUserPhoneSuccess)

        client.newImageReady.connect(reNewImageReady)
        client.newImageUploaded.connect(reNewImageUploaded)
    }
}
