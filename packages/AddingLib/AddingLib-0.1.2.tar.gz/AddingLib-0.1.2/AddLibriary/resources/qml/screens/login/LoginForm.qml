import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    width: 416
    height: parent.height
    anchors.left: parent.left

    property var debug_email_index: 0

    Custom.WindowsFuck {
        color: ui.colors.dark4
    }

    Custom.Button {
        id: ds3Btn

        width: 60
        height: 20

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 12
        }

        text: "DS3"
        color: ui.colors.nonessential

        visible: __debug__
        onClicked: {
            source = "qrc:/resources/qml/screens/ds/Main.qml"
        }
    }

    ColumnLayout {
        anchors.fill: parent

        Item {
            id: languageLayout
            Layout.minimumHeight: 72
            Layout.maximumHeight: 72
            Layout.minimumWidth: parent.width
            Layout.maximumWidth: parent.width
            Layout.alignment: Qt.AlignTop

            DS3.SettingsContainer {
                width: 192

                anchors {
                    top: parent.top
                    topMargin: 16
                    right: parent.right
                    rightMargin: 16
                }

                DS3.SettingsPickerTitleSecondary {
                    id: languageCombobox

                    model: tr.get_available_tr().languages
                    currentIndex: model.indexOf(tr.get_selected())

                    onCurrentIndexChanged: {
                        application.debug("login -> select lang -> " + languageCombobox.model[languageCombobox.currentIndex], false)
                        __ga__.report("activity", "login -> select lang")
                        tr.select_lang(currentIndex)
                    }
                }
            }
        }

        Item {
            id: iconLayout
            Layout.minimumHeight: 96
            Layout.maximumHeight: 96
            Layout.minimumWidth: 96
            Layout.maximumWidth: 96
            Layout.alignment: Qt.AlignHCenter

            Image {
                sourceSize.width: 96
                sourceSize.height: 96
                source: "qrc:/resources/images/icons/a-logo-pro.svg"
                anchors.centerIn: parent

                MouseArea {
                    id: environmentsArea

                    anchors.fill: parent
                    pressAndHoldInterval: 2000
                    onPressAndHold: {
                        servers.visible = !servers.visible
                    }

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: "login_environments_button"
                    Accessible.description: servers.visible ? "<button enabled=" + Accessible.checkable + ">" + "environments:open" + "</button>" : "<button enabled=" + Accessible.checkable + ">" + "environments:closed" + "</button>"
                    Accessible.role: Accessible.Button
                    Accessible.checkable: true
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        environmentsArea.pressAndHold(true)
                    }
                    /* ---------------------------------------------------- */
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "login_logo_image"
                Accessible.description: source
                Accessible.role: Accessible.Graphic
                /* ------------------------------------------------ */
            }

            Custom.ComboBox {
                id: servers
                width: parent.width
                height: 40
                visible: false
                copyVisible: false
                model: [
                    "RELEASE",
                    "STAGE-A",
                    "STAGE-B",
                    "STAGE-C",
                    "STAGE-D",
                    "STAGE-E",
                    "AT",
                    "RU",
                    "CUSTOM"
                ]

                onActivated: {
                    servers.visible = false
                    settings.server = currentText
                }

                Component.onCompleted: {
                    console.log(settings)

                    if (settings.server != "CUSTOM") {
                        console.log(settings.server)
                    } else {
                        console.log(settings.server, settings.server_address)
                    }

                    if (__build__ == "at") {
                        currentIndex = model.indexOf("AT")
                    }

                    if (settings.server == "STAGE") {
                        currentIndex = model.indexOf("STAGE-C")
                    } else {
                        currentIndex = model.indexOf(settings.server)
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleItemNamePrefix: "login_environments_button"

                Accessible.name: "login_environments_dropdown"
                Accessible.description: currentText
                Accessible.role: Accessible.ComboBox
                Accessible.checkable: servers.visible
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    servers.popup.open()
                }
                /* ---------------------------------------------------- */
            }

            Item {
                id: letterP
                width: 12
                height: 16
                anchors {
                    left: parent.left
                    leftMargin: 26
                    bottom: parent.bottom
                    bottomMargin: 24
                }

                Custom.HandMouseArea {
                    cursorShape: Qt.ArrowCursor
                    pressAndHoldInterval: 3000
                    onPressAndHold: {
                        Popups.easter_egg_popup()
                    }
                }
            }
        }

        Item {
            id: serverInput
            visible: servers.currentText == "CUSTOM"
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30
            Layout.minimumWidth: parent.width - 128
            Layout.maximumWidth: parent.width - 128
            Layout.alignment: Qt.AlignHCenter

            Custom.TextField {
                id: input
                width: parent.width - 50
                height: 50
                placeHolderText: "host:port"
                control.text: settings.server_address

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_custom_field"
                Accessible.description: control.text ? control.text : "<placeholder>" + placeHolderText + "</placeholder>"
                Accessible.role: Accessible.EditableText
                Accessible.editable: visible && enabled
                /* ---------------------------------------------------- */
            }

            Image {
                id: serverImage
                sourceSize.width: 40
                sourceSize.height: 40
                source: selected ? "qrc:/resources/images/icons/a-selected-bage-green.svg" : "qrc:/resources/images/icons/a-unselected-badge.svg"
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }

                property var selected: settings.server_address == input.control.text && input.control.text != ""

                Custom.HandMouseArea {
                    id: customCheckboxArea

                    anchors.fill: parent

                    onClicked: {
                        settings.server_address = input.control.text
                        loginBtn.forceActiveFocus()
                    }

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: "login_custom_checkbox"
                    Accessible.description: serverImage.selected ? "checked:true" : "checked:false"
                    Accessible.role: Accessible.CheckBox
                    Accessible.checked: serverImage.selected
                    Accessible.checkable: visible && enabled
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        customCheckboxArea.clicked(true)
                    }
                    Accessible.onToggleAction: {
                        customCheckboxArea.clicked(true)
                    }
                    /* ---------------------------------------------------- */
                }
            }
        }

        Item {
            id: loginLayout
            Layout.minimumHeight: 288
            Layout.maximumHeight: 288
            Layout.minimumWidth: parent.width - 128
            Layout.maximumWidth: parent.width - 128
            Layout.alignment: Qt.AlignHCenter

            Custom.FontText {
                id: welcomeText
                width: parent.width
                height: 24
                text: tr.a911_hello
                color: ui.colors.light3
                font.pixelSize: 16
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors.top: parent.top

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_welcome_text"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ---------------------------------------------------- */
            }

            property var focusInput: true

            Custom.TextField {
                id: emailField
                width: parent.width
                color: ui.colors.dark2
                control.text: app.multisession ? "" : settings.email
                placeHolderText: tr.a911_mail

                anchors {
                    top: welcomeText.bottom
                    topMargin: 24
                }
                onValidChanged: {
                    if (valid && !passwordField.valid) {
                        passwordField.valid = true
                    }
                }

                control.onFocusChanged: {
                    if (control.focus) {
                        control.selectAll()
                    }
                    if (control.focus) loginButtomItem.loginFailed = false
                }

                Keys.onEnterPressed: {
                    if (!loginBtn.enabled) return
                    loginBtn.clicked()
                }

                Keys.onReturnPressed: {
                    if (!loginBtn.enabled) return
                    loginBtn.clicked()
                }

                Keys.onDownPressed: {
                    // develop only. Quick access to recenty used emails
                    if (__debug__) {
                        emailField.control.text = settings.debug_emails[debug_email_index]
                        debug_email_index = debug_email_index + 1
                        if (debug_email_index >= settings.debug_emails.length) {
                            debug_email_index = debug_email_index - settings.debug_emails.length
                        }
                    }
                }

                Keys.onUpPressed: {
                    if (__debug__) {
                        emailField.control.text = settings.debug_emails[debug_email_index]
                        debug_email_index = debug_email_index - 1
                        if (debug_email_index == -1) {
                            debug_email_index = debug_email_index + settings.debug_emails.length
                        }
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_email_field"
                Accessible.description: control.text ? control.text : "<placeholder>" + placeHolderText + "</placeholder>"
                Accessible.role: Accessible.EditableText
                Accessible.editable: visible && enabled
                /* ---------------------------------------------------- */
            }

            Custom.TextField {
                id: passwordField
                width: parent.width
                color: ui.colors.dark2
                control.text: __debug__ && !__empty_password_field__ ? "qwe" : ""
                placeHolderText: tr.password
                control.echoMode: TextInput.Password

                anchors {
                    top: emailField.bottom
                    topMargin: 16
                }
                onValidChanged: {
                    if (valid && !emailField.valid) {
                        emailField.valid = true
                    }
                }

                control.onFocusChanged: {
                    if (control.focus) {
                        control.selectAll()
                    }
                    if (control.focus) loginButtomItem.loginFailed = false
                }

                Keys.onEnterPressed: {
                    if (!loginBtn.enabled) return
                    loginBtn.clicked()
                }

                Keys.onReturnPressed: {
                    if (!loginBtn.enabled) return
                    loginBtn.clicked()
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_password_field"
                Accessible.description: control.text ? control.text : "<placeholder>" + placeHolderText + "</placeholder>"
                Accessible.role: Accessible.EditableText
                Accessible.editable: visible && enabled
                /* ---------------------------------------------------- */
            }

            Item {
                id: loginButtomItem
                width: parent.width
                height: 48
                anchors {
                    top: passwordField.bottom
                    topMargin: 24
                }

                property var loginFailed: false

                Connections {
                    target: app.login_module
                    onLoginFailed: {
                        loginButtomItem.loginFailed = true
                        emailField.control.focus = false
                        passwordField.control.focus = false
                        emailField.valid = false
                        passwordField.valid = false
                    }
                }
                Custom.Button {
                    id: loginBtn
                    width: parent.width
                    text: tr.log_in
                    enabled: emailField.control.text != "" && passwordField.control.text != ""
                    anchors.centerIn: parent
                    visible: !loginButtomItem.loginFailed || emailField.control.focus || passwordField.control.focus
                    onClicked: {
                        application.debug("login -> login")
                        application.waitPopup()
                        app.login_module.login(emailField.control.text.trim(), passwordField.control.text)
                    }

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: "login_login_button"
                    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                    Accessible.role: Accessible.Button
                    Accessible.checkable: visible && enabled
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        loginBtn.clicked(true)
                    }
                    /* ---------------------------------------------------- */
                }

                Custom.FontText {
                    text: tr.Login_bad_credentials0
                    anchors.centerIn: parent
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    color: ui.colors.red1
                    visible: loginButtomItem.loginFailed && !emailField.control.focus && !passwordField.control.focus
                }
            }

            DS3.Text {
                id: iAgreeText

                width: parent.width

                anchors {
                    top: loginButtomItem.bottom
                    topMargin: 6
                }

                visible: __policies_checker_features__
                horizontalAlignment: Text.AlignHCenter
                text: tr.agree_all_updates_loggin_desktop
                style: ui.ds3.text.body.SRegular
                color: ui.ds3.figure.secondary

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_policies_text"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ---------------------------------------------------- */
            }

            Rectangle {
                id: firstLine

                width: parent.width
                height: 1

                anchors {
                    top: iAgreeText.bottom
                    topMargin: 12
                }

                color: ui.ds3.bg.highest
            }

            Custom.FontText {
                id: regText

                width: parent.width * 0.6
                height: 32
                text: tr.a911_create_pro_account
                color: ui.colors.green1
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignLeft
                anchors {
                    top: firstLine.bottom
                    topMargin: 16
                    left: parent.left
                }

                Custom.HandMouseArea {
                    id: registrationButton

                    onClicked: {
                        application.debug("login -> sign up popup")
                        Popups.sign_up_popup()
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_registration_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    registrationButton.clicked(true)
                }
                /* ---------------------------------------------------- */
            }

            Connections {
                target: app.login_module
                onIsNotConfirmed: {
                    Popups.sign_up_popup(1, user.user_info.email, user.user_info.phone)
                }
            }

            Custom.FontText {
                id: forgotText

                width: parent.width * 0.4
                height: 32

                anchors {
                    top: firstLine.bottom
                    topMargin: 16
                    right: parent.right
                }

                text: tr.forgot_password
                color: ui.colors.light3
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight

                Custom.HandMouseArea {
                    id: forgotPasswordArea

                    onClicked: {
                        application.debug("login -> change password popup")
                        Popups.password_change_popup()
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_forgot-password_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    forgotPasswordArea.clicked(true)
                }
                /* ---------------------------------------------------- */
            }
        }

        Item {
            id: additionalLayout
            Layout.minimumHeight: 160
            Layout.maximumHeight: 160
            Layout.minimumWidth: parent.width - 128
            Layout.maximumWidth: parent.width - 128
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter

            Rectangle {
                id: secondLine

                width: parent.width
                height: 1

//                color: ui.ds3.bg.highest
                color: ui.colors.dark1
                anchors.top: parent.top
            }

            Custom.FontText {
                id: problemText

                width: parent.width
                height: 16

                anchors {
                    top: secondLine.bottom
                    topMargin: 16
                }

                text: tr.report_problem
                color: ui.colors.light3
                font.pixelSize: 12
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter

                Custom.HandMouseArea {
                    id: reportProblemArea

                    onClicked: {
                        application.debug("login -> report problem popup")
                        application.reportPopup({"userEmail": emailField.control.text})
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_report-problem_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    reportProblemArea.clicked(true)
                }
                /* ---------------------------------------------------- */
            }

            Rectangle {
                id: thirdLine

                width: parent.width
                height: 1

                anchors {
                    top: problemText.bottom
                    topMargin: 16
                }

                color: ui.colors.dark1
            }

            Custom.FontText {
                id: agreementText

                width: parent.width / 2
                height: 32

                anchors {
                    top: thirdLine.bottom
                    topMargin: 16
                    left: parent.left
                }

                text: "<a href=''>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.middle3) + "</a>"
                color: ui.colors.middle3
                font.pixelSize: 12
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignLeft

                Custom.HandMouseArea {
                    id: agreementArea

                    onClicked: {
                        application.debug("login -> agreement")

                        var locale = tr.get_locale()
                        locale = locale == "uk" ? "ua" : locale
                        locale = locale == "pt_PT" ? "pt" : locale
                        if (!["ru", "ua", "es", "it", "fr", "de", "nl", "pl", "pt"].includes(locale)) {
                            locale = "en"
                        }
                        var link = "https://ajax.systems/" + locale + "/ajax-pro-agreement/"
                        Qt.openUrlExternally(link)
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_agreement_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    agreementArea.clicked(true)
                }
                /* ---------------------------------------------------- */
            }

            Custom.FontText {
                id: privacyText

                width: parent.width / 2
                height: 32

                anchors {
                    top: thirdLine.bottom
                    topMargin: 16
                    right: parent.right
                }

                text: "<a href=''>" + tr.a911_privacy_policy + "</a>"
                color: ui.colors.middle3
                font.pixelSize: 12
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight

                Custom.HandMouseArea {
                    id: privacyArea

                    onClicked: {
                        application.debug("login -> privacy")

                        var locale = tr.get_locale()
                        locale = locale == "uk" ? "ua" : locale
                        locale = locale == "pt_PT" ? "pt" : locale
                        if (!["ru", "ua", "es", "it", "fr", "de", "nl", "pl", "pt"].includes(locale)) {
                            locale = "en"
                        }
                        var link = "https://ajax.systems/" + locale + "/privacy-policy/"
                        Qt.openUrlExternally(link)
                    }
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_privacy_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    privacyArea.clicked(true)
                }
                /* ---------------------------------------------------- */
            }

            Custom.FontText {
                id: versionText

                width: parent.width

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                color: ui.colors.middle3
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter

                text: {
                    var buildMode = ""
                    if (__build__ == "cbt") {
                        buildMode = "CBT v "
                    } else if (__build__ == "pbt") {
                        buildMode = "PBT v "
                    } else if (__build__ == "obt") {
                        buildMode = "OBT v "
                    } else if (__build__ == "qa") {
                        buildMode = "QA v "
                    } else if (__build__ == "at") {
                        buildMode = "AlphaTrack v "
                    } else {
                        buildMode = "v "
                    }

                    return buildMode + __version__
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "login_version_text"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ---------------------------------------------------- */
            }
        }
    }
}
