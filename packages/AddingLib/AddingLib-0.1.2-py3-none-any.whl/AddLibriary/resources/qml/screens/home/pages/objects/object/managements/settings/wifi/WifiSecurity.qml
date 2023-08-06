import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var sideMargin: 24
    property var security_text: null

    function current_field(field) {
        open.checked = false
        wep.checked = false
        wpa.checked = false
        wpa_2.checked = false
        wpa_wpa2.checked = false
        field.checked = true
    }

    anchors.fill: parent

    color: ui.ds3.bg.base
    radius: 12

    DS3.NavBarModal {
        id: networkSettingsBar

        headerText: tr.network_settings
        showBackArrow: true

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/SelectWifiNetworkAdvancedPopup.qml")
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: networkSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSingleSelection {
                id: open

                atomTitle.title: tr.open
                checked: true
                switchChecked: () => {
                    current_field(open)
                }
            }

            DS3.SettingsSingleSelection {
                id: wep

                atomTitle.title: tr.wep
                switchChecked: () => {
                    current_field(wep)
                }
            }

            DS3.SettingsSingleSelection {
                id: wpa

                atomTitle.title: tr.wpa
                switchChecked: () => {
                    current_field(wpa)
                }
            }

            DS3.SettingsSingleSelection {
                id: wpa_2

                atomTitle.title: tr.wpa_2
                switchChecked: () => {
                    current_field(wpa_2)
                }
            }

            DS3.SettingsSingleSelection {
                id: wpa_wpa2

                atomTitle.title: tr.wpa_wpa2
                switchChecked: () => {
                    current_field(wpa_wpa2)
                }
            }
        }
    }

    DS3.ButtonContained {
        id: saveButton

        width: parent.width - sideMargin * 2

        anchors {
            bottom: parent.bottom
            bottomMargin: sideMargin
            horizontalCenter: parent.horizontalCenter
        }

        text: tr.save

        onClicked: {
            if (open.checked) security_text = open.atomTitle.title
            if (wep.checked) security_text = wep.atomTitle.title
            if (wpa.checked) security_text = wpa.atomTitle.title
            if (wpa_2.checked) security_text = wpa_2.atomTitle.title
            if (wpa_wpa2.checked) security_text = wpa_wpa2.atomTitle.title
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/SelectWifiNetworkAdvancedPopup.qml", {"security_text": security_text})
        }
    }
}