import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups

DS3.ButtonBar {
    id: nextButton

    width: parent.width

    anchors {
        bottom: parent.bottom
        horizontalCenter: parent.horizontalCenter
    }

    buttonText: tr.next
    hasBackground: true
    hasStepper: true
    stepAmount: {
        if (hub.hub_type == "YAVIR") {
            return 5
        } else if (hub.hub_type == "YAVIR_PLUS") {
            return 7
        } else {
            return 10
        }
    }

    buttons: DS3.ButtonText {
        id: cancelButton

        text: tr.cancel
        visible: serviceSettings.isWizard

        onClicked: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
            {
                title: tr.confirm_deletion,
                text: tr.all_settings_will_be_saved_to_complete_you_will_have,
                firstButtonCallback: () => {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/ServiceSettings.qml")
                },
                firstButtonText: tr.exit_wizard,
                secondButtonText: tr.cancel,
                isVertical: true,
            }
        )
    }
}