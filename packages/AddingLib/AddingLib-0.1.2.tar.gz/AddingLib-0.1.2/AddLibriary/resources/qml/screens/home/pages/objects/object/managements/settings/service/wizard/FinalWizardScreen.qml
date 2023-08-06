import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: finalWizardScreen

    property bool isNotPdCompliance: serviceSettings.notCompliantWizardScreens.length
    property var sideMargin: 24

    color: ui.ds3.bg.base

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }
    
    DS3.NavBarModal {
        id: finalWizardBar

        headerText: tr.PD_compliance_wizard
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            if (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS") {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml")
            } else {
                if (serviceSettings.notCompliantWizardScreens.includes(tr.beep_on_delay_pd)) {
                    var index = serviceSettings.notCompliantWizardScreens.indexOf(tr.beep_on_delay_pd)
                    if (index !== -1) {
                        serviceSettings.notCompliantWizardScreens.splice(index, 1)
                    }
                }
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/WizardBeepDevices.qml")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: finalWizardBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        width: parent.width

        padding: sideMargin

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.BigImage
            imageSource: "qrc:/resources/images/Athena/PD_compliant/WizardWarning.svg"
            descComponent.text: tr.wizard_is_partially_complete
            visible: isNotPdCompliance
        }

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.BigImage
            imageSource: "qrc:/resources/images/Athena/PD_compliant/WizardComplete.svg"
            titleComponent.text: tr.hub_is_succesfully_set_according_to_PD_standard
            descComponent.text: tr.all_settings_can_be_changed_in_anvanced_settings
            visible: !isNotPdCompliance
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                id: nonPDSetting

                imageItem.visible: false
                atomTitle.subtitle: {
                    let final_text = tr.final_settings_are_not_PD6662_wizard + ":\n"
                    for(let i = 0; i < serviceSettings.notCompliantWizardScreens.length; i++){
                        final_text = final_text + "\n" + serviceSettings.notCompliantWizardScreens[i]
                    }
                    return final_text + "\n\n" + tr.all_settings_can_be_changed_in_anvanced_settings
                }
                visible: isNotPdCompliance
            }
        }

        DS3.Spacing {
            height: nonPDSetting.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                imageItem.visible: false
                atomTitle {
                    title: tr.all_users_are_added_and_have_permissions
                    subtitle: tr.go_to_user_settings
                }
            }
        }
    }

    Parts.ButtonNextCancelPD {
        id: nextButton

        buttonText: tr.complete_2fa
        enabled: devEnable
        hasStepper: true
        stepAmount: hub.hub_type.startsWith("YAVIR") ? 5 : 10
        currentStep: stepAmount - 1

        button.onClicked: {
            serviceSettings.closeWizard()
        }
    }
}