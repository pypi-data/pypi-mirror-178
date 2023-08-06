import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS/" as DS
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

DS3Popups.PopupStep {
    id: step

    property var currentIndex: 0
    property var sensor: null
    property string eolScheme: wizardStorage.eol_scheme ? wizardStorage.eol_scheme : ""
    property string secondState: wizardStorage.normal_state_s2 ? wizardStorage.normal_state_s2 : ""
    property string thirdState: wizardStorage.normal_state_s3 ? wizardStorage.normal_state_s3 : ""
    property string contactTriggerDependency: wizardStorage.contact_trigger_dependency ? wizardStorage.contact_trigger_dependency : ""
    property string eolPath: "qrc:/resources/images/Athena/mtr2_wizard/" + eolScheme + "/" + eolScheme + secondState + thirdState + contactTriggerDependency
    property var isProgressBar: false
    property var isButtonBar: true
    property var buttonBarText: ""
    property var action: () => {
        loadingMode()
        app.hub_management_module.wireMT2_measure_resistance(device.id, sensor)
    }

    Component.onCompleted: {
        resetAll()
    }

    Component.onDestruction: {
        if (!wizardStorage[`${step.sensor}_is_valid`]) delete wizardStorage[step.sensor]
        if (wizardStorage.measure_1 && wizardStorage.measure_2 && wizardStorage.measure_3) delete wizardStorage.measure_3
        if (wizardStorage.isEqual_S1_S2) delete wizardStorage.measure_2
        if (wizardStorage.isEqual_S2_S3) delete wizardStorage.measure_3
    }

    Connections {
        target: app.hub_management_module

        onMtr2MeasureFineshed: {
            if (step.sensor == sensor){
                result = JSON.parse(result)
                if (result['answer'] == 'BUSY') {
                    resetAll()
                } else if (result['measure_details']['status'] == 'REQUEST_ERROR') {
                    errorModeFailedToMeasure()
                } else if (result['measure_details']['status'] == 'ERROR') {
                    if (wizardStorage.eol_scheme === "ONE_EOL") infoContainer.imageSource = eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1_FAILED.svg"

                    else if (wizardStorage.measure_1 && wizardStorage.measure_2) {
                        infoContainer.imageSource = eolPath + "_MEASURE_3_FAILED.svg"
                    }
                    else if (wizardStorage.measure_1) {
                        infoContainer.imageSource = eolPath + "_MEASURE_2_FAILED.svg"
                    }
                    else if (wizardStorage.measure_1 && wizardStorage.isEqual_S1_S2) {
                        infoContainer.imageSource = eolPath + "_MEASURE_1_FAILED.svg"
                    }
                    else infoContainer.imageSource = eolPath + "_MEASURE_1_FAILED.svg"

                    if (!wizardStorage.measure_1_is_valid && wizardStorage.measure_1) infoContainer.imageSource = eolPath + "_MEASURE_1_FAILED.svg"
                    else if (!wizardStorage.measure_2_is_valid && wizardStorage.measure_2) infoContainer.imageSource = eolPath + "_MEASURE_2_FAILED.svg"
                    else if (!wizardStorage.measure_1_is_valid && wizardStorage.measure_3) infoContainer.imageSource = eolPath + "_MEASURE_3_FAILED.svg"

                    errorModeFailedToMeasure()
                } else if (result['measure_details']['status'] == 'SUCCESS') {
                    resetAll()
                    let is_resistances_equal = (first_res, second_res) => {
                        return Math.min(first_res * 0.1, second_res * 0.1) >
                                Math.max(second_res - first_res, first_res - second_res)
                    }
                    popup.wizardStorage[step.sensor] = result['measure_details']['ohms']['value']
                    if (Math.round(popup.wizardStorage[step.sensor] / 100.0) / 10.0 > 45 || Math.round(popup.wizardStorage[step.sensor] / 100.0) / 10.0 < 1) { // A911-5661
                        wizardStorage[`${step.sensor}_is_valid`] = false

                        if (wizardStorage.eol_scheme === "ONE_EOL") infoContainer.imageSource = eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1_FAILED.svg"
                        else if (step.sensor === "measure_1") infoContainer.imageSource = eolPath + "_MEASURE_1_FAILED.svg"
                        else if (step.sensor === "measure_2") infoContainer.imageSource = eolPath + "_MEASURE_2_FAILED.svg"
                        else if (step.sensor === "measure_3") infoContainer.imageSource = eolPath + "_MEASURE_3_FAILED.svg"

                        return errorModeFailedToMeasure() // A911-5583
                    }
                    if (step.sensor == 'measure_2') {
                        if (is_resistances_equal(popup.wizardStorage['measure_1'], popup.wizardStorage['measure_2'])) {
                            wizardStorage.isEqual_S1_S2 = true
                            if (wizardStorage.measure_1 && wizardStorage.measure_2) {
                               infoContainer.imageSource = eolPath + "_MEASURE_2_FAILED.svg"
                            }
                            return errorModeFailedToMeasure() // yeah, they equal, but we raising default error
                        }
                    }
                    if (step.sensor == 'measure_3') {
                        if (is_resistances_equal(popup.wizardStorage['measure_1'], popup.wizardStorage['measure_3'])) {
                            wizardStorage.isEqual_S1_S3 = true

                            if (wizardStorage.measure_1 && wizardStorage.measure_2 && wizardStorage.measure_3) {
                               infoContainer.imageSource = eolPath + "_MEASURE_3_FAILED.svg"
                            }

                            return errorModeFailedToMeasure() // yeah, they equal, but we raising default error
                        }
                        if (is_resistances_equal(popup.wizardStorage['measure_2'], popup.wizardStorage['measure_3'])) {
                            if (wizardStorage.measure_1 && wizardStorage.measure_2 && wizardStorage.measure_3) {
                               infoContainer.imageSource = eolPath + "_MEASURE_3_FAILED.svg"
                            }
                            wizardStorage.isEqual_S2_S3 = true

                            return errorModeFailedToMeasure()
                        }
                    }
                    if (popup.wizard_steps().length - 2 == currentIndex) {
                        loadingMode()
                        app.hub_management_module.calculate_resistances_MTR2(JSON.stringify(popup.wizardStorage), sensor)
                    } else {
                        let [path, next_step_sensor] = popup.wizard_steps()[currentIndex + 1]
                        step.setChild(path, {'sensor': next_step_sensor, 'currentIndex': currentIndex + 1})
                    }
                }
            }
        }

        onHubIsOfflineWizard: {
            DesktopPopups.error_popup(error_text)
            errorModeFailedToMeasure()
        }

        onMtr2ResistanceCalcFinished: {
            if (step.sensor == sensor){
                resetAll()
                result = JSON.parse(result)
                if (result['calculated_resistances_details']['status'] == 'REQUEST_ERROR') {
                    resetAll()
                } else if (result['calculated_resistances_details']['status'] == 'ERROR_R2_EQUALS_R3') {
                    errorResistanceEqual()
                } else if (result['calculated_resistances_details']['status'] == 'ERROR') {
                    calculateFailed()
                    action = () => {
                        popup.child.child.resetAll()
                        if (step.sensor != 'measure_1') {
                            step.goBack(currentIndex)
                        }
                    }
                } else {
                    let [path, next_step_sensor] = popup.wizard_steps()[currentIndex + 1]
                    step.setChild(path, {'sensor': next_step_sensor, 'currentIndex': currentIndex + 1, 'calculated_result': result})
                }
            }
        }
    }

    function formatResistorNumber(tr) {
        return tr.replace('{0}', {
            'measure_1':1,
            'measure_2':2,
            'measure_3':3,
        }[sensor])
    }

    function resetAll() {
        isButtonBar = true
        action = () => {
            loadingMode()
            app.hub_management_module.wireMT2_measure_resistance(device.id, sensor)
        }
        isProgressBar = false
        popup.measuringInProgress = false
        buttonBarText = tr.measure_button

        if (wizardStorage['eol_scheme'] == 'ONE_EOL') {
            infoContainer.titleComponent.text = tr.measure_normal_resistance_title
            infoContainer.descComponent.text = tr.measure_sensor_one_resistanse_descr
        } else if (wizardStorage['eol_scheme'] == 'TWO_EOL') {
            infoContainer.titleComponent.text = {
                'measure_1': tr.measure_normal_resistance_title,
                'measure_2': formatResistorNumber(tr.measure_sensor_resistanse_title),
            }[sensor]
            infoContainer.descComponent.text = {
                'measure_1': tr.measure_sensor_one_resistanse_descr,
                'measure_2': wizardStorage['normal_state_s2'] == 'NC' ? tr.trigger_sensor_two_eol_to_measure_descr : tr.trigger_sensor_two_to_measure_descr_three,
            }[sensor]
        } else if (wizardStorage['eol_scheme'] == 'THREE_EOL') {
            let threeEOLKeySecondMeasure = ""
            let threeEOLKeyThirdMeasure = ""

            if (wizardStorage['normal_state_s2'] === "NC" && wizardStorage['normal_state_s3'] === "NC") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_eol_to_measure_descr
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_three
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_two
            }
            else if (wizardStorage['normal_state_s2'] === "NC" && wizardStorage['normal_state_s3'] === "NO") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr_two
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_four
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr
            }
            else if (wizardStorage['normal_state_s2'] === "NO" && wizardStorage['normal_state_s3'] === "NC") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr_three
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_two
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_three
            }
            else if (wizardStorage['normal_state_s2'] === "NO" && wizardStorage['normal_state_s3'] === "NO") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_four
            }

            infoContainer.titleComponent.text = {
                'measure_1': tr.measure_normal_resistance_title,
                'measure_2': formatResistorNumber(tr.measure_sensor_resistanse_title),
                'measure_3': formatResistorNumber(tr.measure_sensor_resistanse_title),
            }[sensor]
            infoContainer.descComponent.text = {
                'measure_1': tr.measure_sensor_one_resistanse_descr,
                'measure_2': threeEOLKeySecondMeasure,
                'measure_3': threeEOLKeyThirdMeasure,
            }[sensor]
        }
    }

    function loadingMode() {
        isButtonBar = false
        isProgressBar = true
        popup.measuringInProgress = true

        if (wizardStorage.eol_scheme === "ONE_EOL") infoContainer.imageSource = eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1.svg"
        else if (wizardStorage.isEqual_S1_S2) infoContainer.imageSource = eolPath + "_MEASURE_2.svg"
        else if (!wizardStorage.measure_1) infoContainer.imageSource = eolPath + "_MEASURE_1.svg"
        else if (wizardStorage.measure_1 && !wizardStorage.measure_2 && !wizardStorage.measure_3) infoContainer.imageSource = eolPath + "_MEASURE_2.svg"
        else if (wizardStorage.eol_scheme === "THREE_EOL" && wizardStorage.measure_1 && wizardStorage.measure_2) {
            infoContainer.imageSource = eolPath + "_MEASURE_3.svg"
        }

        if(!wizardStorage.measure_1_is_valid && wizardStorage.eol_scheme === "ONE_EOL") infoContainer.imageSource = eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1.svg"
        else if (!wizardStorage.measure_1_is_valid) infoContainer.imageSource = eolPath + "_MEASURE_1.svg"
        else if (!wizardStorage.measure_2_is_valid) infoContainer.imageSource = eolPath + "_MEASURE_2.svg"
        else if (!wizardStorage.measure_3_is_valid) infoContainer.imageSource = eolPath + "_MEASURE_3.svg"

        if (wizardStorage['eol_scheme'] == 'ONE_EOL') {
            infoContainer.titleComponent.text = tr.measure_normal_resistance_title
            infoContainer.descComponent.text = tr.measure_sensor_one_resistanse_descr
        } else if (wizardStorage['eol_scheme'] == 'TWO_EOL') {
            infoContainer.titleComponent.text = {
                'measure_1': tr.measure_normal_resistance_title,
                'measure_2': formatResistorNumber(tr.measure_sensor_resistanse_title),
            }[sensor]
            infoContainer.descComponent.text = {
                'measure_1': tr.measure_sensor_one_resistanse_descr,
                'measure_2': wizardStorage['normal_state_s2'] == 'NC' ? tr.trigger_sensor_two_eol_to_measure_descr : tr.trigger_sensor_two_to_measure_descr_three,
            }[sensor]

        } else if (wizardStorage['eol_scheme'] == 'THREE_EOL') {
            let threeEOLKeySecondMeasure = ""
            let threeEOLKeyThirdMeasure = ""

            if (wizardStorage['normal_state_s2'] === "NC" && wizardStorage['normal_state_s3'] === "NC") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_eol_to_measure_descr
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_three
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_two
            }
            else if (wizardStorage['normal_state_s2'] === "NC" && wizardStorage['normal_state_s3'] === "NO") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr_two
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_four
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr
            }
            else if (wizardStorage['normal_state_s2'] === "NO" && wizardStorage['normal_state_s3'] === "NC") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr_three
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_two
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_three
            }
            else if (wizardStorage['normal_state_s2'] === "NO" && wizardStorage['normal_state_s3'] === "NO") {
                threeEOLKeySecondMeasure = tr.trigger_sensor_two_to_measure_descr
                if (wizardStorage.contact_trigger_dependency === "S2_S3_DEPENDENT")
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr
                else
                    threeEOLKeyThirdMeasure = tr.trigger_sensor_three_to_measure_descr_four
            }

            infoContainer.titleComponent.text = {
                'measure_1': tr.measure_normal_resistance_title,
                'measure_2': formatResistorNumber(tr.measure_sensor_resistanse_title),
                'measure_3': formatResistorNumber(tr.measure_sensor_resistanse_title),
            }[sensor]

            infoContainer.descComponent.text = {
                'measure_1': tr.measure_sensor_one_resistanse_descr,
                'measure_2': threeEOLKeySecondMeasure,
                'measure_3': threeEOLKeyThirdMeasure,
            }[sensor]
        }
    }
    function errorModeFailedToMeasure() {
        isButtonBar = true
        isProgressBar = false
        popup.measuringInProgress = false
        buttonBarText = tr.remeasure_button
        infoContainer.titleComponent.text = sensor == 'measure_1' ?
            tr.failed_measure_normal_resistance_title :
            formatResistorNumber(tr.failed_measure_resistance_title)
        infoContainer.descComponent.text = sensor =='measure_1' ?
                                            tr.failed_measure_first_sensor_resistance :
                                            tr.failed_measure_resistance_descr
    }
    function errorResistanceEqual() {
        isButtonBar = true
        isProgressBar = false
        popup.measuringInProgress = false

        buttonBarText = tr.remeasure_button
        infoContainer.titleComponent.text = tr.resistance_is_equal_title
        infoContainer.descComponent.text = tr.resistance_is_equal_descr
        infoContainer.imageSource = eolPath + "_MEASURE_3_EQUAL.svg"
    }
    function calculateFailed() {
        isButtonBar = true
        isProgressBar = false
        buttonBarText = tr.remeasure_button
        infoContainer.titleComponent.text = formatResistorNumber(tr.failed_measure_server_error_title)
        infoContainer.descComponent.text = tr.failed_measure_server_error_descr
        if (wizardStorage.eol_scheme !== "ONE_EOL") {
            infoContainer.imageType = DS3.InfoContainer.ImageType.BigImage
            infoContainer.imageSource = "qrc:/resources/images/Athena/mtr2_wizard/FINAL_RESISTANCE_VALUE_FAILED.svg"
        }
        else infoContainer.imageSource = eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1_FAILED.svg"
    }

    DS3.Spacing { height: 48 }

    DS3.InfoContainer {
        id: infoContainer

        imageType: DS3.InfoContainer.ImageType.WizardImage
        imageSource: {
            if (wizardStorage.eol_scheme === "ONE_EOL"){
                return eolPath + wizardStorage.normal_state_s1 + "_MEASURE_1.svg"
            }

            if (wizardStorage.measure_1 && wizardStorage.measure_2) {
                return eolPath + "_MEASURE_3.svg"
            }

            if (wizardStorage.measure_1) {
                return eolPath + "_MEASURE_2.svg"
            }
            return eolPath + "_MEASURE_1.svg"
        }
    }

    footer: Item {
        width: parent.width
        height: buttonBar.height

        DS3.ButtonBar {
            id: buttonBar

            visible: isButtonBar
            hasStepper: true
            stepAmount: popup.wizard_steps().length
            currentStep: currentIndex
            buttonText: buttonBarText
            hasBackground: true

            button.onClicked: action()
        }

        Rectangle {
            id: progressBar

            width: parent.width
            height: 92

            visible: isProgressBar
            color: ui.ds3.bg.high

            DS3.Stepper {
                anchors {
                    top: parent.top
                    topMargin: 8
                    horizontalCenter: parent.horizontalCenter
                }

                amount: popup.wizard_steps().length
                current: currentIndex
            }

            DS3.ButtonProgress {
                anchors.centerIn: parent
                anchors.horizontalCenter: parent.horizontalCenter

                textItem.text: tr.measuring_in_progress
            }
        }
    }
}