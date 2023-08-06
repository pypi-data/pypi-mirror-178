import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    height: 500

    title: tr.temperature
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

            title: tr.air_monitor_temperature_title
            from: settings.measure_system == "imperial" ? 32 : 0
            to: settings.measure_system == "imperial" ? 122 : 50
            stepSize: settings.measure_system == "imperial" ? 2 : 1
            firstValue: settings.measure_system == "imperial"
                ? Math.round((device.min_comfort_temperature * 9 / 5 + 32) / 2) * 2
                : device.min_comfort_temperature
            secondValue: settings.measure_system == "imperial"
                ? Math.round((device.max_comfort_temperature * 9 / 5 + 32) / 2) * 2
                : device.max_comfort_temperature
            atomSlider {
                suffix: settings.measure_system == "imperial" ? "°F" : "°C"
                minText: from
                maxText: to
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.air_monitor_temperature_descr
    }

    footer: DS3.ButtonBar {
        enabled: changesChecker.hasChanges
        buttonText: tr.save
        button.onClicked: {
            const payload = {}

            const minTemperature = settings.measure_system == "imperial"
                ? Number.parseInt(
                    temperature_converter.new(
                        settingsSlider.firstValue, settings.measure_system
                    ).convert("metric").value
                )
                : settingsSlider.firstValue
            const maxTemperature = settings.measure_system == "imperial"
                ? Number.parseInt(
                    temperature_converter.new(
                        settingsSlider.secondValue, settings.measure_system
                    ).convert("metric").value
                )
                : settingsSlider.secondValue

            payload["min_comfort_temperature"] = minTemperature
            payload["max_comfort_temperature"] = maxTemperature
            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, payload)
            goBack()
        }
    }
}
