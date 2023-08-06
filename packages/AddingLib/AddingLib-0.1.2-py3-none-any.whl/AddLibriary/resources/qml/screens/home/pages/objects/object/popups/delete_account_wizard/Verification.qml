import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

DS3.Popup {
    id: verificationPopup

    width: 500
    height: maxPopupHeight

    modal: true
    focus: true

    header: DS3.NavBarModal {
        onClosed: () => {
            DesktopPopups.popupByPath(
                "qrc:/resources/qml/screens/popups/DeleteUserAccountClosePopup.qml",
                {callback: () => {verificationPopup.close()}}
            )
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        anchors.horizontalCenter: parent.horizontalCenter

        titleComponent.text: tr.delete_account_confirm_title
        descComponent.text: tr.we_ve_sent_you_an_e_mail_sms_messages_containing_security_codes
    }

    DS3.Spacing {
        height: 24
    }

    Item {
        width: 452
        height: smsCode.height + emailCode.height

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.SettingsContainer {
            anchors.fill: parent

            DS3.InputSingleLine {
                id: smsCode

                atomInput {
                    label: tr.code_from_sms
                    placeholderText: "······"
                    onTextChanged: atomInput.text = util.validator(atomInput.text, 24)
                }
            }
            DS3.InputSingleLine {
                id: emailCode

                atomInput {
                    label: tr.code_from_email
                    placeholderText: "······"
                    onTextChanged: atomInput.text = util.validator(atomInput.text, 24)
                }
            }
        }
    }

    DS3.Spacing {
        height: 32
    }
    
    DS3.Text {
        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.resend
        style: ui.ds3.text.button.SBold
        color: ui.ds3.figure.interactive
        horizontalAlignment: Text.AlignHCenter

        DS3.MouseArea{
            onClicked: {
                DesktopPopups.please_wait_popup(
                    tr.requesting_new_code,
                    30, // default
                    [appUser.deleteUserAccountRequestFailed, appUser.userHasCompaniesEmployeeResponse, appUser.userHasCompaniesOwnerResponse, appUser.deleteUserAccountRequestResponse,]
                )
                appUser.delete_user_account_request()
            }
        }
    }

    footer: DS3.ButtonBar {
        buttonText: tr.delete_account_button
        hasBackground: true
        isAttention: true
        enabled: smsCode.atomInput.text.length == 6 & emailCode.atomInput.text.length == 6

        button.onClicked: {
            DesktopPopups.please_wait_popup(
                tr.deleting_progress_desktop,
                30, // default
                [appUser.deleteUserAccountVerificationFailed, appUser.deleteUserAccountVerificationResponse]
            )
            appUser.delete_user_account_send_verification_request(smsCode.atomInput.text, emailCode.atomInput.text)

        }
        Connections {
            target: appUser

            onDeleteUserAccountVerificationResponse: {
                if (verification_resp == "success") {
                    DesktopPopups.popupByPath(
                        "qrc:/resources/qml/screens/popups/DeleteAccountSuccessPopup.qml",
                        {action: () => {
                            verificationPopup.close()
                            close_settings_popup()
                            app.login_module.logout()
                            screenLoader.source = "qrc:/resources/qml/screens/login/Login.qml"
                        }}
                    )
                } else if (verification_resp == "code_error" || verification_resp == "companies_error") {
                    DesktopPopups.text_popup(tr.wrong_security_codes_title, tr.wrong_security_codes_descr)
                } else if (verification_resp == "companies_after_codes_error") {
                    DesktopPopups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                        {
                            title: tr.cannot_delete_account_title,
                            text: tr.delete_account_employee_title,
                            firstButtonCallback: () => {verificationPopup.close()}
                        }
                    )
                }
            }
            onDeleteUserAccountVerificationFailed: {
                // general error
                DesktopPopups.text_popup(tr.cannot_delete_account_title, tr.cannot_delete_account_descr)
            }
        }
    }
}