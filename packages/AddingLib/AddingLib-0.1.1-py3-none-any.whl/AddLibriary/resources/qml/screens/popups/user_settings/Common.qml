import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    Connections {
        target: appUser

        onDataChanged: {
            phoneField.atomInput.text = appUser.data.user_info.phone
            emailField.atomInput.text = appUser.data.user_info.email
        }
    }

    Connections {
        target: app

        onUserInfoUpdateSuccess: {
            app.get_current_user()
            notificationPopup(tr.Edit_profile_success1)
        }

        onNewImageReady: {
            var settings = {}
            settings["url"] = data["path"]
            app.hub_management_module.upload_user_photo(settings)
        }
    }

    Connections {
        target: app.hub_management_module

        onUploadPhotoSuccess: {
            app.get_current_user()
        }

        onDeletePhotoSuccess: {
            app.get_current_user()
        }
    }

    Connections {
        target: appUser

        onIsUserHasHubsRequestResponse: {
            user_has_hubs ? DesktopPopups.popupByPath(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/delete_account_wizard/HubDeletionWarning.qml",
            ) :
                appUser.delete_user_account_request()
        }

        onUserHasCompaniesEmployeeResponse: {
            DesktopPopups.popupByPath(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/delete_account_wizard/EmployeeWarning.qml",
                {"companies": companies, "isOwner": false}
            )
        }

        onUserHasCompaniesOwnerResponse: {
            DesktopPopups.popupByPath(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/delete_account_wizard/EmployeeWarning.qml",
                {"companies": companies, "isOwner": true}
            )
        }

        onDeleteUserAccountRequestResponse: {
            DesktopPopups.delete_account_verification_popup()
        }
    }

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.a911_general
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        width: parent.width

        contentSpacing: 24

        anchors {
            topMargin: navBarModal.height
            bottomMargin: buttonBar.height
        }

        DS3.UserImageUpload {
            property var imageData: null

            property var isUserImage: appUser &&
                appUser.data &&
                appUser.data.user_info &&
                appUser.data.user_info.image_urls &&
                appUser.data.user_info.image_urls.base_path


            // A signal for opening image file dialog within this popup
            signal imageFileDialogOpened

            onImageDataChanged: {
                if (imageData) {
                    app.process_image(imageData, "user")
                }
            }

            anchors.horizontalCenter: parent.horizontalCenter

            imageRect.source: isUserImage ? appUser.data.user_info.image_urls.base_path + appUser.data.user_info.image_urls.medium : ""

            uploadSwitchCheckedCallback: () => {
                imageFileDialog.target = imageRect
                imageFileDialog.isRounded = true
                imageFileDialog.open()
                imageFileDialogOpened()
                sheetAction.close()
            }
            deleteSwitchCheckedCallback: () => {
                imageRect.source = "WRONG"
                imageRect.imageData = null
                app.hub_management_module.delete_user_photo()
                sheetAction.close()
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            Connections {
                target: app.restore_pass_module

                onUpdateUserTextFieldError: {
                    if (result["1"]) {
                        firstName.atomInput.error = result["1"].message
                        firstName.atomInput.valid = false
                    }
                    if (result["2"]) {
                        lastName.atomInput.error = result["2"].message
                        lastName.atomInput.valid = false
                    }
                }
            }

            DS3.InputSingleLine {
                id: firstName

                atomInput {
                    label: tr.name
                    text: appUser.data.user_info.first_name
                    maximumLength: 100

                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                    }
                }
            }

            DS3.InputSingleLine {
                id: lastName

                atomInput {
                    label: tr.last_name
                    text: appUser.data.user_info.last_name
                    maximumLength: 100

                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                    }
                }
            }
        }
        DS3.SettingsContainer {
            width: parent.width

            DS3.InputSingleLine {
                id: phoneField

                atomInput {
                    label: tr.phone
                    text: appUser.data.user_info.phone
                }

                DS3.MouseArea {
                    onClicked: {
                        Popups.edit_phone_number_popup()
                    }
                }
            }

            DS3.InputSingleLine {
                id: emailField

                atomInput {
                    label: tr.email
                    text: appUser.data.user_info.email
                }

                DS3.MouseArea {
                    onClicked: {
                        Popups.edit_email_popup()
                    }
                }
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsPickerTitleSecondary {
                id: languageCombo

                atomTitle.title: tr.desktop_notific_language
                model: tr.get_sms_locales().languages
                currentIndex: {
                    if (appUser.data.user_info.locale) {
                        if (appUser.data.user_info.locale == "lt_lt") return tr.get_sms_locales().codes.indexOf("lt_LT")
                        return tr.get_sms_locales().codes.indexOf(appUser.data.user_info.locale)
                    }
                    return 0
                }
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.InputPassword {
                id: passwordField

                atomInput {
                    label: tr.password
                    text: "··············"
                }

                DS3.MouseArea {
                    onClicked: {
                        Popups.user_changed_password_popup()
                    }
                }
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: newsletterSwitch

                title: tr.i_agree_to_receive_updates
                visible: __newsletter_features__
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.ButtonRow {
                id: delete_account
                width: parent.width

                text: tr.delete_account_button
                isDanger: true

                onClicked: {
                    DesktopPopups.popupByPath(
                        "qrc:/resources/qml/screens/popups/DeleteAccountPromptPopup.qml"
                    )
                }
            }
        }
    }

    DS3.ButtonBar {
        id: buttonBar

        anchors.bottom: parent.bottom

        hasBackground: true
        button {
            text: tr.a911_save_changes

            onClicked: {
                var settings = {}
                settings["first_name"] = firstName.atomInput.text
                settings["last_name"] = lastName.atomInput.text
                settings["locale"] = tr.get_sms_locales().codes[languageCombo.currentIndex]
                app.restore_pass_module.update_user_info(settings)
            }
        }
    }
}