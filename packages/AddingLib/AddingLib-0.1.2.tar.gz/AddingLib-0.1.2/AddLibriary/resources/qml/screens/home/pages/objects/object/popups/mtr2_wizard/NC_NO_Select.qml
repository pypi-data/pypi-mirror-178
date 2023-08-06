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
    property string eolScheme: wizardStorage.eol_scheme ? wizardStorage.eol_scheme : ""
    property string secondState: wizardStorage.normal_state_s2 ? wizardStorage.normal_state_s2 : ""
    property string thirdState: wizardStorage.normal_state_s3 ? wizardStorage.normal_state_s3 : ""
    property string contactTriggerDependency: wizardStorage.contact_trigger_dependency ? wizardStorage.contact_trigger_dependency : ""

    property string eolPath: "qrc:/resources/images/Athena/mtr2_wizard/" + eolScheme + "/" + eolScheme + secondState + thirdState + "_" + contactTriggerDependency

    Component.onDestruction: {
        if (wizardStorage.normal_state_s2) delete wizardStorage.normal_state_s2
        if (wizardStorage.normal_state_s3) delete wizardStorage.normal_state_s3
    }

    function resetAll() {
        wizardNO.checked = false
        wizardNC.checked = false
    }


    DS3.Spacing { height: 48 }

    DS3.InfoContainer {
        id: infoContainer

        imageType: DS3.InfoContainer.ImageType.WizardImage
        imageSource: "qrc:/resources/images/Athena/mtr2_wizard/" + wizardStorage.eol_scheme + "/" + wizardStorage.eol_scheme + secondState + "_DEF_NC.svg"
        titleComponent.text: {
            let titleText = wizardStorage.normal_state_s2 ? tr.sensor_three_contact_default_state_title : tr.contact_default_state_title
            return util.insert(titleText, [{
                'measure_1':1,
                'measure_2':2,
                'measure_3':3,
            }[sensor]])
        }
        descComponent.text: {
            let titleText = wizardStorage.normal_state_s2 ? tr.measure_sensor_one_resistanse_descr : tr.contact_default_state_descr
            return util.insert(titleText, [{
                'measure_1':1,
                'measure_2':2,
                'measure_3':3,
            }[sensor]])
        }
    }

    DS3.SettingsContainer {
        width: parent.width - 48

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.SettingsSingleSelection {
            id: wizardNO

            atomTitle.title: tr.normally_open
            switchChecked: () => {
                infoContainer.imageSource = eolPath + "DEF_NO.svg"

                wizardNO.checked = true
                wizardNC.checked = false
            }
        }

        DS3.SettingsSingleSelection {
            id: wizardNC

            atomTitle.title: tr.normally_closed
            switchChecked: () => {
                infoContainer.imageSource = eolPath + "DEF_NC.svg"

                wizardNO.checked = false
                wizardNC.checked = true
            }
        }
    }

    footer: DS3.ButtonBar {
        id: buttonBar

        hasStepper: true
        stepAmount: popup.wizard_steps().length
        currentStep: currentIndex

        buttonText: tr.next
        hasBackground: true
        enabled: wizardNC.checked || wizardNO.checked

        button.onClicked: {
            popup.wizardStorage[`normal_state_s${ {'measure_2':2,'measure_3':3,}[sensor] }`] = wizardNO.checked ? 'NO' : 'NC'

            let [path, next_step_sensor] = popup.wizard_steps()[currentIndex + 1]
            step.setChild(path, {'sensor': next_step_sensor, 'currentIndex': currentIndex + 1})
        }
    }
}