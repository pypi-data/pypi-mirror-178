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
    property string eolPath: "qrc:/resources/images/Athena/mtr2_wizard/" + eolScheme + "/" + eolScheme + secondState + thirdState + contactTriggerDependency

    Component.onDestruction: {
        delete wizardStorage.contact_trigger_dependency
    }

    DS3.Spacing { height: 48 }

    DS3.InfoContainer {
        id: infoContainer

        imageType: DS3.InfoContainer.ImageType.WizardImage
        imageSource: eolPath + "_BINDING.svg"
        titleComponent.text: tr.sensor_depend_on_sensor_title
        descComponent.text: tr.contact_default_state_descr
    }

    DS3.SettingsContainer {
        width: parent.width - 48

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.SettingsSingleSelection {
            id: dependency

            atomTitle.title: tr.sensor_depends_on_sensor
            switchChecked: () => {
                infoContainer.imageSource = eolPath + "S2_S3_DEPENDENT.svg"
                dependency.checked = true
                independency.checked = false
            }
        }

        DS3.SettingsSingleSelection {
            id: independency

            atomTitle.title: tr.sensor_not_depend_on_sensor
            switchChecked: () => {
                infoContainer.imageSource = eolPath + "S2_S3_INDEPENDENT.svg"
                dependency.checked = false
                independency.checked = true
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
        enabled: dependency.checked || independency.checked

        button.onClicked: {
            popup.wizardStorage['contact_trigger_dependency'] = dependency.checked ? 'S2_S3_DEPENDENT' : 'S2_S3_INDEPENDENT'

            let [path, next_step_sensor] = popup.wizard_steps()[currentIndex + 1]
            step.setChild(path, {'sensor': next_step_sensor, 'currentIndex': currentIndex + 1})
        }
    }
}