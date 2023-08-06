import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/popups/user_settings"
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    anchors.fill: parent
    property var settings: {"email": "", "roles": new Set([])}

    ScrollView {
        id: staffEditScrollView
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: saveButton.top
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: staffEditScrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (staffEditScrollView.contentHeight > staffEditScrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
        }

        ColumnLayout {
            spacing: 4
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 112
                Layout.maximumHeight: 112

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }
                Item {
                    width: 80
                    height: 80
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    Rectangle {
                        id: backgroundDropArea
                        width: 80
                        height: 80
                        radius: height / 2
                        anchors.centerIn: parent

                        property var deletedImage: false

                        Custom.UserImage {
                            id: userImageEdit
                            anchors.fill: backgroundDropArea
                            fontSize: 28
                            imageSource: {
                                if (backgroundDropArea.deletedImage) return ""
                                if (userImageEdit.urlEmpployeeAvatar) return userImageEdit.urlEmpployeeAvatar
                                if (Object.keys(currentObject.photos).length !== 0) return currentObject.photos["64x64"]
                                if (!userImageEdit.urlEmpployeeAvatar || typeof currentObject.photos["64x64"] == "undefined") return ""
                            }
                            editing: true
                            userName: currentObject ? currentObject.data.first_name + " " + currentObject.data.last_name : ""
                            property var employeeImageId: ""
                            property var urlEmpployeeAvatar: ""

                            Connections {
                                target: app.employee_module
                                onUploadAvatarEmpSuccess: {
                                     userImageEdit.urlEmpployeeAvatar = url_emp_avatar
                                     userImageEdit.employeeImageId = image_id
                                }
                            }
                            MouseArea {
                                anchors.fill: userImageEdit
                                preventStealing: true
                                onClicked: {
                                    application.debug("company -> company info -> employees -> edit -> upload employee image")
                                    fileDialogEmpAvatar.open()
                                }
                            }
                        }
                    }
                    Item {
                        visible: userImageEdit.imageSource === ""
                        width: 32
                        height: 32
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 4
                            right: parent.right
                            rightMargin: 4
                        }
                        Image {
                            sourceSize.width: 32
                            sourceSize.height: 32
                            source: "qrc:/resources/images/icons/a-plus-button.svg"
                            anchors.centerIn: parent
                        }
                    }

                    Custom.DeleteIcon {
                        id: deleteIcon
                        width: 32
                        height: 32
                        img.sourceSize.width: 32
                        img.sourceSize.height: 32
                        visible: userImageEdit.employeeImageId || (!backgroundDropArea.deletedImage && (Object.keys(currentObject.photos).length !== 0))
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 4
                            right: parent.right
                            rightMargin: 4
                        }

                        Custom.HandMouseArea {
                            anchors.fill: parent
                            preventStealing: true
                            onClicked: {
                                application.debug("company -> company info -> employees -> edit -> delete employee image")
                                userImageEdit.employeeImageId = ""
                                backgroundDropArea.deletedImage = true
                            }
                        }
                    }

                    DropArea {
                        anchors.fill: backgroundDropArea
                        enabled: true
                        onEntered: {
                            backgroundDropArea.opacity = 0.7
                            backgroundDropArea.border.color = "skyblue"
                            backgroundDropArea.border.width = 3
                        }
                        onDropped: {
                            backgroundDropArea.border.color = "transparent"
                            backgroundDropArea.opacity = 1
                            if (drop.hasUrls && drop.urls.length === 1) {
                                backgroundDropArea.deletedImage = false
                                app.employee_module.upload_avatar_employee(currentObject, drop.urls[0])
                            } else {
                                 // TODO add popups
                                 // console.log('one file only')
                            }
                        }
                        onExited: {
                           backgroundDropArea.border.color = 'transparent'
                           backgroundDropArea.opacity = 1
                        }
                    }
                }

                Custom.FileDialogImages {
                    id: fileDialogEmpAvatar
                    onAccepted: {
                        if (fileDialogEmpAvatar.fileUrls.length === 1) {
                            if (util.check_file_size(fileDialogEmpAvatar.fileUrl)) {
                                app.employee_module.upload_avatar_employee(currentObject, fileDialogEmpAvatar.fileUrl)
                            }
                            else {
                                Popups.popupByPath(
                                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                                    {
                                        title: tr.file_too_large_title,
                                        text: tr.file_too_large_descr,
                                        firstButtonText: tr.back,
                                    }
                                )
                            }
                            backgroundDropArea.deletedImage = false
                        }
                        fileDialogEmpAvatar.close()
                    }
                }

                Item {
                    width: 150
                    height: 48
                    anchors {
                        top: parent.top
                        topMargin: 12
                        right: parent.right
                        rightMargin: 16
                    }

                    Custom.Button {
                        width: parent.width
                        text: tr.cancel
                        transparent: true
                        color: ui.colors.white
                        anchors.centerIn: parent

                        onClicked: {
                            application.debug("company -> company info -> employees -> edit -> cancel")
                            editMode = false
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88

                Custom.TextFieldEdit {
                    id: userFirstName
                    width: parent.width - 16
                    key: tr.a911_name_surname + ui.required
                    valueText.control.maximumLength: 100
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Component.onCompleted: {
                        value = currentObject ? currentObject.data.first_name : ""
                    }

                    Connections {
                        target: app.employee_module
                        onSaveEmployeeValidationErrors: {
                            if (result["5"]) {
                                userFirstName.valueText.valid = false
                                userFirstName.valueText.error = tr.error_short_name_desktop
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 96
                Layout.maximumHeight: 96

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldEdit {
                    id: userLastName
                    width: parent.width - 16
                    key: tr.last_name
                    valueText.control.maximumLength: 100
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Component.onCompleted: {
                        value = currentObject ? currentObject.data.last_name : ""
                    }

                    Connections {
                        target: app.employee_module
                        onSaveEmployeeValidationErrors: {
                            if (result["6"]) {
                                userLastName.valueText.valid = false
                                userLastName.valueText.error = result["6"].message
                            }
                        }
                    }
                }
            }

            Rectangle {
                id: roleRect
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: keyText.contentHeight + rolesScroll.height + 48
                Layout.maximumHeight: keyText.contentHeight + rolesScroll.height + 48
                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.FontText {
                    id: keyText
                    text: tr.a911_role + ui.required
                    width: parent.width
                    color: ui.colors.white
                    opacity: 0.5
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }

                Roles {
                    id: rolesScroll

                    property var initialRoles: null

                    delegateWidth: parent.width - 16
                    width: parent.width - 16
                    seniorCMSEngineerAdjustmentAllowed: true

                    Component.onCompleted: {
                        isOwner = currentObject.data.role.roles.includes("OWNER")
                        isSeniorCMS = currentObject.data.role.roles.includes("SENIOR_CMS_ENGINEER")
                        roles = (() => {
                            if (appCompany.company_type == "MONITORING") {
                                return new Set(util.remove_installers(currentObject.data.role.roles))
                            } else if (appCompany.company_type == "INSTALLATION") {
                                return new Set(util.filter_installation_company_roles(currentObject.data.role.roles))
                            }
                            return new Set(currentObject.data.role.roles)
                        })()
                        initialRoles = new Set(roles)
                    }

                    anchors {
                        top: keyText.bottom
                        topMargin: 12
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: phoneEditField.height + 12
                Layout.maximumHeight: phoneEditField.height + 12

                Custom.PhonesEdit {
                    id: phoneEditField
                    width: parent.width - 16
                    key: tr.phone
                    distance: 12
                    maxPhoneNumbers: 1
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Component.onCompleted: {
                        model = currentObject ? currentObject.data.phone_numbers : []
                    }

                    Connections {
                        target: app.employee_module
                        onSaveEmployeeValidationErrors: {
                            phoneEditField.errorsResult(result)
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 96
                Layout.maximumHeight: 96

                Custom.TextFieldEdit {
                    id: userLogin
                    width: parent.width - 16
                    key: tr.a911_login
                    distance: 12
                    enabled: false
                    valueText.control.maximumLength: 100
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Component.onCompleted: {
                        value = currentObject ? currentObject.data.email : ""
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Rectangle {
        id: saveButton
        width: parent.width
        height: 72
        color: ui.colors.dark2
        anchors.bottom: parent.bottom

        Custom.Button {
            width: parent.width - 32
            text: tr.a911_save_changes
            transparent: false
            color: ui.colors.green1
            anchors.centerIn: parent
            enabledCustom: rolesScroll.rolesSize != 0

            onClicked: {
                application.debug("company -> company info -> employees -> edit -> save")

                saveButton.forceActiveFocus()
                var phones = []
                phoneEditField.listView.model.forEach(function(phone) {
                    phones.push(phone)
                })

                var settings = {}
                settings["first_name"] = userFirstName.valueText.control.text
                settings["last_name"] = userLastName.valueText.control.text
                settings["role"] = {"roles": Array.from(rolesScroll.roles)}
                settings["phone_numbers"] = phones
                if (backgroundDropArea.deletedImage) {
                   settings["photo_id"] = ""
                } else {
                    settings["photo_id"] = userImageEdit.employeeImageId ? userImageEdit.employeeImageId : currentObject.photo_id
                }
                // Raise warning popup if roles has changed
                if (rolesScroll.initialRoles.size != rolesScroll.roles.size
                    || !Array.from(rolesScroll.initialRoles).every((role) => rolesScroll.roles.has(role)                    )
                ) {
                    Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                        Object.assign({
                            firstButtonText: tr.restart_now_button,
                            firstButtonCallback: () => {
                                app.employee_module.update_employee(currentObject, settings)
                            },
                            isFirstButtonRed: true,
                            firstButtonIsOutline: true,
                            secondButtonText: tr.later_button,
                            secondButtonIsOutline: false,
                            isVertical: true
                        }, (
                            rolesScroll.isSelf
                            ? {
                                title: tr.app_restart_required_title,
                                text: tr.myself_logout_popup_desktop_descr,
                            } : {
                                title: tr.other_user_logout_popup_desktop_title,
                                text: tr.other_user_logout_popup_desktop_descr,
                            }
                        ))
                    )
                } else {
                    app.employee_module.update_employee(currentObject, settings)
                }
            }
        }
    }

    Component.onCompleted: {
        userFirstName.valueText.control.forceActiveFocus()
    }

    Connections {
        target: currentObject

        onActionSuccess: {
            editMode = false
        }
    }
}