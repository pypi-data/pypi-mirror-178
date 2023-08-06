import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "signUpPopup"
    width: 552
    height: 648 + (newsletterToggleText.visible ? newsletterToggleText.height + 26 : 0)
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    property var stepAlt: 0
    property var userEmail: ""
    property var phoneNumber: ""

    onStepAltChanged: {
        if (stepAlt === 1) {
            listView.currentIndex = 1
            popup.width = 328
            popup.height = 480
        }
    }

    property var duration: 200
    property var tokenLength: 6
    property var data: new Object({email: "", phone_number: "", first_name: "", last_name: "", password: ""})

    anchors.centerIn: parent

    onOpened: {
        nameField.valueText.control.forceActiveFocus()
    }

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    PropertyAnimation {
        id: widthAnim
        target: popup
        duration: popup.duration
        property: "width"
    }

    PropertyAnimation {
        id: heightAnim
        target: popup
        duration: popup.duration
        property: "height"
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        property var currentStep: listView.currentIndex + 1

        Item {
            id: header
            width: parent.width
            height: 88

            Item {
                height: 56
                anchors {
                    top: parent.top
                    topMargin: 16
                    left: parent.left
                    leftMargin: 32
                    right: closeArea.left
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: listView.currentIndex < 2 ? body.currentStep + " " + tr.a911_of + " 2" : tr.a911_confirmation
                    value: tr.a911_creating_pro_account
                    distance: 12
                    keyText.opacity: 1
                    keyText.color: ui.colors.middle3
                    valueText.color: ui.colors.light3
                    anchors.verticalCenter: parent.verticalCenter

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    accessibleKeyName: "registration_page_text"
                    accessibleKeyDescription: key

                    accessibleValueName: "registration_title_text"
                    accessibleValueDescription: value
                    /* ---------------------------------------------------- */
                }
            }

            Item {
                id: closeArea
                width: 88
                height: parent.height
                anchors.right: parent.right
                visible: listView.currentIndex < 2

                Image {
                    id: closeIcon

                    source: "qrc:/resources/images/icons/a-delete-button.svg"
                    sourceSize.width: 40
                    sourceSize.height: 40
                    anchors.centerIn: parent

                    Custom.HandMouseArea {
                        id: closeHeaderArea
                        pressAndHoldInterval: 1000
                        onClicked: {
                            popup.close()
                        }

                        onPressAndHold: {
                            return
                            if (listView.currentIndex == 0) {
                                nameField.valueText.control.text = "Elon"
                                surnameField.valueText.control.text = "Musk"
                                emailField.valueText.control.text = "gofikac771@p5mail.com"
//                                phoneField.valueText.control.text = "+13472336099"
                                passwordField.valueText.control.text = "qweqwe12"
                                rePasswordField.valueText.control.text = "qweqwe12"
                                agreementToggle.checked = true
                                return

                                listView.currentIndex = 1
                                widthAnim.to = 328
                                heightAnim.to = 480
                                widthAnim.start()
                                heightAnim.start()
                                return
                            }

                            if (listView.currentIndex == 1) {
                                smsCodeField.valueText.control.text = "123456"
                                emailCodeField.valueText.control.text = "654321"

                                listView.currentIndex = 2
                                widthAnim.to = 328
                                heightAnim.to = 240
                                widthAnim.start()
                                heightAnim.start()
                                return
                            }

                            if (listView.currentIndex == 2) {
                                listView.currentIndex = 0
                                widthAnim.to = 552
                                heightAnim.to = 548
                                widthAnim.start()
                                heightAnim.start()
                                return
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_close_button"
                        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + closeIcon.source + "</button>"
                        Accessible.role: Accessible.Button
                        Accessible.checkable: visible && enabled
                        Accessible.onPressAction: {
                            if (!Accessible.checkable) return
                            closeHeaderArea.clicked(true)
                        }
                        /* ------------------------------------------------ */
                    }
                }
            }
        }

        Item {
            id: pages
            width: parent.width - 32
            anchors {
                top: header.bottom
                right: parent.right
                bottom: parent.bottom
                bottomMargin: 24
            }

            Connections {
                target: app.registration_module

                onRegistrationStepSuccess: {
                    if (step == 0) {
                        popup.tokenLength = info.token_length
                        listView.currentIndex = 1
                        widthAnim.to = 328
                        heightAnim.to = 480
                        widthAnim.start()
                        heightAnim.start()
                        return
                    }

                    if (step == 1) {
                        listView.currentIndex = 2
                        widthAnim.to = 328
                        heightAnim.to = 240
                        widthAnim.start()
                        heightAnim.start()
                        return
                    }

                    if (step == 2) {
                        listView.currentIndex = 0
                        widthAnim.to = 552
                        heightAnim.to = 548
                        widthAnim.start()
                        heightAnim.start()
                        return
                    }
                }
            }

            ListView {
                id: listView

                spacing: 32
                model: objectsModel
                interactive: false
                currentIndex: 0
                anchors.fill: parent

                orientation: Qt.Horizontal
                snapMode: ListView.SnapOneItem
                highlightMoveDuration: popup.duration
                highlightMoveVelocity: -1
                highlightRangeMode: ListView.StrictlyEnforceRange
            }

            ObjectModel {
                id: objectsModel

                Item {
                    width: pages.width
                    height: pages.height

                    Custom.TextFieldEdit {
                        id: nameField

                        width: parent.width / 2 - 24
                        key: tr.name
                        value: ""
                        distance: 12
                        anchors {
                            top: parent.top
                            topMargin: 12
                            left: parent.left
                        }
                        valueText.control.onTextChanged: {
                            valueText.control.text = util.validator(valueText.control.text, 24)
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_first-name_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_first-name_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.TextFieldEdit {
                        id: surnameField

                        width: parent.width / 2 - 24
                        key: tr.last_name
                        value: ""
                        distance: 12
                        anchors {
                            top: parent.top
                            topMargin: 12
                            right: parent.right
                            rightMargin: 32
                        }
                        valueText.control.onTextChanged: {
                            valueText.control.text = util.validator(valueText.control.text, 24)
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_last-name_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_last-name_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.TextFieldEdit {
                        id: emailField

                        width: parent.width - 32
                        key: tr.email
                        value: ""
                        distance: 12
                        anchors {
                            top: nameField.bottom
                            topMargin: 16
                            left: parent.left
                        }
                        valueText.control.validator: RegExpValidator { regExp: ui.regexes.email }

                        Connections {
                            target: app.registration_module

                            onRegistrationErrors: {
                                if (listView.currentIndex != 0) return
                                if (result["1"]) {
                                    emailField.valueText.valid = false
                                    emailField.valueText.error = result["1"].message
                                }
                            }
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_email_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_email_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.CountryPhones {
                        id: phoneField

                        width: parent.width

                        anchors {
                            top: emailField.bottom
                            topMargin: 16
                            left: parent.left
                        }

                        Connections {
                            target: app.registration_module

                            onRegistrationErrors: {
                                if (listView.currentIndex != 0) return
                                if (result["2"]) {
                                    phoneField.valueText.valid = false
                                    phoneField.valueText.error = result["2"].message
                                }
                            }
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_phone_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_phone_field"
                        accessibleValueDescription: phoneText
                        /* ------------------------------------------------ */
                    }

                    Rectangle {
                        id: firstLine

                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors {
                            top: phoneField.top
                            topMargin: 104
                        }
                    }

                    Custom.TextFieldEdit {
                        id: passwordField

                        width: parent.width / 2 - 24
                        key: tr.password
                        value: ""
                        valueText {
                            control {
                                echoMode: TextInput.Password
                                maximumLength: 300
                            }
                        }
                        distance: 12
                        anchors {
                            top: firstLine.bottom
                            topMargin: 24
                            left: parent.left
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_password_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_password_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.TextFieldEdit {
                        id: rePasswordField

                        width: parent.width / 2 - 24
                        key: tr.a911_confirm_password
                        value: ""
                        valueText.control.echoMode: TextInput.Password
                        distance: 12
                        anchors {
                            top: firstLine.bottom
                            topMargin: 24
                            right: parent.right
                            rightMargin: 32
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_repeat-password_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_repeat-password_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.FontText {
                        id: passwordText

                        visible: false
                        width: parent.width - 32
                        height: visible ? contentHeight : 0
                        text: tr.a911_password_requirements
                        color: ui.colors.middle4
                        font.pixelSize: 14
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                        anchors {
                            top: passwordField.bottom
                            topMargin: 0 // 20
                            left: parent.left
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }
                    }

                    Rectangle {
                        id: secondLine
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors {
                            top: passwordText.bottom
                            topMargin: 32
                        }
                    }

                    Custom.HandMouseArea {
                        height: agreementToggleText.height + 16
                        visible: agreementToggleText.hoveredLink != ""
                        anchors {
                            fill: undefined
                            top: secondLine.bottom
                            left: parent.left
                            right: parent.right
                        }
                    }

                    Custom.Toggle {
                        id: agreementToggle

                        anchors {
                            top: secondLine.bottom
                            topMargin: 20
                        }

                        mouseArea.onClicked: {
                            agreementToggle.checked = !agreementToggle.checked
                            firstButton.forceActiveFocus()
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_agreement_toggle"
                        Accessible.description: agreementToggle.checked ? "checked:true" : "checked:false"
                        Accessible.role: Accessible.CheckBox
                        Accessible.checked: agreementToggle.checked
                        Accessible.checkable: visible && enabled
                        Accessible.onPressAction: {
                            if (!Accessible.checkable) return
                            agreementToggle.clicked(true)
                        }
                        Accessible.onToggleAction: {
                            agreementToggle.clicked(true)
                        }
                        /* ------------------------------------------------ */
                    }

                    Custom.FontText {
                        id: agreementToggleText
                        width: parent.width - 96
                        height: contentHeight
                        text: tr.i_have_read_and_agree + ": " + "<a style='text-decoration:none' href='agreement'>" + util.colorize(tr.a911_terms_of_use, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='privacy'>" + util.colorize(tr.a911_privacy_policy, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='license'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.green1) + "</a>"
                        color: ui.colors.light3
                        lineHeight: 1.1
                        font.pixelSize: 12
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.Wrap
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        anchors {
                            top: secondLine.bottom
                            topMargin: 22
                            left: agreementToggle.right
                            leftMargin: 16
                        }

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        onLinkActivated: {
                            var locale = tr.get_locale()
                            locale = locale == "uk" ? "ua" : locale
                            locale = locale == "pt_PT" ? "pt" : locale
                            if (!["ru", "ua", "es", "it", "fr", "de", "nl", "pl", "pt"].includes(locale)) {
                                locale = "en"
                            }

                            if (link == "agreement") {
                                link = "https://ajax.systems/" + locale + "/end-user-agreement/"
                                Qt.openUrlExternally(link)
                                return
                            }

                            if (link == "privacy") {
                                link = "https://ajax.systems/" + locale + "/privacy-policy/"
                                Qt.openUrlExternally(link)
                                return
                            }

                            if (link == "license") {
                                link = "https://ajax.systems/" + locale + "/ajax-pro-agreement/"
                                Qt.openUrlExternally(link)
                                return
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_agreement_text"
                        Accessible.description: text
                        Accessible.role: Accessible.Paragraph
                        /* ------------------------------------------------ */
                    }

                    Custom.Toggle {
                        id: newsletterToggle

                        anchors {
                            top: agreementToggleText.bottom
                            topMargin: 24
                        }

                        mouseArea.onClicked: {
                            newsletterToggle.checked = !newsletterToggle.checked
                            firstButton.forceActiveFocus()
                        }

                        visible: __newsletter_features__
                    }

                    Custom.FontText {
                        id: newsletterToggleText

                        width: parent.width - 96
                        height: contentHeight

                         anchors {
                             top: agreementToggleText.bottom
                             topMargin: 26
                             left: newsletterToggle.right
                             leftMargin: 16
                        }

                        text: tr.i_agree_to_receive_updates
                        color: ui.colors.light3
                        lineHeight: 1.1
                        font.pixelSize: 12
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.Wrap
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        visible: __newsletter_features__

                        Keys.onReturnPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (firstButton.enabledCustom) {
                                firstButton.forceActiveFocus()
                                firstButton.clicked()
                            }
                        }
                    }

                    Item {
                        id: firstButtonItem
                        width: parent.width - 32
                        height: 48
                        anchors.bottom: parent.bottom

                        Custom.Button {
                            id: firstButton
                            width: parent.width
                            text: tr.next
                            enabledCustom: nameField.valueText.control.text &&
                                surnameField.valueText.control.text &&
                                emailField.valueText.control.text &&
                                phoneField.phoneText &&
                                phoneField.countryPhoneCombo.currentIndex != -1 &&
                                agreementToggle.checked &&
                                passwordField.valueText.control.text.trim() &&
                                rePasswordField.valueText.control.text

                            anchors.centerIn: parent

                            Keys.onReturnPressed: {
                                if (firstButton.enabledCustom) {
                                    firstButton.clicked()
                                }
                            }

                            Keys.onEnterPressed: {
                                if (firstButton.enabledCustom) {
                                    firstButton.clicked()
                                }
                            }

                            onClicked: {
                                firstButton.forceActiveFocus(true)
                                if (passwordField.valueText.control.text != rePasswordField.valueText.control.text) {
                                    rePasswordField.valueText.valid = false
                                    rePasswordField.valueText.error = tr.passwords_doesnt_match
                                    return
                                }

                                popup.data.email = emailField.valueText.control.text
                                popup.data.phone_number = phoneField.phoneText
                                popup.data.first_name = nameField.valueText.control.text
                                popup.data.last_name = surnameField.valueText.control.text
                                popup.data.password = passwordField.valueText.control.text

                                firstButton.loading = true
                                app.registration_module.register_user(popup.data)
                            }

                            Connections {
                                target: app.registration_module

                                onRegistrationStepSuccess: {
                                    firstButton.loading = false
                                }

                                onRegistrationErrors: {
                                    firstButton.loading = false
                                }
                            }

                            /* ---------------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "registration_request_button"
                            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                            Accessible.role: Accessible.Button
                            Accessible.checkable: visible && enabled
                            Accessible.onPressAction: {
                                if (!Accessible.checkable) return
                                firstButton.clicked(true)
                            }
                            /* ---------------------------------------------------- */
                        }
                    }
                }

                // -----------  second step ------------

                Item {
                    width: pages.width
                    height: pages.height

                    Custom.FontText {
                        id: codesText
                        width: parent.width - 32
                        height: contentHeight
                        text: tr.we_ve_sent_you_an_e_mail_sms_messages_containing_security_codes
                        color: ui.colors.middle4
                        font.pixelSize: 14
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                        anchors {
                            top: parent.top
                            topMargin: 8
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_codes_text"
                        Accessible.description: text
                        Accessible.role: Accessible.Paragraph
                        /* ------------------------------------------------ */
                    }

                    Custom.TextFieldEdit {
                        id: smsCodeField
                        width: parent.width - 32
                        key: tr.code_from_sms
                        value: ""
                        distance: 12
                        valueText.control.validator: RegExpValidator { regExp: /[0-9]+/ }
                        anchors {
                            top: codesText.bottom
                            topMargin: 24
                            left: parent.left
                        }

                        Keys.onReturnPressed: {
                            if (secondButton.enabledCustom) {
                                secondButton.forceActiveFocus()
                                secondButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (secondButton.enabledCustom) {
                                secondButton.forceActiveFocus()
                                secondButton.clicked()
                            }
                        }

                        valueText.control.onTextEdited: {
                            smsCodeField.valueText.control.text = util.validator(smsCodeField.valueText.control.text, popup.tokenLength)
                        }

                        Connections {
                            target: app.registration_module

                            onRegistrationErrors: {
                                if (listView.currentIndex != 1) return
                                if (result["error"]) {
                                    smsCodeField.valueText.valid = false
                                }
                                if (result["2"]) {
                                    smsCodeField.valueText.valid = false
                                }
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_sms-code_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_sms-code_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Custom.TextFieldEdit {
                        id: emailCodeField
                        width: parent.width - 32
                        key: tr.code_from_email
                        value: ""
                        distance: 12
                        valueText.control.validator: RegExpValidator { regExp: /[0-9]+/ }
                        anchors {
                            top: smsCodeField.bottom
                            topMargin: 16
                            left: parent.left
                        }

                        Keys.onReturnPressed: {
                            if (secondButton.enabledCustom) {
                                secondButton.forceActiveFocus()
                                secondButton.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (secondButton.enabledCustom) {
                                secondButton.forceActiveFocus()
                                secondButton.clicked()
                            }
                        }

                        valueText.control.onTextEdited: {
                            emailCodeField.valueText.control.text = util.validator(emailCodeField.valueText.control.text, popup.tokenLength)
                        }

                        Connections {
                            target: app.registration_module

                            onRegistrationErrors: {
                                if (listView.currentIndex != 1) return
                                if (result["error"]) {
                                    emailCodeField.valueText.valid = false
                                    emailCodeField.valueText.error = result["error"].message
                                }
                                if (result["3"]) {
                                    emailCodeField.valueText.valid = false
                                }
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleKeyName: "registration_email-code_text"
                        accessibleKeyDescription: key

                        accessibleValueName: "registration_email-code_field"
                        accessibleValueDescription: valueText.control.text
                        /* ------------------------------------------------ */
                    }

                    Rectangle {
                        id: thirdLine
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors {
                            top: emailCodeField.top
                            topMargin: 96
                        }
                    }

                    Custom.FontText {
                        id: sendCodesText
                        width: parent.width - 32
                        height: contentHeight
                        text: tr.resend
                        color: ui.colors.green1
                        font.pixelSize: 14
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignHCenter | Text.AlignVCenter
                        anchors {
                            top: thirdLine.bottom
                            topMargin: 28
                        }

                        Custom.HandMouseArea {
                            id: resendArea

                            anchors.fill: parent
                            onClicked: {
                                var data = {}
                                data["email"] = userEmail === "" ? popup.data.email : userEmail
                                data["phone_number"] = phoneNumber === "" ? popup.data.phone_number : phoneNumber

                                secondButton.loading = true
                                app.registration_module.resend_confirmation_registration_token(data)
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "registration_resend_button"
                            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + sendCodesText.text + "</button>"
                            Accessible.role: Accessible.Button
                            Accessible.checkable: visible && enabled
                            Accessible.onPressAction: {
                                if (!Accessible.checkable) return
                                resendArea.clicked(true)
                            }
                            /* -------------------------------------------- */
                        }
                    }

                    Item {
                        width: parent.width - 32
                        height: 48
                        anchors.bottom: parent.bottom

                        Custom.Button {
                            id: secondButton
                            width: parent.width
                            text: tr.continue_android
                            enabledCustom: smsCodeField.valueText.control.text.length == popup.tokenLength && emailCodeField.valueText.control.text.length == popup.tokenLength
                            anchors.centerIn: parent

                            Keys.onReturnPressed: {
                                if (secondButton.enabledCustom) {
                                    secondButton.clicked()
                                }
                            }

                            Keys.onEnterPressed: {
                                if (secondButton.enabledCustom) {
                                    secondButton.clicked()
                                }
                            }

                            onClicked: {
                                secondButton.forceActiveFocus(true)
                                var data = {}
                                data["email"] = userEmail === "" ? emailField.valueText.control.text.trim() : userEmail
                                data["phone_token"] = smsCodeField.valueText.control.text
                                data["email_token"] = emailCodeField.valueText.control.text

                                secondButton.loading = true
                                app.registration_module.confirm_registration(data)
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "registration_confirm_button"
                            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                            Accessible.role: Accessible.Button
                            Accessible.checkable: visible && enabled
                            Accessible.onPressAction: {
                                if (!Accessible.checkable) return
                                secondButton.clicked(true)
                            }
                            /* -------------------------------------------- */
                        }
                    }
                    Connections {
                        target: app.registration_module

                        onRegistrationStepSuccess: {
                            secondButton.loading = false
                        }

                        onRegistrationErrors: {
                            secondButton.loading = false
                        }
                    }
                }

                Item {
                    width: pages.width
                    height: pages.height

                    Image {
                        sourceSize.width: 24
                        sourceSize.height: 24
                        source: "qrc:/resources/images/icons/a-success-badge.svg"
                        anchors {
                            left: parent.left
                            top: parent.top
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_success_icon"
                        Accessible.description: source
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }

                    Custom.FontText {
                        width: parent.width - 80
                        height: contentHeight
                        text: tr.a911_successfuly_created_account
                        color: ui.colors.middle1
                        font.pixelSize: 12
                        font.weight: Font.Light
                        elide: Text.ElideRight
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                        anchors {
                            top: parent.top
                            topMargin: 6
                            left: parent.left
                            leftMargin: 40
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "registration_success_text"
                        Accessible.description: text
                        Accessible.role: Accessible.Paragraph
                        /* ------------------------------------------------ */
                    }

                    Rectangle {
                        id: fourthLine
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 72
                        }
                    }

                    Item {
                        width: parent.width - 32
                        height: 48
                        anchors.bottom: parent.bottom

                        Custom.Button {
                            id: thirdButton

                            width: parent.width
                            text: tr.continue_android
                            enabledCustom: true
                            anchors.centerIn: parent

                            onClicked: {
                                popup.close()
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "registration_success_button"
                            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                            Accessible.role: Accessible.Button
                            Accessible.checkable: visible && enabled
                            Accessible.onPressAction: {
                                if (!Accessible.checkable) return
                                thirdButton.clicked(true)
                            }
                            /* -------------------------------------------- */
                        }
                    }
                }
            }
        }
    }
}
