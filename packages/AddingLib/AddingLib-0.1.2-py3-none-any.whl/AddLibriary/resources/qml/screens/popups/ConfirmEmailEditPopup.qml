import QtQuick 2.13
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


AjaxPopup {
    id: popup

    objectName: "confirmEmailPopup"
    width: 364
    height: 420
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    property var confirmationInfo: null
    property var preset: null

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        radius: 10
        color: ui.colors.dark3

        anchors.fill: parent

        Item {
            width: 32
            height: 32

            anchors {
                top: parent.top
                topMargin: 16
                right: parent.right
                rightMargin: 16
            }

            Image {
                source: "qrc:/resources/images/icons/a-delete-button.svg"
                sourceSize {
                    width: 32
                    height: 32
                }
            }

            Custom.HandMouseArea {
                onClicked: {
                    popup.close()
                }
            }
        }

        Item {
            id: confirmationHeader

            width: parent.width - 128
            height: confirmationHeaderText.contentHeight

            anchors {
                top: parent.top
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Desktop.NormalText {
                id: confirmationHeaderText

                text: {
                    if (!popup.confirmationInfo || !popup.confirmationInfo.confirmation_email_masked) return util.insert(tr.verification_code_has_been_sent_to_company_email, [""])
                    return util.insert(tr.verification_code_has_been_sent_to_company_email, [util.join(popup.confirmationInfo.confirmation_email_masked, "")])
                }
                size: 16
                color: ui.colors.light3
                horizontalAlignment: Text.AlignHCenter

                anchors.fill: parent
            }
        }

        Item {
            id: confirmationTip

            width: parent.width - 48
            height: confirmationTipText.contentHeight

            anchors {
                top: confirmationHeader.bottom
                topMargin: 12
                horizontalCenter: parent.horizontalCenter
            }

            Desktop.NormalText {
                id: confirmationTipText

                text: tr.verification_code_new_company_description
                size: 12
                color: ui.colors.middle1
                textFormat: Text.RichText
                horizontalAlignment: Text.AlignHCenter
                onLinkActivated: Qt.openUrlExternally(link)

                anchors.fill: parent
            }
        }

        Item {
            id: confirmationFieldItem

            width: parent.width - 64
            height: 96

            anchors {
                top: confirmationTip.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextField {
                id: confirmationField

                width: parent.width
                errorColor: ui.colors.red1

                property var expectedLength: {
                    if (!popup.confirmationInfo || !popup.confirmationInfo.expected_token_length) return 6
                    return popup.confirmationInfo.expected_token_length
                }

                control {
                    height: 72
                    font.pixelSize: 32
                    font.letterSpacing: 16
                    horizontalAlignment: TextInput.AlignHCenter
                    maximumLength: confirmationField.expectedLength
                    validator: RegExpValidator { regExp: /[0-9A-Za-z]+/ }
                    color: confirmationField.valid ? ui.colors.white : ui.colors.red1
                }

                errorText {
                    font.pixelSize: 14
                    color: ui.colors.red1
                    horizontalAlignment: TextInput.AlignHCenter
                }

                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }
            }
        }

        Item {
            id: confirmationResend

            width: parent.width - 128
            height: confirmationResendText.contentHeight

            property var timeLeft: 0

            anchors {
                bottom: parent.bottom
                bottomMargin: 104
                horizontalCenter: parent.horizontalCenter
            }

            Desktop.NormalText {
                id: confirmationResendText

                text: confirmationResend.timeLeft > 0 ? util.insert(tr.we_can_resend_code, [util.format_timedelta_minutes(confirmationResend.timeLeft)]) : tr.resend_code
                color: confirmationResend.timeLeft > 0 ? ui.colors.middle4 : ui.colors.green1
                horizontalAlignment: Text.AlignHCenter

                anchors.fill: parent
            }

            Custom.HandMouseArea {
                enabled: confirmationResend.timeLeft <= 0

                onClicked: {
                    var settings = {"email": popup.confirmationInfo.email}
                    console.log(JSON.stringify(settings))
                    app.company_module.resend_new_email_confirmation(settings)
                }
            }

            Timer {
                repeat: true
                running: true
                interval: 500
                triggeredOnStart: true

                onTriggered: confirmationResend.timeLeft = popup.preset.timeDiff(popup.confirmationInfo.email)
            }
        }

        Item {
            width: parent.width - 64
            height: 48

            anchors {
                bottom: parent.bottom
                bottomMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Custom.Button {
                id: confirmEmailContinueButton

                width: parent.width
                text: tr.confirm
                textButton.textFormat: Text.PlainText
                loading_background_color: "transparent"

                enabledCustom: confirmationField.valid && confirmationField.control.acceptableInput && confirmationField.control.text.length == confirmationField.expectedLength

                anchors.centerIn: parent

                onClicked: {
                    confirmEmailContinueButton.forceActiveFocus()

                    popup.enabled = false
                    loading = true

                    var settings = {}
                    settings = {
                        "email": popup.confirmationInfo ? popup.confirmationInfo.email : "",
                        "email_token": confirmationField.control.text,
                    }
                    app.company_module.confirm_new_email(settings)
                }
            }
        }
    }

    Connections {
        target: app.company_module

        onConfirmNewEmailFailed: {
            popup.enabled = true
            confirmEmailContinueButton.loading = false

            if (tokenError) {
                confirmationField.valid = false
                confirmationField.error = tr.code_is_wrong
            }
        }

        onConfirmNewEmailSuccess: {
            popup.enabled = true
            confirmEmailContinueButton.loading = false

            popup.close()
        }

        onResendNewEmailConfirmationSuccess: {
            var date = new Date()
            popup.preset.sendCodesTime[confirmationInfoAlt.email] = date.getTime() + popup.preset.resendCodeTime
            popup.preset.sendCodesInfo[confirmationInfoAlt.email] = confirmationInfoAlt

            popup.confirmationInfo = confirmationInfoAlt
        }
    }
}
