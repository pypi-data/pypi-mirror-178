import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/popups/user_settings/"
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    function close_settings_popup(params) {popup.close()}

    Connections {
        target: application

        onGoToChangePasswordSignal: {
            stackLayout.currentIndex = 0
        }

        onGoToSecurityTabAndOpenSessionsPopupSignal: {
            stackLayout.currentIndex = 1
            app.security_module.get_sessions()
        }
    }

    width: 875
    height: maxPopupHeight

    modal: true
    focus: true
    parent: ApplicationWindow.contentItem
    objectName: "userSettingsPopup"
    closePolicy: Popup.CloseOnEscape
    sideMargins: 0
    header: DS3.NavBarModal {
        headerText: tr.a911_profile_settings
    }
    footer: Item {}

    Row {
        width: parent.width
        height: popup.height - headerItem.height

        Rectangle {
            width: 375
            height: parent.height

            color: ui.ds3.bg.low

            DS3.SettingsContainer {
                width: parent.width - 48

                anchors {
                    top: parent.top
                    topMargin: 24
                    horizontalCenter: parent.horizontalCenter
                }

                DS3.SettingsNavigationTitlePrimary {
                    title: tr.a911_general
                    icon: "qrc:/resources/images/Athena/user_settings/GeneralSettings-L.svg"
                    color: stackLayout.currentIndex == 0 ? ui.ds3.special.selection : ui.ds3.bg.highest

                    onEntered: {
                        stackLayout.currentIndex = 0
                    }
                }
                DS3.SettingsNavigationTitlePrimary {
                    title: tr.account_security
                    icon: "qrc:/resources/images/Athena/user_settings/AccountSecuritySettings-L.svg"
                    color: stackLayout.currentIndex == 1 ? ui.ds3.special.selection : ui.ds3.bg.highest

                    onEntered: {
                        stackLayout.currentIndex = 1
                    }
                }
                DS3.SettingsNavigationTitlePrimary {
                    title: tr.a911_access
                    icon: "qrc:/resources/images/Athena/user_settings/CompaniesAndRolesSettings-L.svg"
                    color: stackLayout.currentIndex == 2 ? ui.ds3.special.selection : ui.ds3.bg.highest

                    onEntered: {
                        stackLayout.currentIndex = 2
                    }
                }
                DS3.SettingsNavigationTitlePrimary {
                    title: tr.app_settings
                    icon: "qrc:/resources/images/Athena/user_settings/AppSettings-L.svg"
                    color: stackLayout.currentIndex == 3 ? ui.ds3.special.selection : ui.ds3.bg.highest

                    onEntered: {
                        stackLayout.currentIndex = 3
                    }
                }
            }
        }

        Rectangle {
            width: 500
            height: parent.height

            color: ui.ds3.bg.base

            StackLayout {
                id: stackLayout

                anchors {
                    fill: parent
                    topMargin: 1
                }

                currentIndex: 0

                Common {}
                Security {}
                Access {}
                SystemSettings {}
            }
        }
    }
}

