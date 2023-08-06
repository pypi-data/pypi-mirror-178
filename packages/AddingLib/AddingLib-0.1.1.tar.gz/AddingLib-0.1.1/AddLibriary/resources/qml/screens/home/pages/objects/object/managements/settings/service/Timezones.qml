import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: timezonesItem

    property var service: true
    property var scenario: null
    property var selected: null
    property var todo: null
    property var sideMargin: 24
    property var timeZones: null

    Connections {
        target: app

        onAltActionSuccess: {
            timezoneLoader.setSource("")

            if (todo) todo()
        }
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: timezonesBar

        headerText: tr.hub_time_zone
        showCloseIcon: false
        isRound: false
        showBackArrow: true

        onBackAreaClicked: {
            timezoneLoader.setSource("")
        }
    }

    DS3.InputSearch {
        id: searchField

        Component.onDestruction: {
            timezones.filtered.set_filter("")
        }

        width: parent.width

        anchors.top: timezonesBar.bottom

        placeholder: tr.city_name_search_timezone
        withSpinner: true
        find: () => {
            timezones.filtered.set_filter(atomInput.text)
            if (atomInput.text.length) {
                currentZone.visible = currentZone.title.toLowerCase().includes(atomInput.text.toLowerCase())
            } else {
                currentZone.visible = service ? timezones.find(hub.hub_timezone).length : selected
            }
        }
    }

    DS3.ScrollView {
        id: scrollView

        anchors {
            fill: undefined
            top: searchField.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.current_timezone
            visible: currentZone.visible
        }

        DS3.Spacing {
            height: 4

            visible: currentZone.visible
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSingleSelection {
                id: currentZone

                visible: service ? timezones.find(hub.hub_timezone).length : selected
                checked: true
                atomTitle.title: selected ? timezones.find(selected) : !!timeZones ? timeZones.subtitle : ""

                DS3.MouseArea {
                    onClicked: {}
                }
            }
        }

        DS3.Spacing {
            height: 24

            visible: currentZone.visible
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.other_timezone_available
            visible: timezones.filtered.length && currentZone.visible
        }

        DS3.Spacing {
            height: 4
            visible: timezones.filtered.length && currentZone.visible
        }

        TimezonesView {
            id: timezonesView
        }
    }

    DS3.ButtonBar {
        id: saveButton

        height: visible ? 80 : 0

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        visible: selected

        button.onClicked: {
            var settings = {
                "_params": {
                    "alt_action_success": true,
                },
            }

            if (selected) {
                settings["time_zone"] = selected
            }

            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
