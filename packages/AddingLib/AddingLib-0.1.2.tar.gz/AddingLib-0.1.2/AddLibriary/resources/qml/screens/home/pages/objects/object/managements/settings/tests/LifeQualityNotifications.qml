import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    title: tr.notifications
    sidePadding: 24

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            accelerationAware.checked,
            temperature.checked,
            humidity.checked,
            co2.checked
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        titleComponent.text: tr.notifications_lightswitch_title
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        enabled: devEnable

        Settings.AccelerationAware {
            id: accelerationAware
        }
    }

    DS3.Comment {
        text: tr.get_notified_if_moved_lq_descr
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        isBgTransparent: true
        isCaps: true
        forceTextToLeft: true
        text: tr.air_quality_change_notif_title
    }

    DS3.SettingsContainer {
        width: parent.width

        enabled: devEnable

        DS3.SettingsSwitch {
            id: temperature

            title: tr.temperature_lq_notif
            checked: device.event_type.includes("TEMPERATURE")
        }

        DS3.SettingsSwitch {
            id: humidity

            title: tr.humidity_lq_notif
            checked: device.event_type.includes("HUMIDITY")
        }

        DS3.SettingsSwitch {
            id: co2

            title: tr.co_level_lq_notif
            checked: device.event_type.includes("CO2")
        }
    }

    DS3.Comment {
        text: tr.air_quality_change_notif_descr
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        hasBackground: true
        button.text: tr.save
        enabled: changesChecker.hasChanges

        button.onClicked: {
            var settings = {
                "acceleration_aware": accelerationAware.checked ? "ACCELERATION_IS_ACTIVE" : "ACCELERATION_NOT_ACTIVE",
                "event_type": []
            }

            if (temperature.checked) settings.event_type.push("TEMPERATURE")
            if (humidity.checked) settings.event_type.push("HUMIDITY")
            if (co2.checked) settings.event_type.push("CO2")

            Popups.waitPopup(device.dataChanged_, goBack)
            app.hub_management_module.apply_update(management, device, settings)
        }
    }
}