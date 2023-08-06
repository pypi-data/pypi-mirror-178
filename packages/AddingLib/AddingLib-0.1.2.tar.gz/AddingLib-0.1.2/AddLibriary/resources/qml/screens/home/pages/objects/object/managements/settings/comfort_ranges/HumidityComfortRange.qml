import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    height: 500

    title: tr.humidity_lq_value
    sidePadding: 24

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            settingsSlider.firstValue,
            settingsSlider.secondValue
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.SettingsDualSlider {
            id: settingsSlider

            title: tr.air_monitor_humidity_title
            from: 0
            to: 100
            stepSize: 5
            firstValue: device.min_comfort_humidity
            secondValue: device.max_comfort_humidity
            atomSlider {
                suffix: "%"
                minText: "0"
                maxText: "100"
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.air_monitor_humidity_descr
    }

    footer: DS3.ButtonBar {
        enabled: changesChecker.hasChanges

        buttonText: tr.save
        button.onClicked: {
            const payload = {}

            payload["min_comfort_humidity"] = settingsSlider.firstValue
            payload["max_comfort_humidity"] = settingsSlider.secondValue
            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, payload)
            goBack()
        }
    }
}
