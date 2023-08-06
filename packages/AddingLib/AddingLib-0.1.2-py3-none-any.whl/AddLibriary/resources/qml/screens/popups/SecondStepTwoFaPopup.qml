import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12
import QtQml.Models 2.1

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: twoFaPopup

    width: 512
    height: pages.height

    closePolicy: Popup.CloseOnEscape

    property var duration: 200
    property var tokenLength: 6
    property var two_fa_secret: ""
    property var previousStep: listView.currentIndex - 1

    signal startLoadingQr()

    background: Rectangle {
        color: "transparent"
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

     PropertyAnimation {
        id: widthAnim
        target: twoFaPopup
        duration: twoFaPopup.duration
        property: "width"
    }

    PropertyAnimation {
        id: heightAnim
        target: twoFaPopup
        duration: twoFaPopup.duration
        property: "height"
    }

    Item {
        id: pages

        width: twoFaPopup.width
        height: {
            if (listView.currentIndex == 0) {
                return secondStep.height
            } else {
                return thirdPopup.height
            }
        }

        Connections {
            target: listView

            onCurrentIndexChanged: {

                if (listView.currentIndex == 0) {
                    widthAnim.to = 512
                    heightAnim.to = twoFaPopup.height
                    widthAnim.start()
                    heightAnim.start()
                    app.security_module.get_secret()
                    return
                }

                if (listView.currentIndex == 1) {
                    widthAnim.to = 440
                    heightAnim.to = thirdPopup.height
                    verificationCodeField.forceActiveFocus()
                    widthAnim.start()
                    heightAnim.start()
                    qrCodeImage.qrCodeUrl = ""
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
            clip: true

            orientation: Qt.Horizontal
            snapMode: ListView.SnapOneItem
            highlightMoveDuration: twoFaPopup.duration
            highlightMoveVelocity: -1
            highlightRangeMode: ListView.StrictlyEnforceRange
        }

        ObjectModel {
            id: objectsModel

            Rectangle {
                id: secondStep

                width: pages.width
                height: {
                    if (740 > application.height) {
                        return maxPopupHeight
                    }
                    return 740
                }

                Connections {
                    target: application
                    onHeightChanged: {
                        if (twoFaPopup.height < 740) {
                            twoFaPopup.height = maxPopupHeight
                        } else if (twoFaPopup.height > maxPopupHeight) {
                            twoFaPopup.height = maxPopupHeight
                            return
                        } else {
                            twoFaPopup.height = 740
                            return
                        }
                    }
                }

                color: ui.colors.dark3
                radius: 8

                focus: true

                Keys.onEnterPressed: {
                    save.clicked(true)
                }

                Keys.onReturnPressed: {
                    save.clicked(true)
                }

                Item {
                    id: secondHeaderItem

                    width: parent.width
                    height: 64

                    anchors.top: parent.top

                    Image {
                        sourceSize.width: 24
                        sourceSize.height: 24

                        source: "qrc:/resources/images/icons/back.svg"

                        anchors {
                            left: parent.left
                            leftMargin: 32
                            verticalCenter: parent.verticalCenter
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor

                            onClicked: {
                                twoFaPopup.close()
                            }
                        }
                    }

                    Custom.PopupHeader {
                        width: parent.width - 56
                        height: 64
                        radius: parent.radius
                        title: tr.warning

                        anchors.right: parent.right

                        closeArea.onClicked: {
                            twoFaPopup.close()
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 1
                    color: ui.colors.dark4
                    anchors.top: secondHeaderItem.bottom
                }

                ScrollView {
                    id: scrollView

                    width: parent.width
                    clip: true

                    anchors {
                        top: secondHeaderItem.bottom
                        topMargin: 16
                        left: parent.left
                        leftMargin: 32
                        bottom: okayButton.top
                        bottomMargin: 24
                    }

                    ScrollBar.vertical: ScrollBar {
                        id: control
                        policy: {
                            if (scrollView.height < scrollView.contentHeight) {
                                return ScrollBar.AlwaysOn
                            }
                            return ScrollBar.AlwaysOff
                        }
                        anchors.top: parent.top
                        anchors.right: scrollView.right
                        anchors.rightMargin: 34
                        anchors.bottom: parent.bottom

                        contentItem: Rectangle {
                            implicitWidth: 2
                            implicitHeight: 100
                            radius: width / 2
                            color: control.pressed ? "#81e889" : "#9e9e9e"
                            opacity: 0.6
                        }

                        background: Rectangle {
                            implicitWidth: 2
                            implicitHeight: 100
                            color: "#575757"
                        }
                    }

                    Column {
                        width: scrollView.width - 64
                        spacing: 16

                        Text {
                            id: contentHeader

                            width: parent.width
                            height: contentHeight
                            text: tr.t_factor_authentication
                            color: ui.colors.light3
                            font.family: roboto.name
                            font.pixelSize: 16
                            wrapMode: Text.WordWrap
                            opacity: 1.0
                        }

                        Text {
                            id: descriptionText

                            width: parent.width
                            height: contentHeight
                            text: tr.desktop_2fa_protect_account
                            color: "#6d7278"
                            font.family: roboto.name
                            font.pixelSize: 12
                            lineHeight: 1.43
                            wrapMode: Text.WordWrap
                        }

                        Text {
                            id: appSettingsText

                            width: parent.width
                            height: contentHeight
                            text: tr.desktop_2fa_link_app + ":"
                            color: ui.colors.light3
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.weight: Font.Bold
                            wrapMode: Text.WordWrap
                        }

                        Text {
                            id: downloadAppText

                            width: parent.width
                            height: contentHeight
                            text: util.insert(tr.desktop_2fa_download_authenticator, ["<font color=\"#5ae4aa\">App Store</font>", "<font color=\"#5ae4aa\">Google Play</font>"])
                            color: "#dbdbdb"
                            font.family: roboto.name
                            font.pixelSize: 14
                            lineHeight: 1.43
                            wrapMode: Text.WordWrap
                        }

                        Image {
                            id: qrCodeImage
                            property var qrCodeUrl: ""

//                            visible: qrCodeUrl

                            width: 120
                            height: 120
                            source: qrCodeUrl
                            anchors.horizontalCenter: parent.horizontalCenter

                            Custom.BlockLoading {
                                id: qrLoader
                                radius: 32
                                minTime: 200
                                customOpacity: 0.1
                                startSignals: [twoFaPopup.startLoadingQr]
                                stopSignals: [util.generateQrCodeSuccess, util.generateQrCodeFailed]
                                backgroundColor: ui.colors.dark3
                            }

                            Item {
                                id: loadingQrFailed

                                visible: false

                                anchors.fill: parent

                                Text {
                                    width: contentWidth > parent.width ? parent.width: contentWidth

                                    text: tr.error
                                    color: ui.colors.red1
                                    font.family: roboto.name
                                    font.pixelSize: 16
                                    font.weight: Font.Bold
                                    wrapMode: Text.Wrap

                                    anchors.centerIn: parent
                                }
                            }
                        }

                        Text {
                            id: secretCodeText

                            width: parent.width
                            height: contentHeight
                            text: tr.desktop_2fa_manual_verification + ":"
                            color: ui.colors.light3
                            font.family: roboto.name
                            font.pixelSize: 16
                            font.weight: Font.Bold
                            wrapMode: Text.WordWrap
                        }

                        Item {
                            width: parent.width
                            height: 16

                            Text {
                                id: secretCode

                                width: parent.width
                                height: contentHeight
                                text: {
                                    if (!two_fa_secret) return ""
                                    return two_fa_secret.match(/.{1,4}/g).join(" ")
                                }
                                color: "#dbdbdb"
                                font.family: roboto.name
                                font.pixelSize: 14
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter

                                anchors {
                                    horizontalCenter: parent.horizontalCenter
                                }
                            }

                             MouseArea {
                                anchors.fill: secretCode
                                hoverEnabled: true
                                onEntered: {
                                    secretCode.color = "#60e3ab"
                                }

                                onExited: {
                                    secretCode.color = "#dbdbdb"
                                }

                                onClicked: {
                                    util.set_clipboard_text(secretCode.text)
                                    if (!notifyAnim.running) notifyAnim.start()
                                }
                            }
                        }

                        Text {
                            id: secretAttention

                            width: parent.width
                            height: contentHeight + 24
                            text: tr.desktop_2fa_secret_code_pay_attention
                            color: ui.colors.light3
                            font.family: roboto.name
                            font.pixelSize: 14
                            lineHeight: 1.43
                            wrapMode: Text.WordWrap
                        }
                    }
                }


                Rectangle {
                    id: delimiterLine

                    width: parent.width - 64
                    height: 1

                    color: "#6d7278"
                    anchors {
                        top: scrollView.bottom
                        horizontalCenter: parent.horizontalCenter
                    }
                }

                Custom.Button {
                    id: okayButton

                    text: tr.desktop_2af_next
                    width: parent.width - 136
                    height: 40
                    transparent: true

                    anchors {
                        bottom: parent.bottom
                        bottomMargin: 24
                        horizontalCenter: parent.horizontalCenter
                    }

                    onClicked: {
                        listView.currentIndex = 1
                    }
                }

                SequentialAnimation {
                    id: notifyAnim
                    running: false

                    PropertyAnimation { target: newEventPopup; property: "y"; from: -200; to: 45; duration: 170 }
                    PropertyAnimation { target: newEventPopup; property: "y"; from: 45; to: 45; duration: 2300 }
                    PropertyAnimation { target: newEventPopup; property: "y"; from: 45; to: -200; duration: 170 }
                }

                Rectangle {
                    id: newEventPopup
                    color: "#373737"
                    opacity: 0.9
                    height: 32
                    width: newEventText.contentWidth + 30
                    radius: 16
                    x: (parent.width - width) / 2
                    y: -200

                    Text {
                        id: newEventText
                        text: tr.copied
                        font.family: roboto.name
                        font.pixelSize: 14
                        color: ui.colors.light1
                        anchors.centerIn: parent
                    }
                }
            }

//          ----------------------------- Last Popup -----------------------------
            Rectangle {
                id: thirdPopup

                width: pages.width
                height: 80 + item.height
                radius: 8
                color: ui.colors.dark3

                Item {
                    id: thirdHeaderItem

                    width: parent.width
                    height: 64

                    anchors.top: parent.top

                    Image {
                        id: thirdIconBack

                        sourceSize.width: 24
                        sourceSize.height: 24

                        source: "qrc:/resources/images/icons/back.svg"

                        anchors {
                            left: parent.left
                            leftMargin: 32
                            verticalCenter: parent.verticalCenter
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor

                            onEntered: thirdIconBack.opacity = 1.0
                            onExited: thirdIconBack.opacity = 0.9

                            onClicked: {
                                listView.currentIndex = previousStep
                                verificationCodeField.text = ""
                                errorText.text = ""
                            }
                        }
                    }

                    Custom.PopupHeader {
                        width: parent.width - 56
                        height: 64
                        radius: parent.radius
                        title: tr.desktop_2fa_enter_code

                        anchors.right: parent.right

                        closeArea.onClicked: {
                            twoFaPopup.close()
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 1
                    color: ui.colors.dark4
                    anchors.top: thirdHeaderItem.bottom
                }

                Item {
                    id: item

                    width: parent.width - 96
                    height: 16 + infoText.height + 24 + verificationCodeField.height + 3 + errorText.height + 16 + approveButton.height + 16
                    anchors {
                        top: thirdHeaderItem.bottom
                        topMargin: 24
                        horizontalCenter: parent.horizontalCenter

                    }

                    Text {
                        id: infoText

                        width: parent.width
                        height: contentHeight
                        text: tr.desktop_2fa_totp_explanation
                        color: "#6d7278"
                        font.family: roboto.name
                        font.pixelSize: 14
                        wrapMode: Text.WordWrap
                    }

                    AjaxTextField {
                        id: verificationCodeField

                        width: parent.width
                        placeHolderText: "XXX XXX"
                        text: ""
                        maximumLength: 7

                        anchors {
                            top: infoText.bottom
                            topMargin: 24
                       }

                        validator: RegExpValidator { regExp: /[0-9]{3} ?[0-9]{3}/ }
                        inputMethodHints: Qt.ImhDigitsOnly

                        onTextChanged: {
                            util.confirm_login_dash_insert(verificationCodeField.text, cursorPosition)
                        }

                        Connections {
                            target: util

                            onDashInsertResult: {
                                verificationCodeField.text = new_text
                                verificationCodeField.cursorPosition = position
                            }
                        }

                        Keys.onPressed: {
                            if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                                approveButton.clicked(true)
                                return
                            }
                        }

                        onActiveFocusChanged: {
                            if (errorText.text) {
                                errorText.text = ""
                            }
                        }
                    }
                    Text {
                        id: errorText
                        anchors {
                            top: verificationCodeField.bottom
                            topMargin: 3
                        }
                        width: parent.width
                        height: contentHeight
                        text: ""
                        color: ui.colors.red1
                        font.family: roboto.name
                        font.pixelSize: 14
                        wrapMode: Text.WordWrap
                    }

                    Custom.Button {
                        id: approveButton

                        text: tr.verify_code


                        width: parent.width - 128
                        height: 40

                        enabled: verificationCodeField.text.length < 7 ? false : true
                        color: enabled ? ui.colors.green1 : ui.colors.middle4
                        transparent: true
//                        buttonText.color: enabled ? "#fdfdfd" : ui.colors.middle4
                        anchors {
                            top: errorText.bottom
                            topMargin: 16
                            horizontalCenter: parent.horizontalCenter
                        }

                        onClicked: {
                            app.security_module.confirm_two_fa(verificationCodeField.text.replace(" ", ""))
                        }
                    }
                }
            }

            // here
        }
    }

    Component.onCompleted: {
        twoFaPopup.startLoadingQr()
    }

    Connections {
        target: util

        onGenerateQrCodeFailed: {
            loadingQrFailed.visible = true
        }

        onGenerateQrCodeSuccess: {
            qrCodeImage.qrCodeUrl = "data:image/png;base64," + imageData
        }
    }

    Connections {
        target: app.security_module

        onSecretTwoFaSignal: {
            two_fa_secret = secret
            util.thread_generate_qr(settings.email, two_fa_secret)
        }

        onConfirmTwoFaSuccess: {
            twoFaPopup.close()
            security.enableTwoFa.checked = true
            application.confirmedToFaSuccess()
        }

        onConfirmTwoFaFailed: {
            errorText.text = tr.desktop_2fa_wrong_code
            verificationCodeField.valid = false
            verificationCodeField.text = ""
        }
    }
}
