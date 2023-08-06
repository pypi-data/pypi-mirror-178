import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    height: 500

    title: tr.co_level_lq_value
    sidePadding: 24

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            settingsSlider.value
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.SettingsColorSlider {
            id: settingsSlider

            title: tr.air_monitor_co_title
            from: 400
            to: 2400
            value: device.max_comfort_co2
            stepSize: 100
            colorStops: ({
                0: ui.ds3.figure.positiveContrast,
                1200: ui.ds3.figure.warningContrast,
                1600: ui.ds3.figure.attention,
                2000: ui.ds3.figure.hazard
            })
            atomSlider {
                suffix: ` ${tr.ppm_co_level_value}`
                minText: "400"
                maxText: "2,4k"
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: settingsSlider.value > 1000 ? tr.air_monitor_co_decr_high : tr.air_monitor_co_decr_normal
    }

    footer: DS3.ButtonBar {
        enabled: changesChecker.hasChanges

        buttonText: tr.save
        button.onClicked: {
            const payload = {}

            payload["max_comfort_co2"] = settingsSlider.value
            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, payload)
            goBack()
        }
    }
}
