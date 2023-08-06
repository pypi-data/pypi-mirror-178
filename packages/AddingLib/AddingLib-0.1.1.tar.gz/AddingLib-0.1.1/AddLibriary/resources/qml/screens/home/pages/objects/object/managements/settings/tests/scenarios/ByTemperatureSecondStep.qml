import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
//  Parameters of slider for each indicator
    property var slidersParameters: [
        {
            from: Math.round(temperature_converter.new(-25, "metric").convert(
                settings.measure_system
            ).value / 2) * 2,
            to: Math.round(temperature_converter.new(60, "metric").convert(
                settings.measure_system
            ).value / 2) * 2,
            value: Math.round(temperature_converter.new(20, "metric").convert(
                settings.measure_system
            ).value / 2) * 2,
            stepSize: settings.measure_system == "imperial" ? 2 : 1,
            suffix: "°"
        }
    ]
//  Which scenario start condition (higher or lower than selected value)
    property int conditionIndex: !!scenario ? [
        "LOWER_THAN",
        "HIGHER_THAN"
    ].indexOf(scenario.threshold.condition) : 1
//  Threshold value for selected condition
    property int selectedValue: 0

    height: maxStepHeight

    title: tr.by_temperature_scenario_title
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        text: tr.parameter_value_scenario
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        Repeater {
            model: slidersParameters

            Column {
                id: slidersForParameter

                width: parent.width

                spacing: 1

                DS3.SettingsSingleSelection {
                    atomTitle.title: tr.value_higher_than_scenario
                    checked: conditionIndex == 1
                    switchChecked: () => conditionIndex = 1
                }

                DS3.SettingsSingleSelection {
                    atomTitle.title: tr.value_lower_than_scenario
                    checked: conditionIndex == 0
                    switchChecked: () => conditionIndex = 0
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        Repeater {
            model: slidersParameters

            Column {
                function selectValue(value) {
                    selectedValue = temperature_converter.new(
                        value, settings.measure_system
                    ).convert("metric").value
                }

                function loadValue() {
                    return settings.measure_system == "imperial"
                        ? Math.round(
                            temperature_converter.new(scenario.threshold.value, "metric", 1).convert("imperial").value / 2
                        ) * 2
                        : scenario.threshold.value
                }

                width: parent.width

                DS3.SettingsValueSlider {
                    id: higherThanSlider

                    Component.onCompleted: if (visible && !!scenario) value = loadValue()

                    visible: conditionIndex == 1
                    from: modelData.from
                    to: modelData.to
                    value: modelData.value
                    stepSize: modelData.stepSize
                    atomSlider.suffix: modelData.suffix

                    onValueChanged: if (visible) selectValue(value)
                }

                DS3.SettingsValueSlider {
                    id: lowerThanSlider

                    Component.onCompleted: if (visible && !!scenario) value = loadValue()

                    visible: conditionIndex == 0
                    from: modelData.from
                    to: modelData.to
                    value: modelData.value
                    stepSize: modelData.stepSize
                    atomSlider.suffix: modelData.suffix

                    onValueChanged: if (visible) selectValue(value)
                }
            }
        }
    }

    DS3.Comment {
        text: tr.by_temperature_descr_for_value
    }

    footer: DS3.ButtonBar {
        hasBackground: true
        button {
            text: tr.next

            onClicked: setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByAlarmSecondStep.qml",
                {title: tr.by_temperature_scenario_title}
            )
        }
    }
}
