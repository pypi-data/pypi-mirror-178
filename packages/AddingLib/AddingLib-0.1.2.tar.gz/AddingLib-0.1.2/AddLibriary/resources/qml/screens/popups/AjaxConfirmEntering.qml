import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups

AjaxPopup {
    id: popup

    property var session: null
    property var twoFactorAuthentificationOn: false

    Component.onCompleted: {
        app.security_module.get_sessions()
        app.security_module.get_two_fa_state()
    }

    Connections {
        target: app.security_module

        onTwoFaStateSignal: {
            twoFactorAuthentificationOn = state == "ENABLED"
        }
        onSessionKilledSuccess: {
            app.security_module.get_sessions()
            popup.close()
        }
    }

    Connections {
        target: app.login_module

        onLoginFailed: {
            popup.close()
        }
        onLogoutSignal: {
            popup.close()
        }
    }

    width: 320
    height: closeItem.height + textLabel.contentHeight + buttonGroup.height + 36

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

            anchors.right: parent.right

            radius: parent.radius
            title: tr.login_session_message

            closeArea.onClicked: {
                popup.close()
            }
        }

        Rectangle {
            width: parent.width
            height: 1

            anchors.top: closeItem.bottom

            color: ui.ds3.bg.low
        }

        Text {
            id: textLabel

            width: parent.width - 32

            anchors {
                top: closeItem.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            text: {
                var label = ""

                if (session.application_label != "n/a") {
                    label = util.label_correct(session.application_label)
                }
                if (session.client_version_major != "n/a") {
                    label += ` ${session.client_version_major}`
                }
                if (session.client_os != "n/a") {
                    label += ` ${session.client_os}`
                }
                if (session.client_device_model != "n/a") {
                    label += ` ${session.client_device_model}`
                }
                if (session.last_connection_ip != "n/a") {
                    label += ` ${session.last_connection_ip}`
                }
                return twoFactorAuthentificationOn ? util.insert(tr.login_account_alert_info_without_link, [label]) : util.insert(tr.login_account_alert_info, [label])
            }

            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 14
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

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                color: ui.ds3.figure.base
                transparent: true
                text: tr.ok

                onClicked: {
                    popup.close()
                }
            }

            Custom.Button {
                id: nextButton

                width: 130
                height: 40

                anchors {
                    left: cancelButton.right
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                color: ui.colors.red2
                transparent: true
                text: session.legacy_session ? tr.go_to_sessions : tr.terminate_session

                onClicked: {
                    if (session.legacy_session) {
                        application.addUserSettingsPopup()
                        application.goToSecurityTabAndOpenSessionsPopupSignal()
                        popup.close()
                    } else {
                        app.security_module.kill_sessions([session.session_id], false)
                    }
                }
            }
        }
    }
}
