import QtQuick 2.12
import QtQuick.Controls 2.2


import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.Dialog {
    id: popup

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }

    title: tr.Change_hub_name_desktop
    hasCrossButton: false
    firstButtonText: tr.save
    secondButtonText: tr.cancel
    isInput: true
    inputValueHandler: (hubName) => {
        if (!hubName) {
            Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
            return
        }
        app.hub_management_module.apply_update(management, hub, {"name": {"name": hubName}})
    }
    inputFieldAtomInput {
        text: hub.name
        label: tr.name

        onTextChanged: {
            inputFieldAtomInput.text = util.validator(inputFieldAtomInput.text, 24)
        }
    }
}