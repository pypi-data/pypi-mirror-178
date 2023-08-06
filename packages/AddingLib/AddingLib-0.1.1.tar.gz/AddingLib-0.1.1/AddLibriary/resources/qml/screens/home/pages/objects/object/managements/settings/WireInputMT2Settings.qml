import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    id: popup

    property bool measuringInProgress: false
    property var wizardStorage: ({})
    function wizard_steps() {
        const path = 'qrc:/resources/qml/screens/home/pages/objects/object/popups/mtr2_wizard/'
        if (wizardStorage['eol_scheme'] == 'ONE_EOL') {
            return [
                [path + 'MeasureResistance.qml', 'measure_1'],
                [path + 'ResistanceMeasured.qml', 'measure_1'],
            ]
        }
        if (wizardStorage['eol_scheme'] == 'TWO_EOL') {
            return [
                [path + 'NC_NO_Select.qml', 'measure_2'],

                [path + 'MeasureResistance.qml', 'measure_1'],
                [path + 'ResistanceMeasured.qml', 'measure_1'],

                [path + 'MeasureResistance.qml', 'measure_2'],
                [path + 'ResistanceMeasured.qml', 'measure_2'],
            ]
        }
        if (wizardStorage['eol_scheme'] == 'THREE_EOL') {
            return [
                [path + 'NC_NO_Select.qml', 'measure_2'],
                [path + 'NC_NO_Select.qml', 'measure_3'],
                [path + 'S2_S3_binding.qml', 'measure_3'],

                [path + 'MeasureResistance.qml', 'measure_1'],
                [path + 'ResistanceMeasured.qml', 'measure_1'],

                [path + 'MeasureResistance.qml', 'measure_2'],
                [path + 'ResistanceMeasured.qml', 'measure_2'],

                [path + 'MeasureResistance.qml', 'measure_3'],
                [path + 'ResistanceMeasured.qml', 'measure_3'],
            ]
        }
    }

    closePolicy: {
        if (popup.child.hasChild &&
                popup.child.child !== null &&
                String(popup.child.child.parent.source).includes('popups/mtr2_wizard/')
            ) {
            return Popup.NoAutoClose
        } else {
            return Popup.CloseOnEscape
        }
    }
    header: DS3.NavBarModal {
        headerText: popup.title
        showBackArrow: popup.child.hasChild
        backArrowEnabled: !popup.measuringInProgress
        onBackAreaClicked: {
            goBack()
        }
        onClosed : () => {
            if (popup.child.hasChild &&
                    popup.child.child !== null &&
                    String(popup.child.child.parent.source).includes('popups/mtr2_wizard/')
                ) {
                Popups.cancel_wizard_popup(() => {popup.goBack(popup.currentStepIndex);})
            } else {
                popup.close()
            }
        }
    }


    Parts.CommonSettings {
        property var chimesSettings: {}

        property var defaultState: -1
        property var eventTypesWireMT2: [
            "BURGLARY_ALARM","FIRE_ALARM","MEDICAL_ALARM",
            "PANIC_ALARM","GAS_ALARM","TAMPER_ALARM","MALFUNCTION_ALARM",
            "LEAK_ALARM", "SERVICE_EVENT"
        ]
        property var wireMT2CustomAlarms: [
            tr.burglary_alarm, tr.fire_alarm, tr.medical_alarm,
            tr.panic_alarm, tr.gas_alarm, tr.tamper_alarm, tr.malfunction,
            tr.leakage_alarm, tr.custom_not_alarm_mtr
        ]
        property var wireMT2CustomAlarmWithPreset: [
            tr.fire_alarm, tr.gas_alarm, tr.medical_alarm,
             tr.panic_alarm, tr.malfunction, tr.leakage_alarm
        ]

        function apply_calculated_resistance(data) {
            // // Response
            // message CalculatedResistancesDetails {
            //     // All resistances are measured in hundreds of Ohms
            //     google.protobuf.Int32Value resistance_1 = 1;
            //     google.protobuf.Int32Value resistance_2 = 2;
            //     google.protobuf.Int32Value resistance_3 = 3;
            // }
            //
            // {'calculated_resistances_details': {'resistance_1': {'value': 21}}}

            data = data['calculated_resistances_details']
            sensorType.currentIndex = ['WITHOUT_EOL','ONE_EOL','TWO_EOL','THREE_EOL'].indexOf(wizardStorage['eol_scheme'])
            let mtr_resistances = util.mtr2_get_resistance().map(item => parseFloat(item))
            let resistance_1 = data['resistance_1']['value'] / 10

            if (wizardStorage['eol_scheme'] == 'ONE_EOL') {
                resistanceS2.currentIndex = mtr_resistances.indexOf(resistance_1)
                external_contact_mode_mt2.currentIndex = ['NO', 'NC'].indexOf(wizardStorage['normal_state_s1'])
            }
            if (wizardStorage['eol_scheme'] == 'TWO_EOL') {
                let resistance_2 = data['resistance_2']['value'] / 10
                resistanceS1.currentIndex = mtr_resistances.indexOf(resistance_1)
                resistanceS2.currentIndex = mtr_resistances.indexOf(resistance_2)
                externalContactStateModeS2.currentIndex = ['NO', 'NC'].indexOf(wizardStorage['normal_state_s2'])
            }
            if (wizardStorage['eol_scheme'] == 'THREE_EOL') {
                let resistance_2 = data['resistance_2']['value'] / 10
                let resistance_3 = data['resistance_3']['value'] / 10
                resistanceS1.currentIndex = mtr_resistances.indexOf(resistance_1)
                resistanceS2.currentIndex = mtr_resistances.indexOf(resistance_2)
                resistanceS3.currentIndex = mtr_resistances.indexOf(resistance_3)
                externalContactStateModeS2.currentIndex = ['NO', 'NC'].indexOf(wizardStorage['normal_state_s2'])
                externalContactStateModeS3.currentIndex = ['NO', 'NC'].indexOf(wizardStorage['normal_state_s3'])
            }
        }

        settingsForChangesChecker: [
            sensorType.currentIndex,
            typeComboboxS1.currentIndex,
            externalContactAlarmModeS1.currentIndex,
            resistanceS1.currentIndex,
            alwaysActiveS1.checked,
            typeComboboxS2.currentIndex,
            externalContactAlarmModeS2.currentIndex,
            externalContactStateModeS2.currentIndex,
            external_contact_mode_mt2.currentIndex,
            resistanceS2.currentIndex,
            alwaysActiveS2.checked,
            typeComboboxS3.currentIndex,
            externalContactAlarmModeS3.currentIndex,
            externalContactStateModeS3.currentIndex,
            resistanceS3.currentIndex,
            alwaysActiveS3.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            partialArm.checked,
            reactionTimeCombobox.currentIndex,
            chimes_button.chimeTriggers,
            chimes_button.chimeSignal,
            sirenS1.checked,
            sirenS2.checked,
            sirenS3.checked,
            sirenShortedOut.checked,
        ]
        generateSettings: () => {
            var bypass_signals = [19, 20] // only for mtr2

            let settings = {
                /* Common settings */
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "alarm_delay_seconds": alarmDelaySeconds.value,
                    "arm_delay_seconds": armDelaySeconds.value,
                    "perimeter_alarm_delay_seconds": perimeterAlarmDelaySeconds.value,
                    "perimeter_arm_delay_seconds": perimeterArmDelaySeconds.value,
                    "night_mode_arm": partialArm.checked,
                },
                "siren_triggers": [],

                /* General settings */
                "sensor_type": ["WITHOUT_EOL", "EOL", "TWO_EOL", "THREE_EOL"][sensorType.currentIndex],
                "reaction_time": reactionTimeCombobox.currentIndex + 1,
                "chime_triggers": chimes_button.chimeTriggers,
                "chime_signal": chimes_button.chimeSignal,

                /* S1 Endpoint (prev. Tamper or EPT) */
                "custom_alarm_S1": eventTypesWireMT2[typeComboboxS1.currentIndex],
                "external_contact_alarm_mode_S1": ["BISTABLE", "IMPULSE"][externalContactAlarmModeS1.currentIndex],
                "input_resistance_S1": resistanceS1.currentIndex + 10,
                "always_active_S1": alwaysActiveS1.checked,

                /* S2 Endpoint (prev. Alarm or EPA) */
                "custom_alarm_S2": eventTypesWireMT2[typeComboboxS2.currentIndex],
                "external_contact_alarm_mode": ["BISTABLE", "IMPULSE"][externalContactAlarmModeS2.currentIndex],
                "external_contact_state_mode_S2": sensorType.currentIndex >= 2 ?
                                                    ["NO", "NC"][externalContactStateModeS2.currentIndex] :
                                                    ["NO", "NC"][external_contact_mode_mt2.currentIndex],
                "input_resistance": resistanceS2.currentIndex + 10,
                "alwaysActive": alwaysActiveS2.checked,

                /* S3 Endpoint (prev. Malfunction or EPM) */
                "custom_alarm_S3": eventTypesWireMT2[typeComboboxS3.currentIndex],
                "external_contact_alarm_mode_S3": ["BISTABLE", "IMPULSE"][externalContactAlarmModeS3.currentIndex],
                "external_contact_state_mode_S3": ["NO", "NC"][externalContactStateModeS3.currentIndex],
                "input_resistance_S3": resistanceS3.currentIndex + 10,
                "always_active_S3": alwaysActiveS3.checked,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (sirenShortedOut.checked) {settings["siren_triggers"].push("SHORT_CIRCUIT")}
            if (sirenS1.checked) {settings["siren_triggers"].push("EXTRA_CONTACT_S1")}
            if (sirenS2.checked) {settings["siren_triggers"].push("EXTRA_CONTACT_S2")}
            if (sirenS3.checked) {settings["siren_triggers"].push("EXTRA_CONTACT_S3")}

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                DS3.SettingsPickerTitleSecondary {
                    id: sensorType

                    atomTitle.title: tr.input_type
                    model: [tr.no_eol, tr.one_eol, tr.two_eol, tr.three_eol]
                    currentIndex: ["WITHOUT_EOL","EOL","TWO_EOL","THREE_EOL"].indexOf(device.sensor_type)
                }

                DS3.SettingsPickerTitleSecondary {
                    id: external_contact_mode_mt2

                    atomTitle.title: tr.contacts_default_state
                    visible: [0, 1].includes(sensorType.currentIndex)
                    enabled: ![tr.tamper_alarm].includes(typeComboboxS2.model[typeComboboxS2.currentIndex])
                    model: [tr.normally_open, tr.normally_closed]
                    currentIndex: {
                        if ([tr.tamper_alarm].includes(typeComboboxS2.model[typeComboboxS2.currentIndex])) return 1
                        return defaultState === -1 ? ["NO","NC"].indexOf(device.external_contact_state_mode_S2) : defaultState
                    }
                    onActivated: {
                        defaultState = currentIndex
                    }
                }
            }

            DS3.Spacing {
                height: 24

                visible: wizardSection.visible
            }

            DS3.TitleSection {
                text: tr.connection_diagram_wire_input
                visible: wizardSection.visible

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }

            DS3.SettingsContainer {
                id: wizardSection

                visible: sensorType.currentIndex >= 1

                Rectangle {
                    width: parent.width
                    height: 166

                    color: ui.ds3.bg.high

                    DS3.Image {
                        width: 375
                        height: 166

                        anchors.centerIn: parent

                        source: {
                            if (sensorType.currentIndex === 1) {
                                return {
                                    0: "qrc:/resources/images/desktop/mtr_settings/schemes1eol_no.svg",
                                    1: "qrc:/resources/images/desktop/mtr_settings/schemes1eol_nc.svg",
                                }[external_contact_mode_mt2.currentIndex] || ""
                            } else if (sensorType.currentIndex === 2) {
                                return {
                                    0: "qrc:/resources/images/desktop/mtr_settings/schemes2eol_no.svg",
                                    1: "qrc:/resources/images/desktop/mtr_settings/schemes2eol_nc.svg",
                                }[externalContactStateModeS2.currentIndex] || ""
                            } else if (sensorType.currentIndex === 3) {
                                if (externalContactStateModeS2.currentIndex == 0) {
                                    return {
                                        0: "qrc:/resources/images/desktop/mtr_settings/schemes3eol_nono.svg",
                                        1: "qrc:/resources/images/desktop/mtr_settings/schemes3eol_nonc.svg",
                                    }[externalContactStateModeS3.currentIndex] || ""
                                } else if (externalContactStateModeS2.currentIndex == 1) {
                                    return {
                                        0: "qrc:/resources/images/desktop/mtr_settings/schemes3eol_ncno.svg",
                                        1: "qrc:/resources/images/desktop/mtr_settings/schemes3eol_ncnc.svg",
                                    }[externalContactStateModeS3.currentIndex] || ""
                                }
                            }
                            return ""
                        }
                    }
                }

                DS3.SettingsNavigationTitlePrimary {
                    visible: __mtr2_wizard_features__
                    title: tr.resistance_measurement_title
                    icon: "qrc:/resources/images/Athena/mtr2_wizard/MTR2WizardStart-M.svg"

                    onEntered: {
                        wizardStorage = {}
                        wizardStorage['measure_1_is_valid'] = true
                        wizardStorage['measure_2_is_valid'] = true
                        wizardStorage['measure_3_is_valid'] = true
                        wizardStorage['eol_scheme'] = ['WITHOUT_EOL','ONE_EOL','TWO_EOL','THREE_EOL'][sensorType.currentIndex]
                        if (wizardStorage['eol_scheme'] == 'ONE_EOL') {
                            wizardStorage['normal_state_s1'] = ['NO', 'NC'][external_contact_mode_mt2.currentIndex]
                        }
                        let [path, sensor] = wizard_steps()[0]
                        setChild(path, {'sensor': sensor, 'currentIndex': 0})
                    }
                }
            }

            DS3.Spacing {
                height: 24
                visible: sensor1.visible
            }
            // S1
            DS3.TitleSection {
                text: tr.sensor_one_settings
                visible: sensor1.visible

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }
            DS3.SettingsContainer {
                id: sensor1

                visible: sensorType.currentIndex >= 2

                DS3.SettingsPickerTitleSecondary {
                    id: typeComboboxS1

                    onCurrentIndexChanged:{
                        if([tr.tamper_alarm].includes(model[currentIndex])) {
                            externalContactAlarmModeS1.currentIndex = 0
                            alwaysActiveS1.checked = true
                        }
                        if(wireMT2CustomAlarmWithPreset.includes(model[currentIndex])) {
                            alwaysActiveS1.checked = true
                        }
                    }
                    model: wireMT2CustomAlarms
                    currentIndex: eventTypesWireMT2.indexOf(device.custom_alarm_S1)
                    atomTitle.title: tr.alarm_type
                    commentText: tr.custom_event_descr
                }

                DS3.SettingsPickerTitleSecondary {
                    id: externalContactAlarmModeS1

                    visible: sensorType.currentIndex >= 1
                    enabled: ![tr.tamper_alarm].includes(typeComboboxS1.model[typeComboboxS1.currentIndex])
                    model: [tr.bistable, tr.pulse]
                    currentIndex: ["BISTABLE","IMPULSE"].indexOf(device.external_contact_alarm_mode_S1)
                    atomTitle.title: tr.operating_mode_wire_input
                }

                DS3.SettingsPickerTitleSecondary {
                    id: resistanceS1

                    model: util.mtr2_get_resistance().map((item) => item + " " + tr.resistance_value)
                    currentIndex: model.indexOf((device.input_resistance_S1 / 10).toFixed(1) + " " + tr.resistance_value)
                    atomTitle.title: tr.resistor_one_resistance
                }

                DS3.SettingsSwitch {
                    id: alwaysActiveS1

                    enabled: ![tr.fire_alarm,tr.gas_alarm,tr.medical_alarm,tr.panic_alarm,tr.malfunction,tr.leakage_alarm,tr.tamper_alarm].includes(typeComboboxS1.model[typeComboboxS1.currentIndex])
                    checked: device.always_active_S1
                    title: tr.always_active
                }
            }

            DS3.Spacing {
                height: 24
                visible: sensor2.visible
            }
            // S2
            DS3.TitleSection {
                text: {
                    return {
                        0:null,
                        1:tr.sensor_settings_wire_input,
                        2:tr.sensor_two_settings,
                        3:tr.sensor_two_settings,
                    }[sensorType.currentIndex] || null
                }
                visible: sensor2.visible && !!text

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }
            DS3.SettingsContainer {
                id: sensor2

                DS3.SettingsPickerTitleSecondary {
                    id: typeComboboxS2

                    model: wireMT2CustomAlarms
                    currentIndex: eventTypesWireMT2.indexOf(device.custom_alarm_S2)
                    atomTitle.title: tr.alarm_type
                    commentText: tr.custom_event_descr

                    onCurrentIndexChanged: {
                        if([tr.tamper_alarm].includes(model[currentIndex])) {
                            externalContactStateModeS2.currentIndex = 1
                            externalContactAlarmModeS2.currentIndex = 0
                            alwaysActiveS2.checked = true
                        }
                        if(wireMT2CustomAlarmWithPreset.includes(model[currentIndex])) {
                            alwaysActiveS2.checked = true
                        }
                    }
                }

                DS3.SettingsPickerTitleSecondary {
                    id: externalContactAlarmModeS2

                    enabled: ![tr.tamper_alarm].includes(typeComboboxS2.model[typeComboboxS2.currentIndex])
                    model: [tr.bistable, tr.pulse,]
                    currentIndex: ["BISTABLE", "IMPULSE",].indexOf(device.external_contact_alarm_mode_S2)
                    atomTitle.title: tr.operating_mode_wire_input
                }

                DS3.SettingsPickerTitleSecondary {
                    id: externalContactStateModeS2

                    visible: sensorType.currentIndex >= 2
                    enabled: ![tr.tamper_alarm].includes(typeComboboxS2.model[typeComboboxS2.currentIndex])
                    model: [tr.normally_open, tr.normally_closed]
                    currentIndex: defaultState === -1 ? ["NO","NC"].indexOf(device.external_contact_state_mode_S2) : defaultState
                    atomTitle.title: tr.contacts_default_state

                    onActivated: {
                        defaultState = currentIndex
                    }
                }

                DS3.SettingsPickerTitleSecondary {
                    id: resistanceS2

                    visible: sensorType.currentIndex >= 1
                    model: util.mtr2_get_resistance().map((item) => item + " " + tr.resistance_value)
                    currentIndex: model.indexOf((device.input_resistance_S2 / 10).toFixed(1) + " " + tr.resistance_value)
                    atomTitle.title: sensorType.currentIndex == 1 ? tr.resistor_one_resistance : tr.resistor_two_resistance
                }

                DS3.SettingsSwitch {
                    id: alwaysActiveS2

                    enabled: ![tr.fire_alarm,tr.gas_alarm,tr.medical_alarm,tr.panic_alarm,tr.malfunction,tr.leakage_alarm,tr.tamper_alarm].includes(typeComboboxS2.model[typeComboboxS2.currentIndex])
                    checked: device.always_active_S2
                    title: tr.always_active
                }
            }

            DS3.Spacing {
                height: 24
                visible: sensor3.visible
            }
            // S3
            DS3.TitleSection {
                text: tr.sensor_three_settings
                visible: sensor3.visible

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }
            DS3.SettingsContainer {
                id: sensor3

                visible: sensorType.currentIndex == 3

                DS3.SettingsPickerTitleSecondary {
                    id: typeComboboxS3

                    model: wireMT2CustomAlarms
                    currentIndex: eventTypesWireMT2.indexOf(device.custom_alarm_S3)
                    atomTitle.title: tr.alarm_type
                    commentText: tr.custom_event_descr

                    onCurrentIndexChanged:{
                        if([tr.tamper_alarm].includes(model[currentIndex])) {
                            externalContactStateModeS3.currentIndex = 1
                            externalContactAlarmModeS3.currentIndex = 0
                            alwaysActiveS3.checked = true
                        }
                        if(wireMT2CustomAlarmWithPreset.includes(model[currentIndex])) {
                            alwaysActiveS3.checked = true
                        }
                    }
                }

                DS3.SettingsPickerTitleSecondary {
                    id: externalContactAlarmModeS3

                    enabled: ![tr.tamper_alarm].includes(typeComboboxS3.model[typeComboboxS3.currentIndex])
                    model: [tr.bistable, tr.pulse,]
                    currentIndex: ["BISTABLE", "IMPULSE",].indexOf(device.external_contact_alarm_mode_S3)
                    atomTitle.title: tr.operating_mode_wire_input
                }

                DS3.SettingsPickerTitleSecondary {
                    id: externalContactStateModeS3

                    enabled: ![tr.tamper_alarm].includes(typeComboboxS3.model[typeComboboxS3.currentIndex])
                    model: [tr.normally_open, tr.normally_closed]
                    currentIndex: ["NO","NC"].indexOf(device.external_contact_state_mode_S3)
                    atomTitle.title: tr.contacts_default_state
                }

                DS3.SettingsPickerTitleSecondary {
                    id: resistanceS3

                    model: util.mtr2_get_resistance().map((item) => item + " " + tr.resistance_value)
                    currentIndex: model.indexOf((device.input_resistance_S3 / 10).toFixed(1) + " " + tr.resistance_value)
                    atomTitle.title: tr.resistor_three_resistance
                }

                DS3.SettingsSwitch {
                    id: alwaysActiveS3

                    enabled: ![tr.fire_alarm,tr.gas_alarm,tr.medical_alarm,tr.panic_alarm,tr.malfunction,tr.leakage_alarm,tr.tamper_alarm].includes(typeComboboxS3.model[typeComboboxS3.currentIndex])
                    checked: device.always_active_S3
                    title: tr.always_active
                }
            }

            DS3.Spacing {
                height: 24
                visible: alarmDelaySection.visible
            }
            // alarm delay
            DS3.SettingsContainer {
                id: alarmDelaySection

                Settings.AlarmDelaySeconds {id: alarmDelaySeconds }
                Settings.ArmDelaySeconds { id: armDelaySeconds }
                Settings.PartialArm { id: partialArm }
                Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }

                DS3.SettingsPickerTitleSecondary {
                    id: reactionTimeCombobox

                    model:  ["20 " + tr.time_value_ms, "100 " + tr.time_value_ms, "1 " + tr.sec]
                    currentIndex: device.reaction_time - 1
                    atomTitle.title: tr.reaction_time_kind
                }
            }

            DS3.Spacing {
                height: 24
                visible: siren_bits.visible
            }
            // siren
            DS3.TitleSection {
                text: tr.alert_with_a_siren
                visible: siren_bits.visible

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }
            DS3.SettingsContainer {
                id: siren_bits

                DS3.SettingsSwitch {
                    id: sirenS1

                    title: tr.if_sensor_one_triggered
                    checked: device.siren_triggers.includes("EXTRA_CONTACT_S1")
                    visible: [2, 3].includes(sensorType.currentIndex)
                }

                DS3.SettingsSwitch {
                    id: sirenS2

                    title: {
                        if (sensorType.currentIndex === 1) return tr.if_device_triggered
                        if (sensorType.currentIndex === 0) return tr.if_alarm_detected
                        return tr.if_sensor_two_triggered
                    }
                    checked: device.siren_triggers.includes("EXTRA_CONTACT_S2")
                }

                DS3.SettingsSwitch {
                    id: sirenS3

                    title: tr.if_sensor_three_triggered
                    checked: device.siren_triggers.includes("EXTRA_CONTACT_S3")
                    visible: sensorType.currentIndex === 3
                }

                DS3.SettingsSwitch {
                    id: sirenShortedOut

                    title: tr.if_wire_input_shorted_out
                    checked: device.siren_triggers.includes("SHORT_CIRCUIT")
                    visible: sensorType.currentIndex !== 0
                }
            }

            DS3.Spacing {
                height: 24
                visible: chimes_button.visible
            }

            DS3.SettingsContainer {
                id: chimes_button

                property var inputType: sensorType.currentIndex
                property var chimeTriggers: device.chime_triggers
                property var chimeSignal: device.chime_signal

                DS3.SettingsNavigationTitlePrimary {
                    title: tr.chimes_title
                    subtitle: device.chime_triggers.length > 0 ? tr.on : tr.off

                    onEntered: {
                        setChild(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/advanced_settings/WIMT2ChimesSettingsPopupStep.qml",
                            {"chimesItem": chimes_button}
                        )
                    }
                }
            }
            DS3.Comment {
                width: parent.width

                text: tr.chimes_device_settings_tip
            }

            DS3.Spacing {
                height: 24
                visible: siren_bits.visible
            }
        }

        DS3.SettingsContainer {
            Parts.BypassButtonNav {}
        }
    }
}