import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var sideMargin: 24
    property var devEnable: true

    function checkWarnings() {
        warningText.visible = offlinePingsSlider.value * frameSlider.value >= 1200
            || offlinePingsSliderFibra.value * frameSlider.value >= 1200
    }

    Connections {
        target: app

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            frameSlider.value,
            offlinePingsSlider.value,
            offlinePingsSliderFibra.value
        ]
    }

    DS3.NavBarModal {
        id: jewellerSettingsBar

        headerText: hub.hub_type == "HUB_FIBRA" ? "Jeweller / Fibra" : "Jeweller"
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: contentView

        width: parent.width

        anchors {
            fill: undefined
            top: jewellerSettingsBar.bottom
            bottom: saveButton.top
        }

        padding: 24

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSliderValue {
                id: frameSlider

                title: tr.frame_length
                enabled: devEnable
                value: hub.frame_length
                from: 12
                to: {
                    if (hub.fire_interconnected && hub.hub_type == "HUB_2_PLUS") return 72
                    if (hub.fire_interconnected) return 48
                    return 300
                }
                stepSize: 12
                suffix: tr.sec

                onPressedChanged: if (!pressed) checkWarnings()
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            id: warningText

            width: parent.width

            Component.onCompleted: {
                checkWarnings()
            }

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            text: tr.jeweller_warning
        }

        DS3.Spacing {
            height: 8
            visible: warningText.visible
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.frame_length_hint
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: hub.hub_type == "HUB_FIBRA" ? 24 : 4
        }

        DS3.Text {
            width: parent.width

            text: tr.losses_before_marking_sensor_as_lost
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: hub.hub_type == "HUB_FIBRA"
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSliderValue {
                id: offlinePingsSlider

                title: hub.hub_type == "HUB_FIBRA" ? tr.packages_via_jeweller : tr.losses_before_marking_sensor_as_lost
                from: 3
                to: 60
                value: hub.lost_device_counter
                enabled: devEnable

                onPressedChanged: if (!pressed) checkWarnings()
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.losses_before_marking_sensor_as_lost_hint
            color: ui.ds3.figure.secondary
            visible: hub.hub_type != "HUB_FIBRA"
        }

        DS3.Spacing {
            height: 24
            visible: hub.hub_type == "HUB_FIBRA"
        }

        DS3.SettingsContainer {
            width: parent.width

            visible: hub.hub_type == "HUB_FIBRA"

            DS3.SettingsSliderValue {
                id: offlinePingsSliderFibra

                title: tr.packages_via_fibra
                enabled: devEnable
                value: hub.lost_fibra_counter
                from: 3
                to: 60

                onPressedChanged: if (!pressed) checkWarnings()
            }
        }

        DS3.Spacing {
            height: 4
            visible: hub.hub_type == "HUB_FIBRA"
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.losses_before_marking_sensor_as_lost_hint
            color: ui.ds3.figure.secondary
            visible: hub.hub_type == "HUB_FIBRA"
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            var settings = {
                "jeweller": {
                    "detector_ping_interval_seconds": frameSlider.value,
                    "lost_heartbeats_threshold": offlinePingsSlider.value,
                },
            }

            if (hub.hub_type == "HUB_FIBRA") {
                settings["lost_fibra_counter"] = offlinePingsSliderFibra.value
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
