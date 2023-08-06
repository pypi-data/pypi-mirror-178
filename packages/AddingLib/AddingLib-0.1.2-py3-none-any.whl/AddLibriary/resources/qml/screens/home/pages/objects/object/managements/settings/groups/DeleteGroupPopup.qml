import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3Popups.Dialog {
    id: dialog

    title: tr.delete_group
    text: util.insert(tr.you_are_about_to_delete_group_all_settings_will_be_erased_continue, [group.name])
    firstButtonText: tr.delete
    secondButtonText: tr.cancel
    isVertical: true
    isFirstButtonRed: true

    firstButtonCallback: () => {
        Popups.please_wait_popup()
        app.hub_management_module.delete_group(hub, group.id)
    }
}
