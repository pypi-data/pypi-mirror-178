import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS/" as DS
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    id: step

    property var currentIndex: null
    property var sensor: null
    property bool isLastStep: popup.wizard_steps().length - 1 == currentIndex
    property string eolScheme: wizardStorage.eol_scheme ? wizardStorage.eol_scheme : ""
    property string secondState: wizardStorage.normal_state_s2 ? wizardStorage.normal_state_s2 : ""
    property string thirdState: wizardStorage.normal_state_s3 ? wizardStorage.normal_state_s3 : ""
    property string contactTriggerDependency: wizardStorage.contact_trigger_dependency ? wizardStorage.contact_trigger_dependency : ""
    property string eolPath: "qrc:/resources/images/Athena/mtr2_wizard/" + eolScheme + "/" + eolScheme + secondState + thirdState + contactTriggerDependency
    property var calculated_result: null

    Component.onCompleted: {
        if (wizardStorage.measure_1) wizardStorage.measure_1_is_valid = true
        if (wizardStorage.measure_2) wizardStorage.measure_2_is_valid = true
        if (wizardStorage.measure_3) wizardStorage.measure_3_is_valid = true
        if (wizardStorage.isEqual_S1_S2) wizardStorage.isEqual_S1_S2 = false
        if (wizardStorage.isEqual_S2_S3) wizardStorage.isEqual_S1_S2 = false
        if (wizardStorage.isEqual_S1_S3) wizardStorage.isEqual_S1_S2 = false
    }

    Component.onDestruction: {
        if (wizardStorage.measure_1 && wizardStorage.measure_2 && !wizardStorage.measure_3) delete wizardStorage.measure_2
        else if (wizardStorage.measure_1 && !wizardStorage.measure_2 && !wizardStorage.measure_3) delete wizardStorage.measure_1
    }

    DS3.Spacing { height: 48 }

    DS3.InfoContainer {
        id: infoContainer

        imageType: DS3.InfoContainer.ImageType.WizardImage
        imageSource: {
            if (wizardStorage.eol_scheme === "ONE_EOL"){
                return eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1_SUCCESS.svg"
            }

            if (wizardStorage.eol_scheme === "THREE_EOL" && wizardStorage.measure_1 && wizardStorage.measure_2 && wizardStorage.measure_3) {
                infoContainer.imageType = DS3.InfoContainer.ImageType.BigImage
                return "qrc:/resources/images/Athena/mtr2_wizard/FINAL_RESISTANCE_VALUE.svg"
            }

            if (wizardStorage.eol_scheme === "TWO_EOL" && wizardStorage.measure_1 && wizardStorage.measure_2) {
                infoContainer.imageType = DS3.InfoContainer.ImageType.BigImage
                return "qrc:/resources/images/Athena/mtr2_wizard/FINAL_RESISTANCE_VALUE.svg"
            }

            if (wizardStorage.measure_1 && wizardStorage.measure_2) {
                return eolPath + "_MEASURE_2_SUCCESS.svg"
            }

            if (wizardStorage.measure_1) {
                return eolPath + "_MEASURE_1_SUCCESS.svg"
            }

            return eolPath + "_SUCCESS.svg"
        }
        titleComponent.text: {
            if (isLastStep) {
                if (popup.wizardStorage['eol_scheme'] == 'ONE_EOL') {
                    return tr.oneeol_resistance_measured_title
                }
                return tr.all_resistance_measured_title
            } else {
                return sensor == 'measure_1' ?
                    tr.measure_normal_resistance_result
                        .replace('{0}', Math.round(popup.wizardStorage[step.sensor] / 100) / 10.0) :
                    tr.alarm_resistance_value_desktop
                        .replace('{0}', {
                            'measure_1':1,
                            'measure_2':2,
                            'measure_3':3,
                        }[sensor])
                        .replace('{1}', Math.round(popup.wizardStorage[step.sensor] / 100) / 10.0)
            }
        }
        descComponent.text: {
            if (wizardStorage.eol_scheme === "ONE_EOL" && isLastStep) return tr.oneeol_resistance_measured_descr
            return isLastStep ? tr.all_resistance_measured_descr : tr.sensor_resistance_value_descr
        }
    }
    DS3.Spacing {
        height: 32
        visible: isLastStep
    }

    DS3.SettingsContainer {
        id: final_result

        width: parent.width - 48

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 32
        anchors.bottomMargin: 24

        visible: isLastStep

        Rectangle {
            width: parent.width
            height: 68

            color: ui.ds3.bg.highest
            DS3.AtomTitle {
                anchors.centerIn: parent
                width: parent.width - 32
                title: tr.resistor_one_resistance
                subtitle: isLastStep ? calculated_result['calculated_resistances_details']['resistance_1']['value'] / 10 + ' ' + tr.resistance_value : ''
            }
        }
        Rectangle {
            width: parent.width
            height: 68

            visible: ['TWO_EOL', 'THREE_EOL'].includes(popup.wizardStorage['eol_scheme'])
            color: ui.ds3.bg.highest

            DS3.AtomTitle {
                anchors.centerIn: parent
                width: parent.width - 32
                title: tr.resistor_two_resistance
                subtitle: isLastStep & ['TWO_EOL', 'THREE_EOL'].includes(popup.wizardStorage['eol_scheme']) ? String(calculated_result['calculated_resistances_details']['resistance_2']['value'] / 10 + ' ' + tr.resistance_value) : ''
            }
        }
        Rectangle {
            width: parent.width
            height: 68

            visible: 'THREE_EOL' == popup.wizardStorage['eol_scheme']
            color: ui.ds3.bg.highest

            DS3.AtomTitle {
                anchors.centerIn: parent
                width: parent.width - 32
                title: tr.resistor_three_resistance
                subtitle: isLastStep & 'THREE_EOL' == popup.wizardStorage['eol_scheme'] ? String(calculated_result['calculated_resistances_details']['resistance_3']['value'] / 10 + ' ' + tr.resistance_value) : ''
            }
        }
    }
    DS3.Spacing { height: isLastStep ? 24 : 200 }

    footer: DS3.ButtonBar {
        id: buttonBar

        hasStepper: true
        stepAmount: popup.wizard_steps().length
        currentStep: currentIndex
        buttonText: isLastStep ? tr.complete_2fa : tr.next
        hasBackground: true

        button.onClicked: {
            if (!currentIndex) {return} // костыль от закликивания, в последнюю секунду, 
            if (isLastStep) {
                deviceStep.apply_calculated_resistance(calculated_result)
                step.goBack(currentIndex + 1)
            } else {
                let [path, next_step_sensor] = popup.wizard_steps()[currentIndex + 1]
                step.setChild(path, {'sensor': next_step_sensor, 'currentIndex': currentIndex + 1})
            }
        }
    }
}