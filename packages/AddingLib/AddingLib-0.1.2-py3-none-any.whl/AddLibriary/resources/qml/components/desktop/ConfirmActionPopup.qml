import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.Dialog {
    id: popup

    title: tr.stop_migration_popup
    text: tr.stop_migration_popup_info
    firstButtonText: tr.interrupt_button
    secondButtonText: tr.cancel
    firstButtonCallback: () => {
        app.stop_migration(hub.hub_id)
    }
    isVertical: true
    isFirstButtonRed: true
    firstButtonIsOutline: true
}
